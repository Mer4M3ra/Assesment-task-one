
import requests
import time
from typing import Dict, List, Optional, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MCTiersAPI:
    """Client for interacting with the MCTiers API v2"""
    
    BASE_URL = "https://mctiers.com/api/v2"
    TIMEOUT = 10
    
    def __init__(self):
        """Initialize the API client"""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'MCTiers-Data-App/1.0'
        })
        self.last_request_time = 0
        self.min_request_interval = 0.1
    
    def _rate_limit(self):
        """Implement rate limiting"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)
        self.last_request_time = time.time()
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """Make a request to the API"""
        self._rate_limit()
        url = f"{self.BASE_URL}/{endpoint}"
        
        try:
            logger.info(f"Request: {url}")
            response = self.session.get(url, params=params, timeout=self.TIMEOUT)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.Timeout:
            logger.error("Request timeout")
            return {"error": "Request timed out"}
            
        except requests.exceptions.ConnectionError:
            logger.error("Connection error")
            return {"error": "Cannot connect to API"}
            
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                return {"error": "Resource not found"}
            elif response.status_code == 400:
                return {"error": "Invalid request"}
            else:
                return {"error": f"API error: {response.status_code}"}
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            return {"error": f"Request failed: {str(e)}"}
            
        except ValueError as e:
            logger.error(f"Invalid JSON: {e}")
            return {"error": "Invalid response"}
    
    def get_gamemodes(self) -> Optional[Dict]:
        """Get all gamemodes"""
        return self._make_request("mode/list")
    
    def get_overall_rankings(self, count: int = 10, from_index: int = 0) -> Optional[List]:
        """Get overall rankings"""
        params = {"count": min(count, 50), "from": from_index}
        return self._make_request("mode/overall", params)
    
    def get_gamemode_rankings(self, gamemode: str, count: int = 10, from_index: int = 0) -> Optional[Dict]:
        """Get rankings for a specific gamemode"""
        params = {"count": min(count, 50), "from": from_index}
        return self._make_request(f"mode/{gamemode}", params)
    
    def get_player_profile(self, uuid: str) -> Optional[Dict]:
        """Get player profile by UUID"""
        return self._make_request(f"profile/{uuid}")
    
    def search_player_by_name(self, name: str) -> Optional[Dict]:
        """Search player by username"""
        return self._make_request(f"profile/by-name/{name}")
    
    def search_player_by_discord(self, discord_id: int) -> Optional[Dict]:
        """Search player by Discord ID"""
        return self._make_request(f"profile/by-discord/{discord_id}")
    
    def get_tester_history(self, uuid: str, gamemode: Optional[str] = None, count: int = 10) -> Optional[List]:
        """Get test history for a player"""
        params = {"count": min(count, 50)}
        if gamemode:
            params["gamemode"] = gamemode
        return self._make_request(f"tests/{uuid}", params)
    
    def get_recent_tests(self, gamemode: Optional[str] = None, count: int = 10) -> Optional[List]:
        """Get recent tests"""
        params = {"count": min(count, 20)}
        if gamemode:
            params["gamemode"] = gamemode
        return self._make_request("tests/recent", params)