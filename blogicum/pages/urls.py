from django.urls import path
from . import views


app_name = 'pages'

urlpatterns = [
    path('about/', views.AboutTemplateView.as_view(), name='about'),
    path('rules/', views.RulesTemplateView.as_view(), name='rules'),
]
