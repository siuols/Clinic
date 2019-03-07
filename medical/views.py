import barcode
import os,sys
from django.shortcuts import render
from .models import Stock, History, Patient
from barcode.writer import ImageWriter
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.utils import timezone
from .forms import (
        DepartmentForm,
        CourseForm,
        PatientForm,
        HistoryForm,
        StockForm,
        RegistrationForm
    )

from .render import Render
# Create your views here.

class Home(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post = Stock.objects.all()
        context = {
            'post': post,
        }
        return render(request, 'clinic/stock-list.html', context)

class HistoryList(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post = History.objects.all()
        context = {
            'post': post,
        }
        return render(request, 'clinic/history-list.html', context)

class StockDetailView(LoginRequiredMixin, View):
    def get(self, request, number, *args, **kwargs):
        item_detail = get_object_or_404(Stock, number = number)
        context = {
            'item_detail': item_detail
        }
        return render(request, 'clinic/stock-detail.html', context)

class DepartmentCreateView(LoginRequiredMixin, View):
    form_class = DepartmentForm
    initial = {'key': 'value'}
    template_name = 'clinic/department-create.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('medical:stock-list')
        else:
            form = DepartmentForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

class CourseCreateView(LoginRequiredMixin, View):
    form_class = CourseForm
    initial = {'key': 'value'}
    template_name = 'clinic/course-create.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('medical:stock-list')
        else:
            form = CourseForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

class PatientList(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post = Patient.objects.all()
        context = {
            'post': post,
        }
        return render(request, 'clinic/patient-list.html', context)

class PatientDetailView(LoginRequiredMixin, View):
    def get(self, request, id_number, *args, **kwargs):
        patient_detail = get_object_or_404(Patient, id_number = id_number)
        context = {
            'patient_detail': patient_detail
        }
        return render(request, 'clinic/patient-detail.html', context)

class PatientCreateView(LoginRequiredMixin, View):
    form_class = PatientForm
    initial = {'key': 'value'}
    template_name = 'clinic/patient-create.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('medical:stock-list')
        else:
            form = PatientForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

class StockCreateView(LoginRequiredMixin, View):
    form_class = StockForm
    initial = {'key': 'value'}
    template_name = 'clinic/stock-create.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            bcode = post.number
            ean = barcode.get('Code39', bcode, writer=ImageWriter())
            filename = ean.save('live-static/media-root/'+bcode)
            post.barcode = bcode + '.png'
            post.actual_used = 0
            post.save()
            return redirect('medical:stock-list')
        else:
            form = StockForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

class HistoryCreateView(LoginRequiredMixin, View):
    form_class = HistoryForm
    initial = {'key': 'value'}
    template_name = 'clinic/history-create.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            itemcode = post.item_code
            q = Stock.objects.get(number=itemcode)
            leftItem = q.quantity - post.quantity
            usedItem = q.actual_used
            b = usedItem + post.quantity
            q.quantity = leftItem
            q.actual_used = b
            q.save()
            post.save()
            return redirect('medical:stock-list')
        else:
            form = HistoryForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

def stock_edit(request,number):
    post_item = Stock.objects.all()
    post = get_object_or_404(Stock, number=number)
    if request.method == "POST":
        form = StockForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('stock:item-detail', number=number)
    else:
        form = StockForm(instance=post)
    context = {
        'form': form,
    }
    return render(request, 'clinic/stock-edit.html', context)

class RegisterFormView(LoginRequiredMixin, View):
    form_class = RegistrationForm
    initial = {'key': 'value'}
    template_name = 'registration/register.html'

    def get(self, request, *args, **kwargs):
        user_form = self.form_class(initial=self.initial)
        context = {
            'user_form': user_form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_form = self.form_class(request.POST)
        if user_form.is_valid():
            user_form.save()
            username = user_form.cleaned_data.get('username')
            raw_password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('medical:stock-list')
        else:
            form = RegistrationForm()
        context = {
            'user_form': user_form,
        }
        return render(request, self.template_name, context)

class StockReport(LoginRequiredMixin, View):
    def get(self, request):
        item = Stock.objects.all()
        today = timezone.now()
        user  = request.user
        params = {
            'today': today,
            'user':user,
            'item': item,   
        }
        return Render.render('report/stock.html', params)

class HistoryReport(View):
    def get(self, request):
        item = History.objects.all()
        today = timezone.now()
        user  = request.user
        params = {
            'today': today,
            'user':user,
            'item': item,   
        }
        return Render.render('report/patient-history.html', params)

class PerPatientReport(View):
    def get(self, request, pk, *args, **kwargs):
        item = get_object_or_404(History, pk=pk)
        today = timezone.now()
        params = {
            'today': today,
            'item': item,            
            'request': request
        }
        return Render.render('report/patient-history.html', params)