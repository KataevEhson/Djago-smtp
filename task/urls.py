from django.urls import path
from .views import *

urlpatterns = [
    path('', registraion, name='registration'),
    path('confirm-email/', confirm_email, name='confirm_email'),
    path('login/', login_user, name='login'),

    path('tasks/new/', task_create, name='task_create'),
    path('tasks/<int:id>/', task_detail, name='task_detail'),

    path('tasks/<int:id>/edit/', task_update,  name='task_update'),
    path('tasks/<int:id>/delete/', task_delete, name='task_delete'),

    path('send-message/', send_message_all, name='send_message_all'),
    path('profile/', show_profile, name='profile'),
]
