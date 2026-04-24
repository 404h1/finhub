from django.db import models
from django.contrib.auth.models import AbstractUser

INVESTMENT_STYLES = [
    ('aggressive', '공격 투자형'),
    ('growth', '성장 추구형'),
    ('balanced', '위험 중립형'),
    ('stable', '안정 추구형'),
    ('conservative', '안정형'),
]

SAVING_STYLES = [
    ('short', '단기 (1년 미만)'),
    ('mid', '중기 (1~3년)'),
    ('long', '장기 (3년 이상)'),
]

class User(AbstractUser):
    nickname    = models.CharField(max_length=50, blank=True, verbose_name='닉네임')
    age         = models.PositiveIntegerField(null=True, blank=True, verbose_name='나이')
    assets      = models.BigIntegerField(null=True, blank=True, verbose_name='자산 (원)')
    salary      = models.BigIntegerField(null=True, blank=True, verbose_name='연봉 (원)')
    investment_style = models.CharField(max_length=20, choices=INVESTMENT_STYLES,
                                        default='balanced', verbose_name='투자 성향')
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True,
                                      verbose_name='프로필 사진')
    bio         = models.TextField(blank=True, verbose_name='자기소개')
    favorite_bank = models.CharField(max_length=50, blank=True, verbose_name='최애 은행')
    saving_style  = models.CharField(max_length=10, choices=SAVING_STYLES,
                                     default='mid', verbose_name='저축 성향')
    interest_stocks = models.CharField(max_length=200, blank=True, verbose_name='관심 종목')

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = '사용자 목록'

    def __str__(self):
        return self.nickname or self.username

    def get_display_name(self):
        return self.nickname or self.username
