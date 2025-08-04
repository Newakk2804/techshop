import pytest
import time
from django.utils import timezone
from django.core.exceptions import ValidationError
from newsletters.models import Subscriber


@pytest.mark.django_db
def test_subscriber_creation():
    email = "test@example.com"
    subscriber = Subscriber.objects.create(email=email)

    assert subscriber.email == email
    assert subscriber.subscribed_at is not None


@pytest.mark.django_db
def test_subscriber_unique_email():
    email = "test@example.com"
    Subscriber.objects.create(email=email)

    with pytest.raises(Exception):
        Subscriber.objects.create(email=email)


@pytest.mark.django_db
def test_subscriber_email_validation():
    with pytest.raises(ValidationError):
        subscriber = Subscriber(email="invalid-email")
        subscriber.full_clean()


@pytest.mark.django_db
def test_subscriber_str_representation():
    email = "test@example.com"
    subscriber = Subscriber.objects.create(email=email)

    assert str(subscriber) == email


@pytest.mark.django_db
def test_subscriber_meta_verbose_names():
    """Тест мета-информации модели"""
    subscriber = Subscriber.objects.create(email="test@example.com")

    assert subscriber._meta.verbose_name == "Подписчик"
    assert subscriber._meta.verbose_name_plural == "Подписчики"


@pytest.mark.django_db
def test_subscriber_auto_now_add():
    before_creation = timezone.now()
    time.sleep(0.001)
    subscriber = Subscriber.objects.create(email="test@example.com")
    time.sleep(0.001)
    after_creation = timezone.now()

    assert before_creation <= subscriber.subscribed_at <= after_creation


@pytest.mark.django_db
def test_subscriber_case_insensitive_email():
    email1 = "test@example.com"
    email2 = "TEST@EXAMPLE.COM"

    Subscriber.objects.create(email=email1)

    assert Subscriber.objects.filter(email=email2.lower()).exists()


@pytest.mark.django_db
def test_subscriber_multiple_subscribers():
    emails = [
        "user1@example.com",
        "user2@example.com",
        "user3@example.com",
    ]

    subscribers = []
    for email in emails:
        subscriber = Subscriber.objects.create(email=email)
        subscribers.append(subscriber)

    assert len(subscribers) == 3
    assert Subscriber.objects.count() == 3

    unique_emails = set(sub.email for sub in subscribers)
    assert len(unique_emails) == 3
