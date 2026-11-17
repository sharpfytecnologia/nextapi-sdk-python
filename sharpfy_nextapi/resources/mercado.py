import re
from typing import Optional

from sharpfy_nextapi._validation import path_segment, positive_int, query
from sharpfy_nextapi.models import MercadoCnaeResponse, MercadoIndicadorResponse, MercadoMunicipioResponse
from sharpfy_nextapi.resources.base import Resource


class Mercado(Resource):
    """Dados de mercado agregados. Planos pagos ou créditos avulsos."""

    def obter_cnae(self, cnae: str, *, uf: Optional[str] = None, meses: Optional[int] = None) -> MercadoCnaeResponse:
        """Empresas ativas, aberturas e baixas de um CNAE (com ou sem pontuação), no Brasil ou numa UF."""
        codigo = path_segment(re.sub(r"[\s./-]", "", str(cnae or "")), "cnae")
        return self._get(f"/v1/mercado/cnaes/{codigo}" + query({"uf": uf, "meses": meses}))

    def obter_municipio(self, id: int) -> MercadoMunicipioResponse:
        """Empresas e economia (PIB, população) de um município, pelo código da Receita."""
        return self._get(f"/v1/mercado/municipios/{positive_int(id, 'id')}")

    def obter_indicador(self, tipo: str, *, inicio: Optional[str] = None,
                        fim: Optional[str] = None) -> MercadoIndicadorResponse:
        """Série de um indicador econômico (ex.: ``ipca``), de ``inicio`` a ``fim`` (``AAAAMM``)."""
        return self._get(f"/v1/mercado/indicadores/{path_segment(tipo, 'tipo')}" + query({"inicio": inicio, "fim": fim}))
