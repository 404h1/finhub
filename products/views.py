from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from .models import DepositProduct
from .services import fetch_and_save_products

def product_list(request):
    qs = DepositProduct.objects.prefetch_related('options').all()
    bank  = request.GET.get('bank', '').strip()
    term  = request.GET.get('term', '').strip()
    rate_min = request.GET.get('rate_min', '').strip()
    rate_max = request.GET.get('rate_max', '').strip()

    if bank:
        qs = qs.filter(kor_co_nm__icontains=bank)
    if term:
        try:
            qs = qs.filter(options__save_trm=int(term)).distinct()
        except ValueError:
            pass
    if rate_min:
        try:
            qs = qs.filter(options__intr_rate2__gte=float(rate_min)).distinct()
        except ValueError:
            pass
    if rate_max:
        try:
            qs = qs.filter(options__intr_rate2__lte=float(rate_max)).distinct()
        except ValueError:
            pass

    banks = DepositProduct.objects.values_list('kor_co_nm', flat=True).distinct().order_by('kor_co_nm')
    products = list(qs)
    products.sort(key=lambda p: p.get_best_rate(), reverse=True)

    if not products:
        fetch_and_save_products()
        products = list(DepositProduct.objects.prefetch_related('options').all())
        products.sort(key=lambda p: p.get_best_rate(), reverse=True)

    return render(request, 'products/list.html', {
        'products': products,
        'banks': banks,
        'bank': bank, 'term': term, 'rate_min': rate_min, 'rate_max': rate_max,
    })

def product_detail(request, pk):
    product = get_object_or_404(DepositProduct, pk=pk)
    options = product.get_options_by_term()
    return render(request, 'products/detail.html', {'product': product, 'options': options})

@staff_member_required
def fetch_products(request):
    if request.method == 'POST':
        cnt = fetch_and_save_products()
        messages.success(request, f'금융 상품 데이터를 업데이트했습니다. ({cnt}개 신규 저장)')
    return redirect('products:list')
