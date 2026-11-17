from typing import Iterable, List, Optional

from sharpfy_nextapi._validation import batch, normalize_cnpj, query
from sharpfy_nextapi.models import (CnpjConformidadeResponse, CnpjInscricaoEstadualResponse, CnpjItemResponse,
                                    CnpjRelacionamentoResponse, CnpjSimplesResponse)
from sharpfy_nextapi.resources.base import Resource


class Cnpj(Resource):
    """Consultas por CNPJ, com ou sem pontuação, numérico ou alfanumérico."""

    def consultar(self, cnpj: str, *, tolerance_days: Optional[int] = None) -> CnpjItemResponse:
        """Dados cadastrais do estabelecimento (1 crédito).

        :param tolerance_days: idade máxima aceita do dado em cache, em dias (0 a 45). 0 força a consulta em tempo real.
        """
        return self._get(f"/v1/cnpj/{normalize_cnpj(cnpj)}" + query({"toleranceDays": tolerance_days}))

    def consultar_ao_vivo(self, cnpj: str) -> CnpjItemResponse:
        """``consultar`` com ``tolerance_days=0``: consulta em tempo real ao provedor (exige plano que permita)."""
        return self.consultar(cnpj, tolerance_days=0)

    def obter_simples(self, cnpj: str, *, tolerance_days: Optional[int] = None) -> CnpjSimplesResponse:
        """Situação no Simples Nacional e no MEI."""
        return self._get(f"/v1/cnpj/{normalize_cnpj(cnpj)}/simples" + query({"toleranceDays": tolerance_days}))

    def obter_inscricoes_estaduais(self, cnpj: str) -> List[CnpjInscricaoEstadualResponse]:
        """Inscrições estaduais do estabelecimento, uma por UF."""
        return self._get(f"/v1/cnpj/{normalize_cnpj(cnpj)}/ie")

    def obter_conformidade(self, cnpj: str) -> CnpjConformidadeResponse:
        """Sanções (CEIS, CNEP, CEPIM) e dívida ativa da União. Planos pagos ou créditos avulsos."""
        return self._get(f"/v1/cnpj/{normalize_cnpj(cnpj)}/conformidade")

    def obter_relacionamentos(self, cnpj: str, *, page: Optional[int] = None, page_size: Optional[int] = None,
                              incluir_inativas: Optional[bool] = None) -> CnpjRelacionamentoResponse:
        """Sócios e empresas ligadas pelos mesmos sócios (grupo econômico), paginado."""
        qs = query({"page": page, "pageSize": page_size, "incluirInativas": incluir_inativas})
        return self._get(f"/v1/cnpj/{normalize_cnpj(cnpj)}/relacionamentos" + qs)

    def consultar_lote(self, cnpjs: Iterable[str]) -> List[CnpjItemResponse]:
        """Até 100 CNPJs numa chamada; 1 crédito por CNPJ encontrado. Não é repetida automaticamente em falha."""
        return self._post("/v1/cnpj/batch", {"cnpjs": batch(cnpjs)})

    def obter_simples_lote(self, cnpjs: Iterable[str]) -> List[CnpjSimplesResponse]:
        """Simples Nacional de até 100 CNPJs numa chamada. Não é repetida automaticamente em falha."""
        return self._post("/v1/cnpj/batch/simples", {"cnpjs": batch(cnpjs)})
