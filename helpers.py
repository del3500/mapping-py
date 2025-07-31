from typing import List, TypedDict, Any
from urllib.parse import urlencode
import aiohttp
import asyncio


class Coordinate(TypedDict):
    lat: float
    lon: float


# Sample data
coordinates: list[Coordinate] = [
    {"lat": 29.819211, "lon": -95.420002},
    {"lat": 29.818516, "lon": -95.420425},
]

# Additional params
params: dict[str, str] = {"format": "json", "zoom": 10}


async def fetch_json(session: aiohttp.ClientSession, url: str) -> Any:
    try:
        async with session.get(url) as response:
            response.raise_for_status()  # raise for HTTP errors
            return await response.json()
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return None


async def fetch_all(urls: list[str]) -> list[Any]:
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_json(session, url) for url in urls]
        return await asyncio.gather(*tasks)


def build_reverse_geocode_urls(
    coords: list[Coordinate], params: dict[str, str]
) -> List[str]:
    base_url = "https://nominatim.openstreetmap.org/reverse"
    urls: list[str] = []

    for coord in coords:
        query_params = {**coord, **params}  # merge coord and param
        query_string = urlencode(query_params)
        url = f"{base_url}?{query_string}"
        urls.append(url)

    return urls


urls = build_reverse_geocode_urls(coordinates, params)

if __name__ == "__main__":
    results: list[str] = asyncio.run(fetch_all(urls))
    for url, data in zip(urls, results):
        print(f"\n--- JSON response from {url} ---")
        print(data)
