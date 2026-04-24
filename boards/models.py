from django.db import models
from django.conf import settings

class Post(models.Model):
    asset_id   = models.CharField(max_length=50, verbose_name='자산 코드')
    title      = models.CharField(max_length=200, verbose_name='제목')
    content    = models.TextField(verbose_name='내용')
    author     = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_DEFAULT,
        default=1,
        related_name='posts',
        verbose_name='작성자',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')
    is_filtered = models.BooleanField(default=False, verbose_name='필터링됨')
    view_count  = models.PositiveIntegerField(default=0, verbose_name='조회수')

    class Meta:
        ordering = ['-created_at']
        verbose_name = '게시글'
        verbose_name_plural = '게시글 목록'

    def __str__(self):
        return self.title
