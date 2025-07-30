import requests
import json
from typing import Dict, Any, Optional

"""
{"verbose":true,"locations":[{"lat":42.358528,"lon":-83.271400},{"lat":42.996613,"lon":-78.749855}],"costing":"bicycle","costing_options":{"bicycle":{"bicycle_type":"road"}},"directions_options":{"units":"miles"},"id":"12abc3afe23984fe"}
"""


def post_lat_lon(
    url: str,
    json_data: Dict[str, Any],
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 10,
) -> requests.Response:
    default_headers = {"Content-Type": "application/json"}
    if headers:
        default_headers.update(headers)

    try:
        response = requests.post(
            url,
            json=json_data,  # automatically serialize to JSON
            headers=default_headers,
            timeout=timeout,
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        raise


def get_street_name(gps: Dict[str, Any]) -> Dict[str, Any]:
    url = "http://localhost:8002/locate"
    response = post_lat_lon(url, gps)
    
    street_names: List[str] = []
    
    for item in response:
        for edge in item.get("edges", []):
            names = edge.get("edge_info", {}).get("names", [])
            street_names.extend(names)

    unique_streets = list(set(street_names))
    return {"streets": unique_streets}



gps = {
    "verbose": True,
    "locations": [{"lat": 29.750022, "lon": -95.373868}],
    #"costing": "bicycle",
    #"costing_options": {"bicycle": {"bicycle_type": "road"}},
    "directions_options": {"units": "feet"},
    "id": "testID",
}

response_data = get_street_name(gps)
print(json.dumps(response_data, indent=2))
