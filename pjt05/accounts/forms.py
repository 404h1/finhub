from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import User

STOCK_CHOICES = [
    ("AAPL", "Apple (AAPL)"),
    ("TSLA", "Tesla (TSLA)"),
    ("GOOGL", "Google (GOOGL)"),
    ("MSFT", "Microsoft (MSFT)"),
    ("AMZN", "Amazon (AMZN)"),
    ("NFLX", "Netflix (NFLX)"),
    ("삼성전자", "삼성전자"),
    ("SK하이닉스", "SK하이닉스"),
    ("카카오", "카카오"),
    ("네이버", "NAVER"),
    ("BTC", "Bitcoin (BTC)"),
    ("ETH", "Ethereum (ETH)"),
]


class CustomUserCreationForm(UserCreationForm):
    """F502: 회원가입 폼"""
    nickname = forms.CharField(
        label="닉네임", max_length=50,
        widget=forms.TextInput(attrs={"placeholder": "표시될 닉네임"}),
    )
    profile_image = forms.ImageField(
        label="프로필 이미지", required=False,
    )
    interest_stocks = forms.MultipleChoiceField(
        label="관심 종목", choices=STOCK_CHOICES, required=False,
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "nickname", "profile_image", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.nickname = self.cleaned_data["nickname"]
        # 다중 선택 → 쉼표 구분 문자열로 저장
        selected = self.cleaned_data.get("interest_stocks", [])
        user.interest_stocks = ", ".join(selected)
        if commit:
            user.save()
        return user


class CustomPasswordChangeForm(PasswordChangeForm):
    """F505: 비밀번호 변경 폼 — 한글 오류 메시지"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].label = "현재 비밀번호"
        self.fields["new_password1"].label = "새 비밀번호"
        self.fields["new_password2"].label = "새 비밀번호 확인"
        self.error_messages.update({
            "password_incorrect": "현재 비밀번호가 올바르지 않습니다.",
            "password_mismatch": "새 비밀번호가 일치하지 않습니다.",
        })
