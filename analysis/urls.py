from django.urls import path

from .views import user_home, user_data, user_data_update, user_pictures, \
    user_pictures_create, user_pictures_delete, user_pictures_update, \
    user_pictures_report

urlpatterns = [
    path('user/', user_home, name='user_home'),
    path('meus_dados/', user_data, name='user_data'),
    path('meus_dados/update/', user_data_update,
         name='update_data'),
    path('analise/', user_pictures, name='user_pics'),
    path('analise/create/', user_pictures_create,
         name='create_pic'),
    path('analise/update/<int:pic_id>/', user_pictures_update,
         name='update_pic'),
    path('analise/delete/<int:pic_id>/', user_pictures_delete,
         name='delete_pic'),
    path('analise/report/<int:pic_id>/', user_pictures_report,
         name='report_pic'),
]
