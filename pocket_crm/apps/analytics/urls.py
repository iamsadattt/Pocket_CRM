from django.urls import path
from .views import AnalyticsOverviewView

app_name = 'pocket_analytics'

urlpatterns = [
    path('overview/', AnalyticsOverviewView.as_view(), name='overview'),
]
