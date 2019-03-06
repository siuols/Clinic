from django.urls import path

from . import views

from .views import (
        StockCreateView,
        Home,
        StockDetailView,
        CourseCreateView,
        DepartmentCreateView,
        PatientCreateView,
        StockReport,
        HistoryReport,
        stock_edit,
        PatientList,
        PatientDetailView,
        HistoryCreateView,
        PerPatientReport,
        HistoryList
    )

app_name='clinic'

urlpatterns = [
    path('', Home.as_view(), name='stock-list'),
    path('patient', PatientList.as_view(), name='patient-list'),
    path('history', HistoryList.as_view(), name='history-list'),
    path('stock/<str:number>/', views.stock_edit, name='stock-edit'),
    path('patient/detail/<str:id_number>/', PatientDetailView.as_view(), name='patient-detail'),
    path('create/medication', HistoryCreateView.as_view(), name='history-create'),
    path('stock/detail/<str:number>/', StockDetailView.as_view(), name='stock-detail'),
    path('create/', StockCreateView.as_view(), name='stock-create'),
    path('create/depatment', DepartmentCreateView.as_view(), name='department-create'),
    path('create/course', CourseCreateView.as_view(), name='course-create'),
    path('create/patient', PatientCreateView.as_view(), name='patient-create'),
    path('report/stock', StockReport.as_view(), name='stock-report'),
    path('report/history', HistoryReport.as_view(), name='history-report'),
    path('pdf/<int:pk>/', views.PerPatientReport.as_view(), name='per-student-report'),
]