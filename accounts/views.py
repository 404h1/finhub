from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from .forms import CustomAuthenticationForm, CustomUserCreationForm, CustomUserChangeForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    form = CustomAuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        messages.success(request, f'{form.get_user().get_display_name()}님, 환영합니다!')
        return redirect(request.GET.get('next', '/'))
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, '로그아웃되었습니다.')
    return redirect('accounts:login')

def signup_view(request):
    form = CustomUserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, '회원가입이 완료되었습니다! 🎉')
        return redirect('/')
    return render(request, 'accounts/signup.html', {'form': form})

def user_list(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'accounts/user_list.html', {'users': users})

def user_detail(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'accounts/user_detail.html', {'profile_user': user})

@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {'profile_user': request.user})

@login_required
def profile_edit(request):
    form = CustomUserChangeForm(request.POST or None, request.FILES or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, '프로필이 수정되었습니다.')
        return redirect('accounts:profile')
    return render(request, 'accounts/profile_edit.html', {'form': form})

@login_required
def password_change(request):
    form = PasswordChangeForm(request.user, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        update_session_auth_hash(request, form.save())
        messages.success(request, '비밀번호가 변경되었습니다.')
        return redirect('accounts:profile')
    return render(request, 'accounts/password_change.html', {'form': form})
