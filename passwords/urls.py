from django.urls import path
from django.contrib.auth.views import PasswordChangeView, \
    PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('mudar-senha/', PasswordChangeView.as_view(
        template_name='passwords/password_change_form.html',
        success_url='done'),
         name='change_password'),
    path('mudar-senha/done/', PasswordChangeDoneView.as_view(
        template_name='passwords/password_change_done.html'),
         name='change_password_done'),

    path('mudar-senha/recuperar', PasswordResetView.as_view(
        template_name='passwords/password_reset_form.html',
        success_url='recuperar/done',
        subject_template_name='passwords/password_reset_subject.txt',
        email_template_name='passwords/password_reset_email.html'),
         name='reset_password'),
    path('mudar-senha/recuperar/done', PasswordResetDoneView.as_view(
        template_name='passwords/password_reset_done.html'),
         name='reset_password_done'),
    path('mudar-senha/recuperar/confirmar/<str:uidb64>/<str:token>/',
         PasswordResetConfirmView.as_view(
             template_name='passwords/password_reset_confirm.html'),
         name='reset_password_confirm'),
    path('mudar-senha/recuperar/confirmar/done',
         PasswordResetCompleteView.as_view(
             template_name='passwords/password_reset_complete.html'),
         name='password_reset_complete'),
]
