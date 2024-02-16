from rest_framework.decorators import api_view
from django.http import JsonResponse
from .helpers import FetchAPIData


# Ping Test
async def index(request):

    return JsonResponse(data={"message": "API is up and running!"})


# API to GET query data
@api_view(http_method_names=["GET"])
def get_data(request):
    api_data = FetchAPIData(query="python")

    # Get API response
    api_response = api_data.get_query_data()
    if api_response["success"] == False:
        return JsonResponse(
            data={"message": "Unable to fetch API data from the database"}
        )

    # If response received from the API - add the records in the databse
    db_response = api_data.load_data_in_db()

    # Destroy the object
    del api_data

    if db_response == False:
        return JsonResponse(data={"message": "Unable to add records in the DB"})

    return JsonResponse(data={"message": "Successfully added the data in the DB"})
