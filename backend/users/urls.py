from django.urls import include, path
from djoser.views import UserViewSet, TokenDestroyView


from .views import TokenCreateView

app_name = "users"

auth_patterns = [
    path(r"token/login/", TokenCreateView.as_view(), name="login"),
    path(r"token/logout/", TokenDestroyView.as_view(), name="logout"),
]
users_patterns = [
    path(r"", UserViewSet.as_view({"get": "list", "post": "create"})),
    path(r"<int:id>/", UserViewSet.as_view({"get": "retrieve"})),
    path(r"me/", UserViewSet.as_view({"get": "me"})),
    path(r"set_password/", UserViewSet.as_view({"post": "set_password"})),
]

urlpatterns = [
    path(r"auth/", include(auth_patterns)),
    path(r"users/", include(users_patterns)),
]
