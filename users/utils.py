from rest_framework.authtoken.models import Token
from .models import User

def get_user_from_token(token):
    try:
        token_obj = Token.objects.get(key=token)
        user = User.objects.get(pk=token_obj.user_id)
        return user
    except Token.DoesNotExist:
        return None
  