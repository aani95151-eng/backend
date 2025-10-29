from rest_framework import serializers
from .models import Blog

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['uid', 'title', 'Blog_text', 'main_image', 'user', 'created_at', 'updated_at']
        # OR use exclude, but NOT both
        # exclude = ['created_at', 'updated_at']
        read_only_fields = ['uid', 'user']  