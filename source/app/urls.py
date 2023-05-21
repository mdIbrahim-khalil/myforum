from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from main.views import (ChangeLanguageView, IndexPageView,
                        subscription_public_view)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexPageView.as_view(), name='index'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('language/', ChangeLanguageView.as_view(), name='change_language'),
    path('accounts/', include('accounts.urls')),
    path('forum/', include('django_forum_app.urls', namespace='forum')),
    url('avatar/', include('avatar.urls')),
    path('flag/', include('flag.urls')),
    url(r'^notifications/', include('notify.urls', 'notifications')),

    url(r'^terms/', TemplateView.as_view(template_name="terms.html"), name='terms'),
    url(r'^privacy/', TemplateView.as_view(template_name="privacy.html"), name='privacy'),
    url(r'^subscription/', subscription_public_view, name='subscription_public'),
    url(r'^about/', TemplateView.as_view(template_name="about.html"), name='about'),
    url(r'^contact/', TemplateView.as_view(template_name="contact.html"), name='contact'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
