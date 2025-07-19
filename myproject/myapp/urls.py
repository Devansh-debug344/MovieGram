from django.urls import path
from .views import NoteListCreate, NoteRetrieveUpdateDestroy, LoginView, SignUp , MovieCreateList , MovieRetreiveUpdateDelete , ProfileViewSet , ProfileViewSet , CommentViewList , CommentRetrieveUpdateDelete , MyCommentsList , SavedMovieList , SavedMovieRetreiveUpdateDelete
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('profiles', ProfileViewSet, basename='profiles')

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('notes/', NoteListCreate.as_view(), name='note-list'),
    path('notes/<int:pk>/', NoteRetrieveUpdateDestroy.as_view(), name='note-detail'),
    path('movies/' , MovieCreateList.as_view() , name = 'movie'),
    path('movies/<int:pk>/' , MovieRetreiveUpdateDelete.as_view() , name = 'movie-detail'),
    path('movies/<int:movie_id>/comments/' , CommentViewList.as_view() , name='movie-comments'),
    path('movies/<int:movie_id>/comments/<int:pk>/' , CommentRetrieveUpdateDelete.as_view() , name='movie-comments-edit'),
    path('movies/comments/' , MyCommentsList.as_view() , name='profile-comment'),    
    path('movies/saved/' , SavedMovieList.as_view() , name='save-movie'),    
    path('movies/saved/<int:movie_id>/save/' , SavedMovieList.as_view() , name='save-movie'),    
    path('movies/saved/<int:pk>/' , SavedMovieRetreiveUpdateDelete.as_view() , name='save-movie-update'),    
]
urlpatterns += router.urls
