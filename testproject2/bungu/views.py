from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from .forms import PostCreateForm, CommentCreateForm
from django.views.generic import (
    ListView, DeleteView, CreateView, DetailView, UpdateView, TemplateView,)
from .models import Sirase, Post, Search, Comment
from django.utils import timezone

def index_view(request):
    object_list = Post.objects.order_by('-id')#新着順
    return render(request, 'bungu/index.html')

class ListContactView(ListView):
    template_name = 'bungu/contact.html'
    model = Sirase

class ListBlogView(ListView):
    template_name = 'bungu/post_list.html'
    model = Post
    fields = ("title","text","date",'category',"thumbnail")
    ordering = ['-date']
    paginate_by = 5

class ListItemView(ListView):
    template_name = 'bungu/item.html'
    model = Post
    fields = ("title","text","date",'category',"thumbnail")

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['post'] = Post.objects.get(pk=self.kwargs['post_id'])
    #     return context

class CreateBlogView(LoginRequiredMixin, CreateView):
    template_name = 'bungu/create.html'
    model = Post
    fields = ("title","text",'category',"date","thumbnail")
    success_url = reverse_lazy('list_blog')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PostDetailView(DetailView):
    template_name = 'bungu/post_detail.html'
    model = Post

    def PostDetail(request, pk):
        """Article page"""
        detail = get_object_or_404(Post, pk=pk)
        
        context = {
            "detail": detail,
            "comments": Comment.objects.filter(target=detail.id)   #該当記事のコメントだけを渡します。
        }

class PostDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'bungu/post_confirm_delete.html'
    model = Post
    success_url = reverse_lazy('list_blog')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        
        if obj.user != self.request.user:
            raise PermissionDenied#自分以外がデータを触ろうとすると例外処理が起きる
        return obj

class SearchPostView(ListView):
    model = Post
    template_name = 'bungu/search_post.html'
    paginate_by = 3

    def get_queryset(self):
        query = self.request.GET.get('q', None)

        if query is not None:
            qs = super().get_queryset().distinct()
            return qs
        qs = super().get_queryset()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        return context
    
class CommentCreate(CreateView):
    """コメント投稿ページのビュー"""
    template_name = 'bungu/comment_form.html'
    model = Comment
    form_class = CommentCreateForm
 
    def form_valid(self, form):
        post_pk = self.kwargs['pk']
        post = get_object_or_404(Post, pk=post_pk)
        comment = form.save(commit=False)
        comment.target = post
        comment.save()
        return redirect('post_detail', pk=post_pk)
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        return context
    
def delete_comment(request, pk, comment_pk):
    comment = Comment.objects.get(id=comment_pk)
    post_id = pk
    if request.user.id == comment.author.id or \
       request.user.id == comment.post.author.id:
        comment.delete()
    return redirect('blog:article', pk=post_id)
