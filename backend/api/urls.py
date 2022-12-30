from django.urls import include, path

# from django.views.generic import TemplateView
# from rest_framework import routers


app_name = "api"

# router = routers.DefaultRouter()
# router.register(r'groups', GroupViewSet, basename='groups')
# router.register(r'posts', PostViewSet, basename='posts')
# router.register(
#     r'posts/(?P<post_id>\d+)/comments',
#     CommentViewSet,
#     basename='comments'
# )
# router.register(r'follow', FollowViewSet, basename='follow')

urlpatterns = [
    path(r"", include("users.urls", namespace="users")),
    # path(include(router.urls)),
]
