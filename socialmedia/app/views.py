# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from app.models import User
from app.seriallizer import UserSerializer,UserLoginSerializer

from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import DestroyAPIView



from rest_framework import generics
from rest_framework import status
from app.models import User, Post,PostLike,Comment,UserFollow
from app.seriallizer import PostSerializer,CommentSerializer,PostLikeSerializer,UserFollowSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.core.exceptions import ObjectDoesNotExist


# Testing purpose-
class ListUser(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class CreateUser(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # for checking purpose-
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    
class LoginUserView(APIView):

    def post(self,request):
       serializer = UserLoginSerializer(data=request.data)

       if serializer.is_valid():
           try:
                user = User.objects.get(email=serializer.validated_data["email"])
                if user.password == serializer.validated_data["password"]:
                    #token not exist then create otherwise get
                    token=Token.objects.get_or_create(user=user)
                    return Response({"success":True,"token":token[0].key})
                else:
                    return Response({"success":False,"message":"incorrect password"})
           except ObjectDoesNotExist:
               return Response({"success":False,"message":"user does not exist"})
           
class RetrieveUser(generics.RetrieveAPIView):
      queryset = User.objects.all()
      serializer_class = UserSerializer
      authentication_classes = [TokenAuthentication]
      permission_classes = [IsAuthenticated]

               
class UpdateUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        # check -- login user = user
        if request.user.id != int(pk):
            return Response({"error": "You are not allowed to update this user's profile"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            updated_user = serializer.save()
            return Response({"msg": "User updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DeleteUser(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        try:
            user = self.get_object()  
            if user.id == request.user.id:  
                self.perform_destroy(user)
                return Response({"success": True, "message": "User deleted"}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"success": False, "message": "You can only delete your own profile"},
                                status=status.HTTP_403_FORBIDDEN)
        except ObjectDoesNotExist:
            return Response({"success": False, "message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        




# post----
class ListPost(generics.ListAPIView):
     queryset = Post.objects.all()
     serializer_class = PostSerializer

class CreatePost(generics.CreateAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

           
class RetrievePost(generics.RetrieveAPIView):
      queryset = Post.objects.all()
      serializer_class = PostSerializer

class UpdatePost(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"msg": "Post does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(post, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            # Ensure the user is the owner of the post
            if request.user != post.user:
                raise PermissionDenied("You do not have permission to update this post.")

            serializer.save()
            return Response({"msg": "Data is Updated!!", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"msg": "Data is Not Updated!!", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
class DestroyPost(generics.DestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        try:
            pk = kwargs.get("pk")
            post = Post.objects.get(id=pk)
            if post.user.id == request.user.id:
                self.perform_destroy(post)
                return Response({"success":True,"message":"Post Deleted"})
            else:
                return Response({"success":False,"message":"not enough permissions"})
        except ObjectDoesNotExist:
            return Response({"success":False,"message":"post does not exist"})
        

class RetrieweUserPosts(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
    
        user_posts = Post.objects.filter(user=request.user)
        
        
        serializer = self.serializer_class(user_posts, many=True)
        
        
        return Response({"success": True, "posts": serializer.data})
    
class LikePost(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get(self,request,pk):
        try:    
            
            post = Post.objects.get(id=pk)
            Like_list = PostLike.objects.filter(post=post)
            serializer = PostLikeSerializer(Like_list,many=True)
            
            return Response({"success":True,"Likes_list":serializer.data})
            
        except ObjectDoesNotExist:
            return Response({"success":False,"message":"post does not exist"})
    
    def post(self,request,pk):
        try:
            post = Post.objects.get(id=pk)
            # it is for if we like post then we get post and if we don't like then in db created the like field
            new_post_like = PostLike.objects.get_or_create(user=request.user,post=post)
            if not new_post_like[1]:
                new_post_like[0].delete()
                return Response({"success":True,"message":"Post unLiked"})
            else:
                return Response({"sucess":True,"message":"Post Liked"})
        except ObjectDoesNotExist:
            return Response({"success":False,"message":"Post does not exist"})
        

        
class CommentPost(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
 
    def get(self,request,pk):
        try:    
            context = {
                "request":request
            }
            post = Post.objects.get(id=pk)
            comments = Comment.objects.filter(post=post)
            serializer = CommentSerializer(comments,many=True)
            
            
            return Response({"success":True,"Comments":serializer.data})
            
        except ObjectDoesNotExist:
            return Response({"success":False,"message":"post does not exist"})


    def post(self,request,pk):
        try:
            context = {
                "request":request
            }
            post = Post.objects.get(id=pk)
            # request.data["post"] =post
            serializer = self.serializer_class(context=context,data=request.data)
            if serializer.is_valid():
                serializer.save(post=post)
                return Response({"success":True,"message":"comment added"})
            else:
                return Response({"success":False,"message":"error adding a comment"})
        except ObjectDoesNotExist:
            return Response({"success":False,"message":"post does not exist"})

class FollowUser(APIView):
    # queryset = UserFollow.objects.all()
    # serializer_class = UserFollowSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            # Retrieve all following users
            following = UserFollow.objects.filter(user=request.user)
            following_serializer = UserFollowSerializer(following, many=True)

            # Retrieve all followers of the user with id=pk
            followers = UserFollow.objects.filter(follows=pk)
            followers_serializer = UserFollowSerializer(followers, many=True)

            return Response({"success": True, "following": following_serializer.data, "followers": followers_serializer.data})
        except ObjectDoesNotExist:
            return Response({"success": False, "message": "User or followers/following not found"})

    def post(self, request, pk):
        try:
            # Retrieve the user to follow/unfollow
            following_user = User.objects.get(id=pk)

            # Check if the user is already followed
            follow_user, created = UserFollow.objects.get_or_create(user=request.user, follows=following_user)

            if not created:
                # If the relationship already exists, delete it (unfollow)
                follow_user.delete()
                return Response({"success": True, "message": "Unfollowed user"})
            else:
                return Response({"success": True, "message": "Followed user"})
        except ObjectDoesNotExist:
            return Response({"success": False, "message": "User to follow/unfollow doesn't exist"})