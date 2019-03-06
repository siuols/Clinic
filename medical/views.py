import barcode
import os,sys
from django.shortcuts import render
from .models import Stock, History
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

class Home(View):
    def get(self, request, *args, **kwargs):
        post = Stock.objects.all()
        context = {
            'post': post,
        }
        return render(request, 'clinic/stock-list.html', context)

class StockDetailView(View):
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

class StockCreateView(View):
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

class StockReport(View):
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