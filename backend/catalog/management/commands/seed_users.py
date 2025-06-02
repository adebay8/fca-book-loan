from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        users = [
            {"username": "john", "email": "john@example.com", "password": "password123"},
            {"username": "jane", "email": "jane@example.com", "password": "password123"},
        ]

        for data in users:
            if not User.objects.filter(username=data["username"]).exists():
                user = User.objects.create_user(
                    username=data["username"],
                    email=data["email"],
                    password=data["password"]
                )
                self.stdout.write(self.style.SUCCESS(f"Created user: {user.username}"))
            else:
                self.stdout.write(f"User {data['username']} already exists")
