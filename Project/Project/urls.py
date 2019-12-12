from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from Users import views as user_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('FittingRoom.urls')),
    path('register/', user_views.register, name = 'User-Register'),
    path('login/', auth_views.LoginView.as_view( template_name = 'Users/login.html' ),
        name = 'User-Login'),
    path('logout/', auth_views.LogoutView.as_view( template_name = 'Users/logout.html' ), name = 'User-Logout'),
    path('profile/', user_views.profile, name = 'User-Profile'),
    # path('password-reset/',
    #     auth_views.PasswordResetView.as_view(template_name = 'Users/reset_pwd.html'),
    #     name = 'User-Reset-Pwd'),
    # path('password-reset/done/',
    #     auth_views.PasswordResetDoneView.as_view(template_name = "Users/reset_pwd_done.html"),
    #     name = 'User-Reset-Pwd-Done'),
    # path('password-reset-confirm/<uidb64>/<token>/',
    #      auth_views.PasswordResetConfirmView.as_view(
    #          template_name='Users/pwd_reset_confirm.html'
    #      ),
    #      name='password_reset_confirm'),
    path('upload/', user_views.upload_dress, name = 'User-Upload'),
    path('delete-confirmation/', user_views.delete_profile_confirmation, name = 'User-Delete-Confirmation'),
    path('delete-confirmed/', user_views.delete_profile, name = 'User-Delete-Confirmed'),
    path('admin-upload/', user_views.admin_upload, name = 'User-Admin-Upload')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.UPLOAD_URL, document_root = settings.UPLOAD_ROOT)
