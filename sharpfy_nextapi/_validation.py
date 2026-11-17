"""Normalização e validação das entradas, antes de qualquer requisição."""
import math
import re
from datetime import date
from typing import Any, Dict, Iterable, List, Optional
from urllib.parse import quote, urlencode

from sharpfy_nextapi.errors import NextApiValidationError

_CNPJ = re.compile(r"^[0-9A-Z]{12}[0-9]{2}$")
_CEP = re.compile(r"^[0-9]{8}$")
_HASH = re.compile(r"^[0-9a-fA-F]{20}$")
_SEGMENT = re.compile(r"^[0-9A-Za-z_-]+$")
_STRIP_CNPJ = re.compile(r"[\s./-]")


def _invalid(message: str):
    raise NextApiValidationError(message)


def normalize_cnpj(cnpj: str) -> str:
    """Tira pontuação e põe em maiúsculas. Aceita o CNPJ alfanumérico (12 alfanuméricos e 2 dígitos)."""
    value = _STRIP_CNPJ.sub("", str(cnpj or "")).upper()
    if not _CNPJ.match(value):
        _invalid(f'CNPJ inválido: "{cnpj}". Informe 14 caracteres, com ou sem pontuação.')
    return value


def normalize_cep(cep: str) -> str:
    value = re.sub(r"[\s.-]", "", str(cep or ""))
    if not _CEP.match(value):
        _invalid(f'CEP inválido: "{cep}". Informe 8 dígitos.')
    return value


def normalize_hash_socio(value: str) -> str:
    text = str(value or "").strip()
    if not _HASH.match(text):
        _invalid("hash_socio inválido: são 20 caracteres hexadecimais.")
    return text.lower()


def path_segment(value: Any, name: str) -> str:
    text = str(value if value is not None else "").strip()
    if not _SEGMENT.match(text):
        _invalid(f'{name} inválido: "{value}".')
    return quote(text, safe="")


def positive_int(value: Any, name: str) -> str:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        _invalid(f'{name} inválido: "{value}".')
    return str(value)


def require_positive(value: Any, name: str) -> None:
    if not _number(value) or value <= 0:
        _invalid(f"{name} tem de ser maior que zero.")


def require_range(value: Any, low: float, high: float, name: str) -> None:
    if not _number(value) or not low <= value <= high:
        _invalid(f"{name} tem de estar entre {low:g} e {high:g}.")


def batch(cnpjs: Iterable[str]) -> List[str]:
    if isinstance(cnpjs, (str, bytes)):
        _invalid("Informe uma lista de CNPJs, não um texto.")
    values = list(cnpjs or [])
    if not values:
        _invalid("Informe ao menos um CNPJ.")
    if len(values) > 100:
        _invalid(f"O lote aceita até 100 CNPJs; vieram {len(values)}.")
    return [normalize_cnpj(c) for c in values]


def query(params: Dict[str, Any]) -> str:
    """Query string sem os valores ausentes, na ordem informada; booleanos como true/false."""
    pairs = []
    for key, value in params.items():
        if value is None or value == "":
            continue
        if isinstance(value, bool):
            value = "true" if value else "false"
        elif isinstance(value, date):
            value = value.isoformat()[:10]
        elif isinstance(value, float) and value.is_integer():
            value = int(value)
        pairs.append((key, str(value)))
    return "?" + urlencode(pairs) if pairs else ""


def _number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)
