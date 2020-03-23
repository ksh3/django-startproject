import pytest
from django.urls import reverse
from django.utils import timezone
from factory import fuzzy, SubFactory
from factory.django import DjangoModelFactory

from . import models


class UserFactory(DjangoModelFactory):

    class Meta:
        model = models.User
        django_get_or_create = ('username', 'password')

    username = fuzzy.FuzzyText(length=16)
    password = fuzzy.FuzzyText(length=16)

    @classmethod
    def create_user(cls, username: str) -> models.User:
        user = UserFactory(username=username, password='password')
        return user


class SubscriptionFactory(DjangoModelFactory):

    class Meta:
        model = models.Subscription
        django_get_or_create = ('user', 'expired_at')

    user = SubFactory(UserFactory)
    expired_at = timezone.now() + timezone.timedelta(days=1)


@pytest.fixture(autouse=True)
def unsubscriber() -> models.User:
    return UserFactory.create_user('unsubscriber')


@pytest.fixture(autouse=True)
def expired_subscriber():
    user = UserFactory.create_user('expired_subscriber')
    SubscriptionFactory(
        user=user, expired_at=timezone.now() - timezone.timedelta(days=1))
    return user


@pytest.fixture(autouse=True)
def subscriber():
    user = UserFactory.create_user('subscriber')
    SubscriptionFactory(user=user)
    return user


@pytest.mark.django_db
class TestModel:

    def test_subscriber(self, subscriber) -> bool:
        assert subscriber.is_subscriber

    def test_unsubscriber(self, unsubscriber) -> bool:
        assert not unsubscriber.is_subscriber

    def test_expired_subscriber(self, expired_subscriber) -> bool:
        assert not expired_subscriber.is_subscriber


@pytest.mark.django_db
class TestView:

    @pytest.mark.parametrize(
        'url, status_code',
        [
            (reverse('app:index'), 200),
            (reverse('app:registration'), 200),
            (reverse('app:logout'), 200),
            (reverse('app:dashboard'), 302),
            (reverse('app:free-content'), 302),
            (reverse('app:paid-content'), 302),
            (reverse('app:subscription-create'), 302),
        ]
    )
    def test_anonymous_views(self, client, url, status_code) -> bool:

        resp = client.get(url)
        assert resp.status_code == status_code

    @pytest.mark.parametrize(
        'url, status_code',
        [
            (reverse('app:index'), 200),
            (reverse('app:registration'), 200),
            (reverse('app:logout'), 200),
            (reverse('app:dashboard'), 200),
            (reverse('app:free-content'), 200),
            (reverse('app:paid-content'), 403),
            (reverse('app:subscription-create'), 200),
        ]
    )
    def test_unsubscriber_views(self, client, unsubscriber,
                                url, status_code) -> bool:

        client.force_login(unsubscriber)
        resp = client.get(url)
        assert resp.status_code == status_code

    @pytest.mark.parametrize(
        'url, status_code',
        [
            (reverse('app:index'), 200),
            (reverse('app:registration'), 200),
            (reverse('app:logout'), 200),
            (reverse('app:dashboard'), 200),
            (reverse('app:free-content'), 200),
            (reverse('app:paid-content'), 200),
            (reverse('app:subscription-create'), 400),
        ]
    )
    def test_subscriber_views(self, client, subscriber, url,
                              status_code) -> bool:

        client.force_login(subscriber)
        resp = client.get(url)
        assert resp.status_code == status_code

    def test_subscription_create(self, client, unsubscriber):
        client.force_login(unsubscriber)
        resp = client.post(reverse('app:subscription-create'), {})
        assert resp.status_code == 302
        assert unsubscriber.is_subscriber

    def test_not_allow_subscription_create(self, client, subscriber):
        client.force_login(subscriber)
        resp = client.post(reverse('app:subscription-create'), {})
        assert resp.status_code == 400
