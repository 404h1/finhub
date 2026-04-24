from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from .utils import load_assets, get_asset_by_id
from .models import Post


def asset_list(request):
    """금융 자산 리스트"""
    assets = load_assets()
    return render(request, "community/asset_list.html", {"assets": assets})


def board(request, asset_id):
    """자산별 토론 게시판"""
    asset = get_asset_by_id(asset_id)
    if not asset:
        return render(request, "community/404.html", status=404)
    posts = Post.objects.filter(asset_id=asset_id)
    return render(request, "community/board.html", {"asset": asset, "posts": posts})


def post_detail(request, asset_id, post_id):
    """게시글 상세"""
    asset = get_asset_by_id(asset_id)
    if not asset:
        return render(request, "community/404.html", status=404)
    post = get_object_or_404(Post, id=post_id, asset_id=asset_id)
    # F506: 본인 글 여부 확인
    is_author = request.user.is_authenticated and request.user.username == post.author
    return render(request, "community/post_detail.html", {
        "asset": asset, "post": post, "is_author": is_author,
    })


@login_required
@require_http_methods(["GET", "POST"])
def post_create(request, asset_id):
    """F506: 게시글 작성 — 로그인 필수"""
    asset = get_asset_by_id(asset_id)
    if not asset:
        return render(request, "community/404.html", status=404)

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()
        if title and content:
            Post.objects.create(
                asset_id=asset_id,
                title=title,
                content=content,
                author=request.user.username,  # F506: username 자동 저장
            )
            return redirect("community:board", asset_id=asset_id)
        messages.error(request, "제목과 내용을 모두 입력해주세요.")
    return render(request, "community/post_form.html", {"asset": asset})


@login_required
@require_http_methods(["GET", "POST"])
def post_update(request, asset_id, post_id):
    """F506: 게시글 수정 — 작성자 본인만"""
    asset = get_asset_by_id(asset_id)
    if not asset:
        return render(request, "community/404.html", status=404)
    post = get_object_or_404(Post, id=post_id, asset_id=asset_id)

    # F506: 작성자 검증
    if request.user.username != post.author:
        messages.error(request, "본인이 작성한 게시글만 수정할 수 있습니다.")
        return redirect("community:post_detail", asset_id=asset_id, post_id=post.id)

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()
        if title and content:
            post.title = title
            post.content = content
            post.save()
            return redirect("community:post_detail", asset_id=asset_id, post_id=post.id)
        messages.error(request, "제목과 내용을 모두 입력해주세요.")

    return render(request, "community/post_form.html", {
        "asset": asset, "post": post,
        "title": post.title, "content": post.content, "is_edit": True,
    })


@login_required
@require_http_methods(["POST"])
def post_delete(request, asset_id, post_id):
    """F506: 게시글 삭제 — 작성자 본인만"""
    post = get_object_or_404(Post, id=post_id, asset_id=asset_id)
    if request.user.username != post.author:
        messages.error(request, "본인이 작성한 게시글만 삭제할 수 있습니다.")
        return redirect("community:post_detail", asset_id=asset_id, post_id=post.id)
    post.delete()
    messages.success(request, "게시글이 삭제되었습니다.")
    return redirect("community:board", asset_id=asset_id)
