import requests, os, json
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


class FetchAPIData:
    """
    Fetch data from YouTube Data API (v3) according to a search query.\n
    Example: \n
    ```python
    api_data = FetchAPIData(query="python")
    api_data.get_search_data()
    ```
    """

    def __init__(self, query) -> None:
        self.query = query
        self.url = "https://www.googleapis.com/youtube/v3/search"

    async def get_search_data(self):
        query_params = {
            "key": os.getenv("GOOGLE_API_KEY"),
            "q": self.query,
            "type": "video",
            "order": "date",
            "part": "snippet",
        }

        response_data = []
        try:
            request_response = requests.get(url=self.url, params=query_params)
            if request_response.status_code == 200:

                # Get the response data in JSON format
                json_response = request_response.json()

                for _obj in json_response["items"]:
                    new_obj = {
                        "videoId": _obj["id"]["videoId"],
                        "publishedAt": _obj["snippet"]["publishedAt"],
                        "channelId": _obj["snippet"]["channelId"],
                        "videoTitle": _obj["snippet"]["title"],
                        "videoDescription": _obj["snippet"]["description"],
                        "thumbnailUrl": _obj["snippet"]["thumbnails"]["default"]["url"],
                        "channelTitle": _obj["snippet"]["channelTitle"],
                    }
                    response_data.append(new_obj)

                # Serve the response with response data
                response = {
                    "success": True,
                    "message": "Successfully fetched API data",
                    "data": response_data,
                }
        except Exception as e:
            response = {
                "success": False,
                "message": f"Raised exception while fetching API data.\nException: {e}",
                "data": response_data,
            }
            return response

    def __del__(self) -> None:
        pass
