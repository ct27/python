"""ct_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls import url, include
from accounts.views import RegisterView, LoginView
from django.contrib.auth import views as auth_views

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^', include('blog.urls')),
    url(r'^blog/', include(('blog.urls', 'blog'), namespace='blog')),
    url(r'^search/', include(('search.urls', 'search'), namespace='search')),
    url(r'^login/$',LoginView.as_view(), name='login'),
    url(r'^register/$',RegisterView.as_view(), name='register'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)