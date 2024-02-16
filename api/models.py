from django.db import models

"""Video Data Models"""


class VideoDataModel(models.Model):
    videoId = models.CharField(max_length=100, unique=True)
    publishedAt = models.DateTimeField()
    channelId = models.CharField(max_length=100)
    videoTitle = models.CharField(max_length=2500)
    videoDescription = models.CharField(max_length=5000)
    thumbnailUrl = models.CharField(max_length=250)
    channelTitle = models.CharField(max_length=250)

    def __str__(self) -> str:
        return f"Video ID: {self.videoId}"
