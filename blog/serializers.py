'''
모델 시리얼라이져
객체식별: ID를 기반
관계필드 설정: PKFK
API 탐색: 프론트가 ID를 추측해서 URL로 만들어야함
'''
# from rest_framework import serializers
# from .models import Post, Comment
# from django.contrib.auth.models import User

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username']

# class CommentSerializer(serializers.ModelSerializer):
#     author = UserSerializer(read_only=True)

#     class Meta:
#         model = Comment
#         fields = ['id', 'post', 'author', 'content', 'created_at']

# class PostSerializer(serializers.ModelSerializer):
#     author = UserSerializer(read_only=True)
#     comments = CommentSerializer(many=True, read_only=True)

#     class Meta:
#         model = Post
#         fields = ['id', 'title', 'content', 'author', 'created_at', 'comments']
'''
하이퍼링크드
객체식별: URL
관계필드: 다른 링크
API 탐색: URL이 응답에 포함되어 있음(클릭만 하면 됨)
REST철학: HATEOAS준수
'''
#얻게되는 효과 : 탐색가능성 증가, 프론트와의 협업향상(데이터 참조 시 URL로 직접 접근이 가능해 API통합이 쉬워짐)

from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'username']

class PostSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        read_only=True
    )
    url = serializers.HyperlinkedIdentityField(
        view_name='post-detail'
    )
    class Meta:
        model = Post
        fields = ['url', 'id', 'title', 'content', 'author', 'created_at']

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        read_only=True
    )
    post = serializers.HyperlinkedRelatedField(
        view_name='post-detail',
        queryset=Post.objects.all()
    )
    url = serializers.HyperlinkedIdentityField(
        view_name='comment-detail'
    )

    class Meta:
        model = Comment
        fields = ['url', 'id', 'post', 'author', 'content', 'created_at']
        