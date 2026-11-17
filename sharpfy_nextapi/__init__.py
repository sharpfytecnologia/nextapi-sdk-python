"""SDK oficial da NextAPI para Python (CNPJ, CEP, sócios, mercado). Sem dependências."""
from sharpfy_nextapi._validation import normalize_cep, normalize_cnpj
from sharpfy_nextapi._version import VERSION as __version__
from sharpfy_nextapi.client import NextApi, NextApiClient
from sharpfy_nextapi.errors import (ErrorCodes, NextApiAuthenticationError, NextApiConnectionError, NextApiError,
                                    NextApiInsufficientCreditsError, NextApiNotFoundError,
                                    NextApiPaidPlanRequiredError, NextApiRateLimitError, NextApiServerError,
                                    NextApiValidationError)

__all__ = [
    "NextApiClient", "NextApi", "ErrorCodes", "NextApiError", "NextApiAuthenticationError",
    "NextApiInsufficientCreditsError", "NextApiPaidPlanRequiredError", "NextApiNotFoundError",
    "NextApiValidationError", "NextApiRateLimitError", "NextApiServerError", "NextApiConnectionError",
    "normalize_cnpj", "normalize_cep", "__version__",
]
