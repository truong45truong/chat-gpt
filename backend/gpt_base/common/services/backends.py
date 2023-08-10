from gpt_base.user.models import User

def get_user(user_id):
    try:
        user = User._default_manager.get(pk=user_id)
        return user
    except Exception:
        return None