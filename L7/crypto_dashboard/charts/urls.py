from django.urls import path
from .views import bitcoin_chart, alma_chart

urlpatterns = [
    path("bitcoin-chart/", bitcoin_chart, name="bitcoin_chart"),
    path('alma-chart/', alma_chart, name='alma_chart'),  # Add this line for the chart page
]
