from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('dashboard', views.DashboardView.as_view(), name='dashboard'),
    path('paid-content', views.PaidContentView.as_view(), name='paid-content'),
    path('free-content', views.FreeContentView.as_view(), name='free-content'),
    path(
        'registration', views.RegistrationView.as_view(),
        name='registration'
    ),
    path('login', views.InheritedLoginView.as_view(), name='login'),
    path(
        'logout', LogoutView.as_view(template_name='logout.html'),
        name='logout'
    ),
    path('subscription-create', views.SubscriptionCreateView.as_view(),
         name='subscription-create'),
]
