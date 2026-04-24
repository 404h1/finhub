import json, os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import Post
from .forms import PostForm

def _load_assets():
    path = os.path.join(settings.BASE_DIR, 'data', 'assets.json')
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def _get_asset(asset_id):
    for a in _load_assets():
        if a['id'] == asset_id:
            return a
    return None

def board_home(request):
    assets = _load_assets()
    for a in assets:
        a['post_count'] = Post.objects.filter(asset_id=a['id']).count()
    return render(request, 'boards/home.html', {'assets': assets})

def board_list(request, asset_id):
    asset = _get_asset(asset_id)
    if asset is None:
        from django.http import Http404
        raise Http404("존재하지 않는 자산입니다.")
    posts = Post.objects.filter(asset_id=asset_id).select_related('author').order_by('-created_at')
    return render(request, 'boards/list.html', {'asset': asset, 'posts': posts})

@login_required
def post_create(request, asset_id):
    asset = _get_asset(asset_id)
    if asset is None:
        from django.http import Http404
        raise Http404
    form = PostForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.asset_id = asset_id
        post.author   = request.user
        post.save()
        messages.success(request, '게시글이 등록되었습니다.')
        return redirect('boards:list', asset_id=asset_id)
    return render(request, 'boards/form.html', {'form': form, 'asset': asset, 'action': 'create'})

def post_detail(request, asset_id, pk):
    asset = _get_asset(asset_id)
    if asset is None:
        from django.http import Http404
        raise Http404
    post = get_object_or_404(Post, pk=pk, asset_id=asset_id)
    post.view_count += 1
    post.save(update_fields=['view_count'])
    return render(request, 'boards/detail.html', {'post': post, 'asset': asset})

@login_required
def post_edit(request, asset_id, pk):
    post  = get_object_or_404(Post, pk=pk, asset_id=asset_id)
    asset = _get_asset(asset_id)
    if post.author != request.user:
        messages.warning(request, '본인 게시글만 수정할 수 있습니다.')
        return redirect('boards:detail', asset_id=asset_id, pk=pk)
    form = PostForm(request.POST or None, instance=post)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, '게시글이 수정되었습니다.')
        return redirect('boards:detail', asset_id=asset_id, pk=pk)
    return render(request, 'boards/form.html', {'form': form, 'asset': asset, 'post': post, 'action': 'edit'})

@login_required
def post_delete(request, asset_id, pk):
    post = get_object_or_404(Post, pk=pk, asset_id=asset_id)
    if request.method == 'POST':
        if post.author == request.user:
            post.delete()
            messages.success(request, '게시글이 삭제되었습니다.')
        else:
            messages.warning(request, '본인 게시글만 삭제할 수 있습니다.')
    return redirect('boards:list', asset_id=asset_id)
