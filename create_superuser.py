# create_superuser.py
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

if username and email and password:
    if not User.objects.filter(username=username).exists():
        print(f"Creating superuser {username}")
        User.objects.create_superuser(username, email, password)
    else:
        print(f"Superuser {username} already exists")
else:
    print("Superuser environment variables not set")
