from django.db import models

class DepositProduct(models.Model):
    fin_co_no    = models.CharField(max_length=20, verbose_name='금융회사 코드')
    kor_co_nm    = models.CharField(max_length=100, verbose_name='금융회사명')
    fin_prdt_cd  = models.CharField(max_length=50, unique=True, verbose_name='상품 코드')
    fin_prdt_nm  = models.CharField(max_length=200, verbose_name='상품명')
    join_way     = models.CharField(max_length=100, blank=True, verbose_name='가입 방법')
    join_deny    = models.IntegerField(default=1, verbose_name='가입 제한')
    join_member  = models.TextField(blank=True, verbose_name='가입 대상')
    spcl_cnd     = models.TextField(blank=True, verbose_name='우대 조건')
    etc_note     = models.TextField(blank=True, verbose_name='기타 유의사항')
    max_limit    = models.BigIntegerField(null=True, blank=True, verbose_name='최고 한도')
    dcls_month   = models.CharField(max_length=8, blank=True, verbose_name='공시 월')
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '정기예금 상품'
        verbose_name_plural = '정기예금 상품 목록'
        ordering = ['kor_co_nm', 'fin_prdt_nm']

    def __str__(self):
        return f'[{self.kor_co_nm}] {self.fin_prdt_nm}'

    def get_best_rate(self):
        opts = self.options.all()
        if opts.exists():
            return max(o.intr_rate2 or o.intr_rate or 0 for o in opts)
        return 0

    def get_options_by_term(self):
        return self.options.order_by('save_trm')

class DepositOption(models.Model):
    product         = models.ForeignKey(DepositProduct, on_delete=models.CASCADE,
                                        related_name='options')
    fin_prdt_cd     = models.CharField(max_length=50)
    intr_rate_type_nm = models.CharField(max_length=20, blank=True, verbose_name='금리 유형')
    save_trm        = models.IntegerField(verbose_name='저축 기간 (개월)')
    intr_rate       = models.FloatField(null=True, blank=True, verbose_name='기본 금리 (%)')
    intr_rate2      = models.FloatField(null=True, blank=True, verbose_name='최고 우대 금리 (%)')

    class Meta:
        verbose_name = '예금 옵션'
        verbose_name_plural = '예금 옵션 목록'
        ordering = ['save_trm']

    def __str__(self):
        return f'{self.product.fin_prdt_nm} - {self.save_trm}개월'
