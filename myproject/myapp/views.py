from rest_framework import generics, permissions , filters , viewsets
from .models import Note , User , Movie , Profile , Comment , SaveMovie
from .serializers import NoteSerializer , MovieSerializer , UserProfileSerializer , CommentSerializer , SaveMovieSerializer
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import status , decorators
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsOwnerOrReadOnlyOrAdmin

class SignUp(APIView):
    permission_classes = [AllowAny] 
    def post(self , request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if username and password:
            if User.objects.filter(username = username).exists():
                return Response({'message': "Account already created"} , status=status.HTTP_400_BAD_REQUEST)
            
            user  = User.objects.create_user(username = username , email=email , password = password)

            refresh = RefreshToken.for_user(user)

            return Response({
              "message" : "User Created Successfully",
              "access_token" : str(refresh.access_token),
              "refresh_token" : str(refresh),
            } , status=status.HTTP_201_CREATED)
        
        return Response({'message' : 'Fill all require fields'} , status=status.HTTP_400_BAD_REQUEST)
            
class LoginView(APIView):
    permission_classes = [AllowAny] 
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Login successful',
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            }, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
   
#allow functionality to get list and create notes

class NoteListCreate(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['id' , 'title']

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

#allows functionality to updateretrievedelete notes

class NoteRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)



class MovieCreateList(generics.ListCreateAPIView):
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated , IsOwnerOrReadOnlyOrAdmin]
    filter_backends = [DjangoFilterBackend , filters.SearchFilter]
    search_fields = ['name' , 'rating']
    filterset_fields = ['is_favorite'] 

    def get_queryset(self):
        return Movie.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)
    

class MovieRetreiveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated , IsOwnerOrReadOnlyOrAdmin]

    def get_queryset(self):
        return Movie.objects.all()

class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
  
    def get_queryset(self):
        return Profile.objects.filter(user = self.request.user)
    
    def perform_create(self, serializer):
        return serializer.save(user = self.request.user)
    
    @action(detail=False , methods=['get' , 'patch'] , permission_classes=[IsAuthenticated])
    def me(self , request):
        profile , created = Profile.objects.get_or_create(user = request.user)
        if request.method == 'GET':
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        if request.method == 'PATCH':
            serializer = self.get_serializer(profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        
class CommentViewList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        movie_id = self.kwargs.get('movie_id')
        return Comment.objects.filter(movie_id = movie_id)
    
    def perform_create(self, serializer):
        movie_id = self.kwargs.get('movie_id')
        serializer.save(owner=self.request.user, movie_id=movie_id)

class CommentRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
   
    def get_queryset(self):
        movie_id = self.kwargs.get('movie_id')
        return Comment.objects.filter(owner = self.request.user , movie_id = movie_id)
    
class MyCommentsList(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(owner=self.request.user)
    
class SavedMovieList(generics.ListCreateAPIView):
    serializer_class = SaveMovieSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SaveMovie.objects.all()
    
    def perform_create(self, serializer):
        movie_id = self.kwargs.get('movie_id')
        movie = Movie.objects.get(id=movie_id)
        serializer.save(movie=movie)
        
class SavedMovieRetreiveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
   serializer_class = SaveMovieSerializer
   permission_classes = [IsAuthenticated]

   def get_queryset(self):
       return SaveMovie.objects.all()