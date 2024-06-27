from django.urls import include, path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path('start_interview/', views.start_interview, name='start_interview'),
    path('submit_message/', views.submit_message, name='submit_message'),
    path("<str:thread_id>/", views.chat, name="chat"),
]