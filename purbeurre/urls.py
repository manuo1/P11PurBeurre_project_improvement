"""purbeurre URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path


def sentry_error_test(request):
    """Raises an error when using sentry-debug/ url."""
    """ that will be captured by Sentry  """
    division_by_zero = 1 / 0


urlpatterns = [
    path('mo1admin/', admin.site.urls),
    path('user/', include('app_users.urls')),
    path('', include('app_products.urls')),
    path('sentry-debug/', sentry_error_test),
]
