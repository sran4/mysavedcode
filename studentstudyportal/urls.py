from django.contrib import admin
from django.urls import path, include
from dashboard import views as dash_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import (
    handler400, handler403, handler404, handler500
)
from ckeditor_uploader.views import ImageUploadView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('admin/', include('admin_honeypot.urls',
         namespace='admin_honeypot')),  # add this line
    # change this to securelogin instead of admin
    path('securelogin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('images/', ImageUploadView.as_view(), name='image-upload'),

    path('register/', dash_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name="dashboard/auth/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name="dashboard/auth/logout.html"), name='logout'),
    path('profile/', dash_views.profile, name='profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)


handler404 = 'dashboard.views.handle404'

