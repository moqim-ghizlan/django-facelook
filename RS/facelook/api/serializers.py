from rest_framework.serializers import ModelSerializer
from ..models import Post, Like, Fallowing, User, Topic




class Topics_serialized(ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


class Post_serialized(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class User_serialized(ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'bio'
        ]