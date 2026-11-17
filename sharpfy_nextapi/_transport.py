"""Transporte HTTP sobre a biblioteca padrão (urllib), sem dependências."""
import ssl
import urllib.error
import urllib.request
from typing import Dict, Mapping, NamedTuple, Optional, Protocol


class Response(NamedTuple):
    status: int
    headers: Mapping[str, str]
    body: bytes


class Transport(Protocol):
    """Faz uma requisição e devolve a resposta, seja qual for o status. Erros de rede viram exceção (OSError)."""

    def __call__(self, method: str, url: str, headers: Dict[str, str], body: Optional[bytes],
                 timeout: float) -> Response: ...


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    # urllib manda o cabeçalho Authorization junto para o destino do redirecionamento: não seguir.
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class UrllibTransport:
    def __init__(self, ssl_context: Optional[ssl.SSLContext] = None):
        context = ssl_context or ssl.create_default_context()
        self._opener = urllib.request.build_opener(_NoRedirect(), urllib.request.HTTPSHandler(context=context))

    def __call__(self, method, url, headers, body, timeout):
        request = urllib.request.Request(url, data=body, headers=headers, method=method)
        try:
            with self._opener.open(request, timeout=timeout) as response:
                return Response(response.status, {k.lower(): v for k, v in response.headers.items()}, response.read())
        except urllib.error.HTTPError as error:  # status >= 400 e redirecionamentos não seguidos
            with error:
                payload = error.read()
            return Response(error.code, {k.lower(): v for k, v in (error.headers or {}).items()}, payload)
