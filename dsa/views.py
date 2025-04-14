from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.contrib import messages
import uuid
from datetime import timedelta
from django.utils.timezone import now

from .forms import UserRegisterForm, UserLoginForm
from .models import User, EmailVerification


class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        # Создаем запись для подтверждения email
        expiration = now() + timedelta(hours=48)
        record = EmailVerification.objects.create(
            user=user,
            code=uuid.uuid4(),
            expiration=expiration
        )
        # Отправляем письмо с подтверждением
        send_mail(
            'Подтверждение email',
            f'Для подтверждения email перейдите по ссылке: http://127.0.0.1:8000/users/verify/{record.code}/',
            'from@example.com',
            [user.email],
            fail_silently=False,
        )
        messages.success(self.request, 'Регистрация прошла успешно! Проверьте ваш email для подтверждения.')
        return response


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы успешно вошли в систему.')
            return redirect('index')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('index')


def email_verification(request, code):
    try:
        record = EmailVerification.objects.get(code=code)
        if record.is_expired():
            messages.error(request, 'Ссылка для подтверждения email устарела.')
        else:
            user = record.user
            user.email_verified = True
            user.save()
            record.delete()
            messages.success(request, 'Ваш email успешно подтвержден!')
    except EmailVerification.DoesNotExist:
        messages.error(request, 'Неверный код подтверждения.')
    return redirect('index')



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Product, Cart
from .forms import RegisterForm

def index(request):
    products = Product.objects.all()[:4]
    return render(request, 'shop/index.html', {'products': products})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})

@login_required
def profile(request):
    return render(request, 'shop/profile.html')

def about(request):
    return render(request, 'shop/about.html')

@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)
    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total': total})

def auth_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'shop/auth.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'shop/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')