from django.urls import path
from . import views

urlpatterns = [
    path('conversations/', views.ConversationListView.as_view(), name='conversation_list'),
    path('conversations/<int:conversation_id>/messages/', views.MessageListView.as_view(), name='message_list'),
]
