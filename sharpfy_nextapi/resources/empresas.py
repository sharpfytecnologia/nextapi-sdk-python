from datetime import date
from typing import Optional, Union

from sharpfy_nextapi._validation import query
from sharpfy_nextapi.models import CnpjSimplifiedResponse, Page
from sharpfy_nextapi.resources.base import Resource


class Empresas(Resource):
    def pesquisar(self, *, q: Optional[str] = None, uf: Optional[str] = None, codigo_municipio: Optional[str] = None,
                  cnpj_raiz: Optional[str] = None, cnpj: Optional[str] = None,
                  data_abertura_inicio: Union[date, str, None] = None, data_abertura_fim: Union[date, str, None] = None,
                  codigo_situacao_cadastral: Optional[str] = None, ceps: Optional[str] = None,
                  cnaes: Optional[str] = None, page: Optional[int] = None,
                  page_size: Optional[int] = None) -> "Page[CnpjSimplifiedResponse]":
        """Pesquisa de empresas por filtros. ``ceps`` e ``cnaes`` aceitam vários valores separados por vírgula."""
        return self._get("/v1/empresas" + query({
            "q": q, "uf": uf, "codigoMunicipio": codigo_municipio, "cnpjRaiz": cnpj_raiz, "cnpj": cnpj,
            "dataAberturaInicio": data_abertura_inicio, "dataAberturaFim": data_abertura_fim,
            "codigoSituacaoCadastral": codigo_situacao_cadastral, "ceps": ceps, "cnaes": cnaes, "page": page,
            "pageSize": page_size}))
