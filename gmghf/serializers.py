from rest_framework import serializers
from .models import *



class GMGHFProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = GMGHFProgram
        fields = '__all__'



class GMGHFPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = GMGHFPicture
        fields = '__all__'

    def validate_image(self, value):
        max_size = 1 * 1024 * 1024  # 1MB in bytes
        if value.size > max_size:
            raise serializers.ValidationError("Image file size must not exceed 1.0MB.")
        
        # Check that the uploaded file is an image
        if not value.content_type.startswith('image/'):
            raise serializers.ValidationError("Uploaded file must be an image.")
        
        return value


class GMGHFVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GMGHFVideo
        fields = '__all__'

    def validate_video(self, value):
        max_size = 1 * 1024 * 1024  # 2MB in bytes
        if value.size > max_size:
            raise serializers.ValidationError("Video file size must not exceed 1.0MB.")
        
        # Check that the uploaded file is a video
        if not value.content_type.startswith('video/'):
            raise serializers.ValidationError("Uploaded file must be a video.")
        
        return value




