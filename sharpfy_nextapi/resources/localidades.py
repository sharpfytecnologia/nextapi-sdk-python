from typing import Optional

from sharpfy_nextapi._validation import positive_int, query
from sharpfy_nextapi.models import (CnaeItemResponse, EstadoItemResponse, MunicipioDetalhadoResponse,
                                    MunicipioItemResponse, Page)
from sharpfy_nextapi.resources.base import Resource


class Cnaes(Resource):
    def listar(self, *, page: Optional[int] = None, page_size: Optional[int] = None) -> "Page[CnaeItemResponse]":
        return self._get("/v1/cnaes" + query({"page": page, "pageSize": page_size}))


class Estados(Resource):
    def listar(self, *, page: Optional[int] = None, page_size: Optional[int] = None) -> "Page[EstadoItemResponse]":
        return self._get("/v1/estados" + query({"page": page, "pageSize": page_size}))


class Municipios(Resource):
    def listar(self, *, uf: Optional[str] = None, page: Optional[int] = None,
               page_size: Optional[int] = None) -> "Page[MunicipioItemResponse]":
        return self._get("/v1/municipios" + query({"uf": uf, "page": page, "pageSize": page_size}))

    def obter_por_id(self, id: int) -> MunicipioDetalhadoResponse:
        """Município pelo código da Receita (o ``id`` de ``listar``), com a hierarquia do IBGE."""
        return self._get(f"/v1/municipios/{positive_int(id, 'id')}")
