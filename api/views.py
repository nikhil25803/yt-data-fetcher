from rest_framework.decorators import api_view
from django.http import JsonResponse
from .helpers import FetchAPIData
from .models import VideoDataModel
from rest_framework.pagination import PageNumberPagination
from .serializers import VideosDataResponse, AddNewKeySerializer


# Ping Test
async def index(request):
    return JsonResponse(data={"message": "API is up and running!"})


# API to GET query data
@api_view(http_method_names=["GET"])
def load_data(request):
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


@api_view(http_method_names=["GET"])
def get_all_videos(request):
    # Get the query parameter for limit (data per page)
    query_param = request.GET.get("limit")
    PAGE_SIZE = (
        int(query_param)
        if isinstance(query_param, int) and int(query_param) > 0
        else 10
    )

    # Fetch all the data from the model
    videos_data = VideoDataModel.objects.all().values()

    # Paginate the data
    paginator = PageNumberPagination()
    paginator.page_size = PAGE_SIZE
    paginated_data = paginator.paginate_queryset(videos_data, request)

    # Serialize the data
    serialized_data = VideosDataResponse(paginated_data, many=True)

    # If serialized data is valid
    if serialized_data:
        return JsonResponse(
            data={
                "message": "All videos has been fetched",
                "totalCount": paginator.page.paginator.count,
                "pageCount": PAGE_SIZE,
                "next": paginator.get_next_link(),
                "previous": paginator.get_previous_link(),
                "data": serialized_data.data,
            }
        )

    return JsonResponse(
        data={
            "message": f"All video has been fetched.\nError: {serialized_data.error_messages}",
            "data": [],
        }
    )


@api_view(http_method_names=["POST"])
def add_new_key(request):
    incoming_data = request.data
    validate_data = AddNewKeySerializer(data=incoming_data)
    if validate_data.is_valid(raise_exception=True):
        validate_data.save()
        return JsonResponse(
            data={"message": "API key has been added.", "data": validate_data.data}
        )

    return JsonResponse(
        data={
            "message": f"Unable to add new key.\nError: {validate_data.error_messages}",
        }
    )
