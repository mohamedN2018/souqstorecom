"""
Write-side business logic (services layer).

Keeping mutations here — instead of in serializers/views — keeps the API thin
and makes the logic reusable from Celery tasks, management commands, or events.
"""
from __future__ import annotations

from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()


@transaction.atomic
def register_user(
    *,
    email: str,
    password: str,
    full_name: str = "",
    phone: str = "",
    role: str = "customer",
) -> User:
    """Create a new account. Raises django.db.IntegrityError on duplicate email."""
    user = User.objects.create_user(
        email=email,
        password=password,
        full_name=full_name,
        phone=phone,
        role=role,
    )
    # TODO(events): publish `user.registered` to the event bus so the
    # notification service can send a welcome/verification email.
    return user
