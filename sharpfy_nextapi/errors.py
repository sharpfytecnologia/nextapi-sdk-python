"""Erros do SDK. Toda falha da API vira um :class:`NextApiError`; a subclasse diz o que fazer.

O código numérico da API (``code``) distingue casos com o mesmo status HTTP: 405 vale tanto para
"sem créditos" (1004, 1006) quanto para "plano pago obrigatório" (1012, 1005).
"""
from typing import Any, Optional


class ErrorCodes:
    NOT_FOUND = 1000
    TOKEN_NOT_PROVIDED = 1001
    TOKEN_INVALID = 1002
    TOO_MANY_REQUESTS = 1003
    MISSING_CREDITS = 1004
    LIVE_SEARCH_NOT_ALLOWED = 1005
    LIVE_SEARCH_MISSING_CREDITS = 1006
    INVALID_CEP = 1007
    REQUIRES_PAID_PLAN = 1012
    EXTERNAL_PROVIDER_FAILURE = 1014
    SANDBOX_DAILY_LIMIT = 1015
    SANDBOX_DISABLED = 1016


class NextApiError(Exception):
    """Falha numa chamada à NextAPI.

    :ivar status: status HTTP (0 quando a requisição nem chegou à API).
    :ivar code: código de erro da NextAPI (ver :class:`ErrorCodes`), quando informado.
    :ivar body: corpo da resposta de erro (JSON interpretado, ou o texto).
    :ivar request_id: cabeçalho ``x-request-id``, para o suporte.
    """

    def __init__(self, message: str, status: int = 0, code: Optional[int] = None, body: Any = None,
                 request_id: Optional[str] = None, retry_after: Optional[float] = None):
        super().__init__(message)
        self.message = message
        self.status = status
        self.code = code
        self.body = body
        self.request_id = request_id
        self.retry_after = retry_after

    def __repr__(self) -> str:
        return f"{type(self).__name__}(status={self.status}, code={self.code}, message={self.message!r})"


class NextApiAuthenticationError(NextApiError):
    """Chave ausente, inválida ou revogada."""


class NextApiInsufficientCreditsError(NextApiError):
    """Sem créditos para a consulta (1004, 1006)."""


class NextApiPaidPlanRequiredError(NextApiError):
    """O recurso exige plano pago ou créditos avulsos (1012, 1005)."""


class NextApiNotFoundError(NextApiError):
    """O CNPJ, CEP ou sócio pesquisado não existe (404)."""


class NextApiValidationError(NextApiError, ValueError):
    """Parâmetro rejeitado pela API (400) ou pelo próprio SDK antes de enviar (status 0)."""


class NextApiRateLimitError(NextApiError):
    """Limite de requisições do plano ou do sandbox (429). ``retry_after`` em segundos."""


class NextApiServerError(NextApiError):
    """Falha do lado da API (5xx), inclusive a do provedor em tempo real (1014)."""


class NextApiConnectionError(NextApiError):
    """Não houve resposta: rede, DNS, TLS, tempo esgotado ou redirecionamento recusado."""


_BY_CODE = {
    ErrorCodes.TOKEN_NOT_PROVIDED: NextApiAuthenticationError,
    ErrorCodes.TOKEN_INVALID: NextApiAuthenticationError,
    ErrorCodes.SANDBOX_DISABLED: NextApiAuthenticationError,
    ErrorCodes.MISSING_CREDITS: NextApiInsufficientCreditsError,
    ErrorCodes.LIVE_SEARCH_MISSING_CREDITS: NextApiInsufficientCreditsError,
    ErrorCodes.REQUIRES_PAID_PLAN: NextApiPaidPlanRequiredError,
    ErrorCodes.LIVE_SEARCH_NOT_ALLOWED: NextApiPaidPlanRequiredError,
}


def error_class(status: int, code: Optional[int]) -> type:
    if code in _BY_CODE:
        return _BY_CODE[code]
    if status in (401, 403):
        return NextApiAuthenticationError
    if status == 404:
        return NextApiNotFoundError
    if status == 429:
        return NextApiRateLimitError
    if status >= 500:
        return NextApiServerError
    if status in (400, 422):
        return NextApiValidationError
    return NextApiError
