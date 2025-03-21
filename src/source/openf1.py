from typing import Dict, Any, Optional
from source.base.baseapi import BaseAPI

class OpenF1(BaseAPI):
    def __init__(self):
        base_url = "https://api.openf1.org/v1"
        headers = {"Content-Type": f"application/json"}
        super().__init__(base_url, headers)

    def session_list(self, year: int, type: str) -> Any:
        return self._get("sessions", {"year": year, "session_type": type})

    def driver_list(self, session: int) -> Any:
        return self._get("drivers", {"session_key": session})

    def get(self, endpoint: str, params: Dict[str, Any]) -> Any:
        return self._get(f"{endpoint}", params)