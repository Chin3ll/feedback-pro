from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from yourapp.models import Profile

class Command(BaseCommand):
    help = "Create missing profiles for users"

    def handle(self, *args, **kwargs):
        users_without_profiles = User.objects.filter(profile__isnull=True)
        for user in users_without_profiles:
            Profile.objects.create(user=user)
            self.stdout.write(f"Created profile for {user.username}")
        self.stdout.write("Profiles created for all users without profiles.")
