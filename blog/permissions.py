from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    작성자만 수정/삭제 권한 부여 (나머지는 읽기만 가능)
    """
    def has_object_permission(self, request, view, obj):
        #읽기는 누구나 허용
        if request.method in permissions.SAFE_METHODS:
            return True
        
        #수정/삭제는 작성자만 가능
        return obj.author == request.user


#과제 유저뷰셋 조회 보호
class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'list':   # 목록 조회 하면 관리자만 허용하게 하면 됨.
            return bool(request.user and request.user.is_staff)# is_staff는 True면 admin 페이지 접속가능하고 나머지는 일반 유저와 동일함.
        elif view.action == 'retrieve': # 목록이 아닌 단일 객체?를 조회하면 로그인된 사용자만 접속하게 하기
            return bool(request.user and request.user.is_authenticated)
        
        return False
    
    def has_object_permission(self, request, view, obj):
        # retrieve이 호출되면 여기로 내려오는데 관리자나 본인만 접속하게 하는 것임.
        return request.user.is_staff or obj == request.user

    
