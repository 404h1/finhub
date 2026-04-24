from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import User

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='아이디',
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': '아이디를 입력하세요'})
    )
    password = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': '비밀번호를 입력하세요'})
    )

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'nickname', 'age', 'password1', 'password2')
        labels = {
            'username': '아이디',
            'email': '이메일',
            'nickname': '닉네임',
            'age': '나이',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control form-control-lg'})

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'nickname', 'age', 'assets', 'salary',
                  'investment_style', 'bio', 'profile_image',
                  'favorite_bank', 'saving_style', 'interest_stocks')
        labels = {
            'email': '이메일',
            'nickname': '닉네임',
            'age': '나이',
            'assets': '보유 자산 (원)',
            'salary': '연봉 (원)',
            'investment_style': '투자 성향',
            'bio': '자기소개',
            'profile_image': '프로필 사진',
            'favorite_bank': '최애 은행',
            'saving_style': '저축 성향',
            'interest_stocks': '관심 종목 (쉼표 구분)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'profile_image':
                field.widget.attrs.update({'class': 'form-control'})
            elif name in ('investment_style', 'saving_style'):
                field.widget.attrs.update({'class': 'form-select form-select-lg'})
            else:
                field.widget.attrs.update({'class': 'form-control form-control-lg'})
