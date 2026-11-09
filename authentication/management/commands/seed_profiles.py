import secrets
import string

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from authentication.models import RoleChoices, TechChoices, profile


PROFILES = [
    ("Ava", "Thompson", "4821", RoleChoices.PROJECT_COORDINATOR, None),
    ("Marcus", "Chen", "7316", RoleChoices.PROJECT_COORDINATOR, None),
    ("Sofia", "Patel", "2947", RoleChoices.DEVEPLOPER, TechChoices.FRONTEND),
    ("Liam", "Brooks", "6183", RoleChoices.DEVEPLOPER, TechChoices.BACKEND),
    ("Maya", "Rodriguez", "8502", RoleChoices.DEVEPLOPER, TechChoices.FULLSTACK),
    ("Noah", "Kim", "4391", RoleChoices.DEVEPLOPER, TechChoices.TESTER),
    ("Priya", "Shah", "7624", RoleChoices.DEVEPLOPER, TechChoices.UIUX),
    ("Ethan", "Wright", "3058", RoleChoices.DEVEPLOPER, TechChoices.BACKEND),
    ("Isabella", "Nguyen", "9173", RoleChoices.DEVEPLOPER, TechChoices.FRONTEND),
    ("Daniel", "Foster", "5640", RoleChoices.DEVEPLOPER, TechChoices.FULLSTACK),
    ("Zoe", "Martin", "8236", RoleChoices.DEVEPLOPER, TechChoices.TESTER),
    ("Arjun", "Mehta", "1469", RoleChoices.DEVEPLOPER, TechChoices.BACKEND),
    ("Grace", "Cooper", "6725", RoleChoices.DEVEPLOPER, TechChoices.UIUX),
    ("Mateo", "Silva", "3904", RoleChoices.DEVEPLOPER, TechChoices.FRONTEND),
    ("Chloe", "Bennett", "5842", RoleChoices.DEVEPLOPER, TechChoices.FULLSTACK),
    ("Omar", "Hassan", "2317", RoleChoices.DEVEPLOPER, TechChoices.TESTER),
    ("Leah", "Park", "9056", RoleChoices.DEVEPLOPER, TechChoices.BACKEND),
]


class Command(BaseCommand):
    help = "Create sample project coordinators and developers."

    def handle(self, *args, **options):
        created_credentials = []
        existing_count = 0

        with transaction.atomic():
            for first_name, last_name, number, role, tech in PROFILES:
                email = (
                    f"{first_name.lower()}.{last_name.lower()}{number}@mailinator.com"
                )
                existing = profile.objects.filter(username=email).first()
                if existing:
                    expected = (first_name, last_name, email, role, tech)
                    actual = (
                        existing.first_name,
                        existing.last_name,
                        existing.email,
                        existing.role,
                        existing.tech,
                    )
                    if actual != expected:
                        raise CommandError(
                            f"Username {email!r} already belongs to a different profile."
                        )
                    existing_count += 1
                    continue

                user = profile(
                    username=email,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    role=role,
                    tech=tech,
                )
                password = self._generate_password(user)
                user.set_password(password)
                user.save()
                created_credentials.append((user, password))

        if created_credentials:
            self.stdout.write("Created profiles (copy these passwords now):")
            for user, password in created_credentials:
                self.stdout.write(
                    f"{user.get_full_name()} | {user.role} | "
                    f"{user.username} | {password}"
                )
        if existing_count:
            self.stdout.write(
                self.style.WARNING(
                    f"{existing_count} matching profiles already existed; "
                    "their passwords were left unchanged and cannot be displayed."
                )
            )

    @staticmethod
    def _generate_password(user):
        alphabet = string.ascii_letters + string.digits + "!@#$%&*-_"
        while True:
            characters = [
                secrets.choice(string.ascii_lowercase),
                secrets.choice(string.ascii_uppercase),
                secrets.choice(string.digits),
                secrets.choice("!@#$%&*-_"),
            ]
            characters.extend(secrets.choice(alphabet) for _ in range(20))
            secrets.SystemRandom().shuffle(characters)
            password = "".join(characters)
            try:
                validate_password(password, user)
            except ValidationError:
                continue
            return password