from django.contrib import admin
from django.urls import path, include
from django_apps.qcm import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.ThemeQuestionView.as_view(), name='index'),
    path('report', views.ReportView.as_view(), name='report'),
    path('questionsdb', views.MCQModelView.as_view(), name="question_db_viewer"),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('mcq-all-viewer/', views.MCQModelView.as_view(), name="mcq_all_viewer"),
    path('mcq-one-viewer/', views.MCQModelViewer.as_view(), name="mcq_one-viewer"),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='register'),

]
