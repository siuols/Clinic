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
        HistoryReport
    )

app_name='clinic'

urlpatterns = [
    path('', Home.as_view(), name='stock-list'),
    path('stock/detail/<str:number>/', StockDetailView.as_view(), name='stock-detail'),
    path('create/', StockCreateView.as_view(), name='stock-create'),
    path('create/depatment', DepartmentCreateView.as_view(), name='department-create'),
    path('create/course', CourseCreateView.as_view(), name='course-create'),
    path('create/patient', PatientCreateView.as_view(), name='patient-create'),
    path('report/stock', StockReport.as_view(), name='stock-report'),
    path('report/history', HistoryReport.as_view(), name='history-report'),
]