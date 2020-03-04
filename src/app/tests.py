import pytest
from django.urls import reverse
from factory import fuzzy
from factory.django import DjangoModelFactory

from . import models


class UserFactory(DjangoModelFactory):

    class Meta:
        model = models.User
        django_get_or_create = ('username', 'password')

    username = fuzzy.FuzzyText(length=16)
    password = fuzzy.FuzzyText(length=16)

    @classmethod
    def create_unsubscriber(cls, username: str) -> models.User:
        subscriber = UserFactory(username=username, password='password')
        return subscriber


@pytest.fixture(autouse=True)
def unsubscriber() -> models.User:
    return UserFactory.create_unsubscriber('unsubscriber')


# FIXME: Define subscriber.
# @pytest.fixture(autouse=True)
# def subscriber():
#     return UserFactory.create_subscriber()


@pytest.mark.django_db
class TestModel:

    # FIXME: Define subscriber.
    def test_is_subscribe(self, unsubscriber) -> bool:
        assert not unsubscriber.is_subscriber


@pytest.mark.django_db
class TestView:

    @pytest.mark.parametrize(
        'url, status_code',
        [
            (reverse('app:index'), 200),
            (reverse('app:registration'), 200),
        ]
    )
    def test_public_views(self, client, url, status_code) -> bool:
        resp = client.get(url)
        assert resp.status_code == status_code

    @pytest.mark.parametrize(
        'url, status_code',
        [
            (reverse('app:logout'), 200),
            (reverse('app:dashboard'), 200),
            (reverse('app:free-content'), 200),
        ]
    )
    def test_login_required_views(self, client,
                                  unsubscriber, url, status_code) -> bool:
        client.force_login(unsubscriber)
        resp = client.get(url)
        assert resp.status_code == status_code

    @pytest.mark.parametrize(
        'url, status_code',
        [
            (reverse('app:paid-content'), 403),
        ]
    )
    def test_subscriber_required_views(self, client,
                                       unsubscriber, url, status_code) -> bool:
        client.force_login(unsubscriber)
        resp = client.get(url)
        assert resp.status_code == status_code
