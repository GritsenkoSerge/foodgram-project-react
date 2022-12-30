from djoser import views
from rest_framework import status


class TokenCreateView(views.TokenCreateView):
    def _action(self, serializer):
        response = super()._action(serializer)
        if response.status_code == status.HTTP_200_OK:
            response.status_code = status.HTTP_201_CREATED
        return response
