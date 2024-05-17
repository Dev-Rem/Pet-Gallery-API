from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from jwt import decode as jwt_decode
from django.conf import settings
from django.contrib.auth import get_user_model
from urllib.parse import parse_qs

from typing import Dict

from users.models import CustomUser


@database_sync_to_async
def get_user(decoded_data: Dict) -> CustomUser:
    try:
        user = get_user_model().objects.get(id=decoded_data["user_id"])
        return user

    except CustomUser.DoesNotExist:
        return AnonymousUser()


class TokenAuthMiddleware(BaseMiddleware):
    """
    Custom jwt token auth middleware
    """

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        # Close old database connections to prevent usage of timed out connections
        close_old_connections()
        token = parse_qs(scope["query_string"].decode("utf8"))["token"][0]

        # Try to authenticate the user
        try:
            UntypedToken(token)
        except (InvalidToken, TokenError) as e:
            raise e
        else:
            decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = get_user(decoded_data=decoded_data)

            # Add the user to the scope
            scope["user"] = user
            scope["auth_user_id"] = decoded_data["user_id"]
            return await super().__call__(scope, receive, send)
