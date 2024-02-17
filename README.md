# YT Data Fetcher

Server-side script to fetch the latest videos using YouTube API. The script will continuously be called in the background (async) with some interval (say 10 seconds) for fetching the latest videos for a predefined search query

## Project Setup

- Clone the repository

```bash
git clone https://github.com/nikhil25803/yt-data-fetcher.git
```

```bash
cd yt-data-fetcher
```

- Virtual Environment Setup

```bash
python -m venv env

source env/Scripts/Activate
```

- Download Requirements

```bash
pip install -r requirements.txt
```

- Environment Variables Requirements

```.env
DJANG_SECRET_KEY=...
GOOGLE_API_KEY=...
GCP_CLIENT_ID=...
GCP_CLIENT_SECRET=...
KEYWORD=...
```

- Make migrations (For DB functionality)

```bash
python manage.py makemigrations

python manage.py migrate
```

- Run the server

```bash
python manage.py runserver
```

### API Reference

- **GET** `/api/data`
  - This endpoint will add data latest fetched YouTube video data of the keyword mentioned.
  - "cricket" by default

Response

```js
{
    "message": "Successfully added the data in the DB"
}
```

- **GET** `/api/videos`
  - This endpoint will return the data in paginated form (one can set the limit per-response)
  - Query params
    - `limit`
    - `page`
    - Example - `/api/videos?limit=2&page=2`

Respose

```js
{
    "message": "All videos has been fetched",
    "totalCount": 25,
    "pageCount": 10,
    "next": "http://127.0.0.1:8000/api/videos?limit=2&page=2",
    "previous": null,
    "data": [
        {
            "publishedAt": "2024-02-16T20:49:02Z",
            "videoTitle": "The Importance of Python For IT Specialists | Google IT Support Certificate",
            "videoDescription": "Python is still important in today's IT industry. Python has been adopted drastically in the last few years because its language has ...",
            "thumbnailUrl": "https://i.ytimg.com/vi/RgcEylkiaXE/default.jpg",
            "channelTitle": "Google Career Certificates"
        },
        ...
    ]
}
```

- **POST** `api/key/add`
  - Add new API key to the DB
  - This key will be used when the currently provided key will get expired or failed for any reason

Response

```js
{
    "message": "API key has been added.",
    "data": {
        "key_name": "...",
        "key_value": "..."
    }
}
```
