# =======================================================================
# FILE: myduka/users/urls.py (FIXED)
# =======================================================================
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, UserDetailView, InviteUserView, CompleteInviteView, ManageStaffView
from django.http import JsonResponse

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', UserDetailView.as_view(), name='user_detail'),
    path('invite/', InviteUserView.as_view(), name='invite_user'),
    path('complete-invite/', CompleteInviteView.as_view(), name='complete_invite'),
    path("api/v1/ping/", lambda request: JsonResponse({"status": "ok"})),
    path('staff/<int:user_id>/manage/', ManageStaffView.as_view(), name='manage_staff'),
]