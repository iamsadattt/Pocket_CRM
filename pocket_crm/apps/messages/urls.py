from django.urls import path
from .views import MessageListCreateView, MessageDetailView, MessageGenerateView, MessageSendView

app_name = 'pocket_messages'

urlpatterns = [
    path('', MessageListCreateView.as_view(), name='message-list'),
    path('<int:pk>/', MessageDetailView.as_view(), name='message-detail'),
    path('<int:pk>/send/', MessageSendView.as_view(), name='message-send'),
    path('generate/', MessageGenerateView.as_view(), name='message-generate'),
]
