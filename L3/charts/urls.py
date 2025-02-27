from django.urls import path
from charts.views import crypto_chart, get_chart_data

urlpatterns = [
    path("chart/", crypto_chart, name="crypto_chart"),
    path("get_chart_data/", get_chart_data, name="get_chart_data"),  # API endpoint
]
