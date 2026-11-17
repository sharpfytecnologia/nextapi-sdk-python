from sharpfy_nextapi.models import WorkspaceCreditsResponse
from sharpfy_nextapi.resources.base import Resource


class Creditos(Resource):
    def consultar(self) -> WorkspaceCreditsResponse:
        """Saldo de créditos do plano e avulsos, e os limites da chave. Não consome crédito."""
        return self._get("/v1/credits")
