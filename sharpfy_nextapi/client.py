"""Cliente da NextAPI."""
import json
import os
import platform
import sys
import re
import random
import time
from email.utils import parsedate_to_datetime
from typing import Any, Optional
from urllib.parse import urlsplit

from sharpfy_nextapi import _version
from sharpfy_nextapi._transport import Transport, UrllibTransport
from sharpfy_nextapi.errors import NextApiAuthenticationError, NextApiConnectionError, error_class
from sharpfy_nextapi.resources.ceps import Ceps
from sharpfy_nextapi.resources.cnpj import Cnpj
from sharpfy_nextapi.resources.creditos import Creditos
from sharpfy_nextapi.resources.empresas import Empresas
from sharpfy_nextapi.resources.localidades import Cnaes, Estados, Municipios
from sharpfy_nextapi.resources.mercado import Mercado
from sharpfy_nextapi.resources.socios import Socios

DEFAULT_BASE_URL = "https://api.nextapi.com.br"
_RETRYABLE = {429, 502, 503, 504}
_LOCAL = {"localhost", "127.0.0.1", "::1"}


class NextApiClient:
    """Cliente da NextAPI. Sem dependências: só a biblioteca padrão.

    >>> nextapi = NextApiClient()  # lê NEXTAPI_KEY
    >>> empresa = nextapi.cnpj.consultar("11.222.333/0001-81")

    :param api_key: ``nxa_live_…`` (produção) ou ``nxa_test_…`` (sandbox). Padrão: ``NEXTAPI_KEY``.
    :param base_url: padrão ``https://api.nextapi.com.br``; só https (http apenas para localhost).
    :param timeout: segundos por tentativa (padrão 30).
    :param max_retries: novas tentativas em falha transitória (429, 502, 503, 504, rede), só em leituras.
    :param app_info: complemento do User-Agent para identificar a sua aplicação (ex.: ``"minha-app/1.2"``).
    :param transport: transporte HTTP alternativo (testes, proxies corporativos).
    """

    def __init__(self, api_key: Optional[str] = None, *, base_url: str = DEFAULT_BASE_URL, timeout: float = 30.0,
                 max_retries: int = 2, app_info: Optional[str] = None, transport: Optional[Transport] = None):
        key = (api_key if api_key is not None else os.environ.get("NEXTAPI_KEY", "")).strip()
        if not key:
            raise NextApiAuthenticationError("Chave de API não informada: passe api_key ou defina NEXTAPI_KEY.")
        self.__api_key = key
        self.environment = "sandbox" if key.startswith("nxa_test_") else "production"
        self.base_url = _check_base_url(base_url)
        self.timeout = timeout
        self.max_retries = max(0, int(max_retries))
        self._transport = transport or UrllibTransport()
        app = sanitize_app_info(app_info)
        runtime = f"python/{platform.python_version()}"
        ua = f"nextapi-python/{_version.VERSION} {runtime}"
        self._user_agent = f"{ua} {app}" if app else ua
        self._client_info = f"{runtime}; {_os_name(sys.platform)}" + (f"; {app}" if app else "")

        self.cnpj = Cnpj(self)
        self.socios = Socios(self)
        self.ceps = Ceps(self)
        self.empresas = Empresas(self)
        self.cnaes = Cnaes(self)
        self.estados = Estados(self)
        self.municipios = Municipios(self)
        self.mercado = Mercado(self)
        self.creditos = Creditos(self)

    def __repr__(self) -> str:  # nunca mostra a chave
        return f"NextApiClient(base_url={self.base_url!r}, environment={self.environment!r})"

    def _request(self, method: str, path: str, body: Any = None) -> Any:
        url = self.base_url + path
        headers = {
            "Authorization": f"Bearer {self.__api_key}",
            "Accept": "application/json",
            "User-Agent": self._user_agent,
            "X-NextApi-Client": f"python/{_version.VERSION}",
            "X-NextApi-Client-Info": self._client_info,
        }
        payload = None
        if body is not None:
            headers["Content-Type"] = "application/json"
            payload = json.dumps(body).encode("utf-8")
        # POST de lote consome créditos: nunca repete sozinho.
        retries = self.max_retries if method == "GET" else 0

        attempt = 0
        while True:
            try:
                response = self._transport(method, url, headers, payload, self.timeout)
            except OSError as error:  # URLError, timeout, conexão recusada, TLS
                if attempt < retries:
                    attempt += 1
                    time.sleep(_backoff(attempt))
                    continue
                reason = getattr(error, "reason", error)
                raise NextApiConnectionError(f"Falha de conexão com a NextAPI: {reason}", body=error) from None

            if 200 <= response.status < 300:
                return json.loads(response.body) if response.body else None
            if 300 <= response.status < 400:
                raise NextApiConnectionError(
                    f"A NextAPI respondeu com redirecionamento ({response.status}); o SDK não o segue para não "
                    "reenviar a chave.", status=response.status)

            wait = _retry_after(response.headers.get("retry-after"))
            if response.status in _RETRYABLE and attempt < retries:
                attempt += 1
                time.sleep(wait if wait is not None else _backoff(attempt))
                continue
            raise _to_error(response, wait)


def _to_error(response, wait):
    text = response.body.decode("utf-8", errors="replace")
    try:
        body = json.loads(text) if text else None
    except ValueError:
        body = text
    fields = body if isinstance(body, dict) else {}
    code = fields.get("code") if isinstance(fields.get("code"), int) else None
    message = fields.get("message") if isinstance(fields.get("message"), str) and fields.get("message") else None
    cls = error_class(response.status, code)
    return cls(message or f"HTTP {response.status}", status=response.status, code=code, body=body,
               request_id=response.headers.get("x-request-id"), retry_after=wait)


def _check_base_url(raw: str) -> str:
    parts = urlsplit(raw)
    if not parts.scheme or not parts.hostname:
        raise ValueError(f"base_url inválida: {raw}")
    if parts.scheme != "https" and not (parts.scheme == "http" and parts.hostname in _LOCAL):
        raise ValueError("base_url tem de usar https (http só para localhost): a chave vai no cabeçalho.")
    return f"{parts.scheme}://{parts.netloc}{parts.path.rstrip('/')}"


def _backoff(attempt: int) -> float:
    base = min(8.0, 0.5 * 2 ** (attempt - 1))
    return base / 2 + random.random() * base / 2


def _retry_after(header: Optional[str]) -> Optional[float]:
    if not header:
        return None
    try:
        seconds = float(header)
    except ValueError:
        try:
            seconds = parsedate_to_datetime(header).timestamp() - time.time()
        except (TypeError, ValueError):
            return None
    return min(max(seconds, 0.0), 60.0)


NextApi = NextApiClient


def sanitize_app_info(info):
    """Só caracteres seguros num cabeçalho: CR/LF ou espaço no app_info quebrariam a requisição."""
    return re.sub(r"[^A-Za-z0-9._/@+-]", "", info or "")[:64]


def _os_name(name):
    if name.startswith("win"):
        return "windows"
    if name.startswith("linux"):
        return "linux"
    return "darwin" if name == "darwin" else "other"
