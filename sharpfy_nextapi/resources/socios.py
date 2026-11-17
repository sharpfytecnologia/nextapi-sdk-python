from typing import Optional

from sharpfy_nextapi._validation import normalize_hash_socio, query
from sharpfy_nextapi.models import SocioEmpresasResponse
from sharpfy_nextapi.resources.base import Resource


class Socios(Resource):
    def listar_empresas(self, hash_socio: str, *, page: Optional[int] = None, page_size: Optional[int] = None,
                        incluir_inativas: Optional[bool] = None) -> SocioEmpresasResponse:
        """Empresas do sócio. O hash vem de ``obter_relacionamentos`` (``socios[].hashSocio``); com
        ``socio.vinculoVerificavel`` falso ele é provisório: não guarde."""
        qs = query({"page": page, "pageSize": page_size, "incluirInativas": incluir_inativas})
        return self._get(f"/v1/socios/{normalize_hash_socio(hash_socio)}/empresas" + qs)
