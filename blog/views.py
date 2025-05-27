from rest_framework import viewsets, permissions, throttling
from .models import Post, Comment
from django.contrib.auth.models import User
from .serializers import PostSerializer, CommentSerializer, UserSerializer
from .permissions import IsAuthorOrReadOnly, IsAdminUser

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    filterset_fields =['author__username', 'title'] #'author_username은 장고 ORM에서 자동으로 만들어주는 유저이름
                                                    # 추가 ORM 제공 : author__email, author__id, comment__post__title
    ordering_fields =['created_at', 'title']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class UserViewThrottle(throttling.UserRateThrottle):
    scope = 'user_view'

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    #과제 유저뷰셋 조회 보호
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    # IsAuthenticated는 인증된 사용자만 접근을 허용하는데 IsAuthenticatedOrReadOnly 이건 비인증 사용자도 읽는 접근은 가능함.
    # 아래 참고
    # https://ssungkang.tistory.com/entry/Django-Authentication-%EA%B3%BC-Permissions
    # https://www.django-rest-framework.org/api-guide/permissions/


    throttle_classes = [UserViewThrottle]
    # 아래 참고
    # https://ssungkang.tistory.com/entry/Django-Throttling


