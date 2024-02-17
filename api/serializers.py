from rest_framework import serializers
from .models import VideoDataModel
from .models import APIKeysModel


"""Videos Data Response Serializer"""


class VideosDataResponse(serializers.ModelSerializer):
    class Meta:
        model = VideoDataModel
        exclude = ["id", "videoId", "channelId"]


class AddNewKeySerializer(serializers.Serializer):
    key_name = serializers.CharField()
    key_value = serializers.CharField()

    def validate(self, data):
        key_name = data["key_name"]
        key_check = APIKeysModel.objects.filter(key_name=key_name).exists()
        if key_check:
            raise serializers.ValidationError(
                detail="A key with the given name already exists."
            )

        return data

    def create(self, data):
        # Encrypt the data

        new_key = APIKeysModel.objects.create(
            key_name=data["key_name"], key_value=data["key_value"]
        )

        new_key.save()

        return new_key
