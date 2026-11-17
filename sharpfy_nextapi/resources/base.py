from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from sharpfy_nextapi.client import NextApiClient


class Resource:
    def __init__(self, client: "NextApiClient"):
        self._client = client

    def _get(self, path: str):
        return self._client._request("GET", path)

    def _post(self, path: str, body):
        return self._client._request("POST", path, body)
