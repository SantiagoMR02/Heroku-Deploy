from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import PDFinve, PDFacti, PDFsal, PDFot

# Importación para recuperar contraseña
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('usuarios/login', views.login_view, name='login'),
    path('usuarios/logout', views.logout_view, name='logout'),
    path('usuarios/registro', views.register, name='register'),
    path('usuarios/remember', views.remember_view, name='remember'),
    path('pruevas/', views.pruevas, name='pruevas'),
    path('', views.index, name='index'),   
    path('admin/', admin.site.urls),
    path('pagos/', views.pagos, name='pagos'),

    #Rutas Recuperación de contraseña
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='reset_password.html'), name='reset_password'),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="reset_password_sent.html"), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="reset.html"),name='password_reset_confirm'),

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="reset_password_complete.html"),name='password_reset_complete'),

    #PDF
    path('PDFinve/', PDFinve.as_view(), name='PDFinve'),
    path('PDFacti/', PDFacti.as_view(), name='PDFacti'),
    path('PDFsal/', PDFsal.as_view(), name='PDFsal'),
    path('PDFot/', PDFot.as_view(), name='PDFot'),
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


