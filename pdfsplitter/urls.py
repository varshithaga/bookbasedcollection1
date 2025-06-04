from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_pdf, name='upload_pdf'),
    path('frames/<int:file_id>/', views.view_frames, name='view_frames'),
    path('enter-frames/<int:file_id>/', views.enter_frames, name='enter_frames'),
    path('generate-frames/<int:file_id>/<int:n_frames>/', views.generate_frames, name='generate_frames'),
    path('', views.home, name='home'),  

]
