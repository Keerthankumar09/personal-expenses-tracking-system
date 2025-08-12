from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Expense
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        User.objects.create_user(username=username, password=password)
        return redirect('login')
    return render(request, 'tracker/register.html')

def login_view(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'tracker/login.html')

@login_required
def dashboard(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    return render(request, 'tracker/dashboard.html', {'expenses': expenses})

@login_required
def add_expense(request):
    if request.method == 'POST':
        Expense.objects.create(
            user=request.user,
            amount=request.POST['amount'],
            category=request.POST['category'],
            note=request.POST['note'],
            date=request.POST['date']
        )
        return redirect('dashboard')
    return render(request, 'tracker/add_expense.html')

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def edit_expense(request, id):
    expense = Expense.objects.get(id=id, user=request.user)
    if request.method == 'POST':
        expense.amount = request.POST['amount']
        expense.category = request.POST['category']
        expense.note = request.POST['note']
        expense.date = request.POST['date']
        expense.save()
        return redirect('dashboard')
    return render(request, 'tracker/edit_expense.html', {'expense': expense})

@login_required
def delete_expense(request, id):
    Expense.objects.filter(id=id, user=request.user).delete()
    return redirect('dashboard')

@login_required
def edit_expense(request, id):
    expense = Expense.objects.get(id=id, user=request.user)
    if request.method == 'POST':
        expense.amount = request.POST['amount']
        expense.category = request.POST['category']
        expense.note = request.POST['note']
        expense.date = request.POST['date']
        expense.save()
        return redirect('dashboard')
    return render(request, 'tracker/edit_expense.html', {'expense': expense})

@login_required
def delete_expense(request, id):
    Expense.objects.filter(id=id, user=request.user).delete()
    return redirect('dashboard')

from django.contrib import messages  # ✅ Add this at the top

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')  # ✅ Show message
    return render(request, 'tracker/login.html')
