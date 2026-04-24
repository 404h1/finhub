from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from community.models import Post
from .forms import CustomUserCreationForm, CustomPasswordChangeForm


def signup(request):
    """F502: 회원가입 — 성공 시 자동 로그인"""
    if request.user.is_authenticated:
        return redirect("community:asset_list")
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"{user.nickname}님, 환영합니다!")
            return redirect("community:asset_list")
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/signup.html", {"form": form})


def login_view(request):
    """F503: 로그인"""
    if request.user.is_authenticated:
        return redirect("community:asset_list")
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            next_url = request.GET.get("next", "community:asset_list")
            return redirect(next_url)
        messages.error(request, "아이디 또는 비밀번호가 올바르지 않습니다.")
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    """F504: 로그아웃"""
    if request.method == "POST":
        logout(request)
        messages.success(request, "로그아웃되었습니다.")
    return redirect("community:asset_list")


@login_required
def password_change(request):
    """F505: 비밀번호 변경"""
    if request.method == "POST":
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect("accounts:password_change_done")
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, "accounts/password_change.html", {"form": form})


@login_required
def password_change_done(request):
    """F505: 비밀번호 변경 완료"""
    return render(request, "accounts/password_change_done.html")


@login_required
def profile(request):
    """F507: 프로필 — 유저 정보 + 내가 작성한 게시글"""
    my_posts = Post.objects.filter(author=request.user.username)
    return render(request, "accounts/profile.html", {
        "user": request.user,
        "my_posts": my_posts,
    })
