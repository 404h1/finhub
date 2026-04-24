from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content')
        labels = {'title': '제목', 'content': '내용'}
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': '제목을 입력하세요',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': '내용을 입력하세요.\n\n투자 관련 정보를 나눠보세요. 욕설·비방은 자동으로 차단됩니다.',
            }),
        }
