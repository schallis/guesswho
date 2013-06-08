from django.contrib import auth


def log_user_in_without_password(request, user):
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    auth.login(request, user)
