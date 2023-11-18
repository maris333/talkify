from src.run import login_manager
from src.models.auth import User


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
