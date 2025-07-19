from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE , related_name='profile')
    bio = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return self.user.username
    
class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.title
    
class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Movie(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField(null=True)
    rating = models.DecimalField(max_digits=3 , decimal_places=1)
    launch_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category , on_delete= models.CASCADE)
    is_favorite = models.BooleanField(default=False)
    owner = models.ForeignKey(User , on_delete=models.CASCADE)

    def __str__(self):
        return self.name   

class Comment(models.Model):
    review = models.TextField()
    is_like = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie , on_delete=models.CASCADE , null=True)

    def __str__(self):
        return self.review
    
class SaveMovie(models.Model):
    movie = models.ForeignKey(Movie , on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.movie.name
    
