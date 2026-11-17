from typing import Optional

from sharpfy_nextapi._validation import normalize_cep, query, require_positive, require_range
from sharpfy_nextapi.models import CepItemResponse, Page
from sharpfy_nextapi.resources.base import Resource


class Ceps(Resource):
    def consultar(self, cep: str) -> CepItemResponse:
        """Endereço e coordenadas de um CEP."""
        return self._get(f"/v1/ceps/{normalize_cep(cep)}")

    def buscar(self, *, uf: Optional[str] = None, id_municipio: Optional[int] = None,
               nome_municipio: Optional[str] = None, logradouro: Optional[str] = None, q: Optional[str] = None,
               page: Optional[int] = None, page_size: Optional[int] = None) -> "Page[CepItemResponse]":
        """Busca por UF, município, logradouro ou texto livre (``q``, que não combina com ``logradouro``)."""
        return self._get("/v1/ceps" + query({
            "uf": uf, "idMunicipio": id_municipio, "nomeMunicipio": nome_municipio, "logradouro": logradouro,
            "q": q, "page": page, "pageSize": page_size}))

    def buscar_proximos(self, *, latitude: float, longitude: float, raio_metro: float, page: Optional[int] = None,
                        page_size: Optional[int] = None) -> "Page[CepItemResponse]":
        """CEPs num raio (em metros) ao redor de uma coordenada."""
        require_range(latitude, -90, 90, "latitude")
        require_range(longitude, -180, 180, "longitude")
        require_positive(raio_metro, "raio_metro")
        return self._get("/v1/ceps/geo" + query({
            "latitude": latitude, "longitude": longitude, "raioMetro": raio_metro, "page": page,
            "pageSize": page_size}))

    def buscar_proximos_do_cep(self, cep: str, *, raio_metro: float, page: Optional[int] = None,
                               page_size: Optional[int] = None) -> "Page[CepItemResponse]":
        """CEPs num raio (em metros) ao redor de outro CEP."""
        require_positive(raio_metro, "raio_metro")
        return self._get(f"/v1/ceps/geo/{normalize_cep(cep)}" + query({
            "raioMetro": raio_metro, "page": page, "pageSize": page_size}))
