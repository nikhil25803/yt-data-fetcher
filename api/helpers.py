import requests, os
from dotenv import load_dotenv
from datetime import datetime
from django.utils.timezone import make_aware
from .models import VideoDataModel

# Load environment variables
load_dotenv()


class FetchAPIData:
    """
    Fetch data from YouTube Data API (v3) according to a search query.\n
    Example: \n
    ```python
    api_data = FetchAPIData(query="python")
    api_data.get_query_data()
    ```
    """

    def __init__(self, query="python") -> None:
        self.query = query
        self.url = "https://www.googleapis.com/youtube/v3/search"
        self.obj_list = []

    def get_query_data(self):
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
                    # Create a new object for each record
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

                # Update object list attribute
                self.obj_list = response_data

                # Serve the response with response data
                response = {
                    "success": True,
                    "message": "Successfully fetched API data",
                }

                return response
        except Exception as e:
            response = {
                "success": False,
                "message": f"Raised exception while fetching API data.\nException: {e}",
            }
            return response

    def load_data_in_db(self):
        try:
            # Create a new object
            if len(self.obj_list) == 0:
                return False
            for obj in self.obj_list:
                # Format time in required format
                published_time = datetime.strptime(
                    obj["publishedAt"], "%Y-%m-%dT%H:%M:%SZ"
                )

                # Convert naive datetime to aware datetime
                published_time_aware = make_aware(published_time)

                # Try adding a object to the DB, if fails, skip to next object
                try:
                    # Create new object
                    new_data = VideoDataModel.objects.create(
                        videoId=obj["videoId"],
                        publishedAt=published_time_aware,
                        channelId=obj["channelId"],
                        videoTitle=obj["videoTitle"],
                        videoDescription=obj["videoDescription"],
                        thumbnailUrl=obj["thumbnailUrl"],
                        channelTitle=obj["channelTitle"],
                    )

                    # Save the object
                    new_data.save()

                except Exception:
                    continue

            return True
        except Exception as e:
            print(f"Raised exception while loading data in the DB.\nExeption: {e}")
            return False

    def __del__(self) -> None:
        pass
