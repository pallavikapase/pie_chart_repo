from django.conf.urls import url
from agent_sales import views

# template URLs

app_name = 'agent_sales'

urlpatterns = [
    url(r'^pie_chart/', views.pie_chart, name= 'pie_chart'),
]
