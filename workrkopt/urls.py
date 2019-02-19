from django.urls import path, include
from . import views
from rest_framework import routers
from. views import WorkerCreateView, WorkerDetailView, WorkerChangeView, WorkerDeleteView, StandardsView, SchedulesCreateView, SchedulesChangeView, SchedulesDeleteView
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.views import LogoutView





urlpatterns = [
    path('api/report/', views.ReportView, name='report'),
    path('api/penalty/', views.IssuePenaltyView, name='issue-penalty'),
    path('', views.DashboardView, name='dashboard'),
    path('workers/', views.WorkersView, name='home'),
    path('api/', views.DetailedWorkerView, name='dashboard-api'),
    path('worker/<pk>/view/', WorkerDetailView, name='worker-detail'),
    path('worker/<pk>/change/', login_required(WorkerChangeView.as_view()), name='worker-change'),
    path('worker/add-worker/', WorkerCreateView, name='worker-create'),
    path('worker/<pk>/delete/', login_required(WorkerDeleteView.as_view()), name='worker-delete'),
    path('categories/<pk>/change/', login_required(views.PositionsChangeView.as_view()), name='positions-change'),
    path('categories/<pk>/delete/', login_required(views.PositionsDeleteView.as_view()), name='positions-delete'),
    path('categories/add/', login_required(views.PositionsCreateView.as_view()), name='positions-create'),
    path('categories/view/', views.CategoriesView, name='positions-view'),
    path('schedules/view/', views.SchedulesView, name='schedules-view'),
    path('schedules/add/', views.SchedulesCreateView.as_view(), name='schedules-create'),
    path('schedules/<pk>/change/', login_required(views.SchedulesChangeView.as_view()), name='schedules-change'),
    path('schedules/<pk>/delete/', login_required(views.SchedulesDeleteView.as_view()), name='schedules-delete'),
    path('standards/view/', views.StandardsView, name='standards-view'),
    path('standards/add/', login_required(views.StandardsCreateView.as_view()), name='standards-create'),
    path('standards/<pk>/change/', login_required(views.StandardsChangeView.as_view()), name='standards-change'),
    path('standards/<pk>/delete/', login_required(views.StandardsDeleteView.as_view()), name='standards-delete'),
    path('reports/', views.Reports, name='calendar'),
    path('worker/<pk>/view/api/', views.WorkerStatistics, name='worker-statistics'),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
]



