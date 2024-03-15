from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from app.models import User,Post,Comment,PostLike,UserFollow

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()
    bio = serializers.CharField()

    # def create(self, v
    
    def create(self, validated_data):
        # Remove groups from validated_data if present
        groups = validated_data.pop('groups', None)
        
        # Create the user object
        user = User.objects.create(**validated_data)
        
        # If groups were provided, add them to the user
        if groups:
            user.groups.set(groups)
        
        return user
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


    title = serializers.CharField()
    description = serializers.CharField()
    image = serializers.ImageField()
    # it mean that when we post then user not show it's hidden only current use we have 
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def update(self, instance, validated_data):
        # Check if the current user is the owner of the post
        if instance.user == self.context['request'].user:
            return super().update(instance, validated_data)
        else:
            raise PermissionDenied("You do not have permission to update this post.")
        

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

    comment_text = serializers.CharField(max_length=100)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    def save(self, **kwargs):
        # Assign the post object to the comment's post field
        self.validated_data['post'] = kwargs.get('post')
        self.post = kwargs["post"]
        return super().save(**kwargs)
    
class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = "__all__"
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)

class UserFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollow
        fields = "__all__"

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    follows_id = serializers.PrimaryKeyRelatedField(read_only=True)
    