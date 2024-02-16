from .helpers import FetchAPIData
from apscheduler.schedulers.background import BackgroundScheduler


# Create a function that will called to fetch Data
def schedule_data_fetching():
    api_data = FetchAPIData(query="rust")

    # Get API response
    api_response = api_data.get_query_data()
    if api_response["success"] == False:
        print("Unable to fetch API data from the database")

    # If response received from the API - add the records in the databse
    db_response = api_data.load_data_in_db()
    if db_response == False:
        print("Unable to add records in the DB")

    # Destroy the object
    del api_data
    print("Added new records in the DB")


# Updater function to schedule JOBS
def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(schedule_data_fetching, "interval", seconds=10)
    scheduler.start()
