from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """F501: 커스텀 유저 모델"""
    nickname = models.CharField(max_length=50, verbose_name="닉네임")
    interest_stocks = models.CharField(
        max_length=500, blank=True, verbose_name="관심 종목",
        help_text="쉼표로 구분하여 입력 (예: AAPL, 삼성전자, BTC)"
    )
    profile_image = models.ImageField(
        upload_to="profiles/", blank=True, null=True, verbose_name="프로필 이미지"
    )

    def get_interest_stocks_list(self):
        """관심 종목 문자열 → 리스트 변환"""
        if not self.interest_stocks:
            return []
        return [s.strip() for s in self.interest_stocks.split(",") if s.strip()]

    def __str__(self):
        return self.username
