from rest_framework import serializers
from .models import Note , Movie , Profile , Comment , SaveMovie , Category

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'created_at', 'updated_at']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id' , 'name']

class MovieSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Movie
        fields = ['id', 'name', 'image', 'rating', 'launch_date', 'is_favorite', 'owner_username', 'category']


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source = 'user.username', read_only = True)

    class Meta:
        model = Profile
        fields = ['id' , 'username' , 'profile_picture' , 'bio']

class CommentSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source = 'owner.username' , read_only = True)
    movie_name = serializers.CharField(source = 'movie.name' , read_only = True)
    movie_id = serializers.CharField(source = 'movie.id' , read_only = True)
    class Meta:
        model = Comment
        fields = ['id', 'movie_id' , 'movie_name' ,  'review' , 'is_like' , 'owner_username']

class SaveMovieSerializer(serializers.ModelSerializer):
    movie_name = serializers.CharField(source = 'movie.name' , read_only = True)
    movie_rating  = serializers.DecimalField(source = 'movie.rating' , read_only = True , max_digits=3 , decimal_places=1)
    movie_id = serializers.CharField(source = 'movie.id' , read_only = True)
    movie_category = serializers.CharField(source = 'movie.category.name' , read_only = True)
    class Meta:
        model = SaveMovie
        fields = ['id' ,  'movie_name' , 'movie_rating' , 'movie_id', 'movie_category' ,  'saved_at']