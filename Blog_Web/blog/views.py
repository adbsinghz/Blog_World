from typing import Optional
from django.forms.models import BaseModelForm
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import CommentForm
from django.utils import timezone
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
# Create your views here.


def home(request):
    context = {
        'key' : Post.objects.all()
    }
    return render(request,'blog/home.html', context)


class PostListView(ListView):
    
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'key'
    ordering = ['-date_posted']
    
class PostDetailView(DetailView):
    model = Post
    
    def get_context_data(self,*args, **kwargs):
        context = super(PostDetailView, self).get_context_data(*args,**kwargs)
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.totallLikes()
        
        liked = False
        if stuff.likes.filter(id = self.request.user.id).exists():
            liked = True
            
        context['users'] = Post.objects.all()
        context['total_likes'] = total_likes
        context['liked'] = liked
        return context   
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user 
        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user 
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
        
        
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post   
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False 
    
    success_url = '/'
    
def about(request):
    return render(request,'blog/about.html', {'title' : 'About'})


def PostLikeView(request, pk):
    post = get_object_or_404(Post, id = request.POST.get('postLike_id'))
    liked = False
    if post.likes.filter(id = request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))


class PostCommentView(LoginRequiredMixin, CreateView):
    
    model = Comment
    form_class = CommentForm
    template_name = 'blog/add_comments.html'
    def get_context_data(self,*args, **kwargs):
        context = super(PostCommentView, self).get_context_data(*args,**kwargs)
        context['name'] = self.request.user
        return context
    
    def form_valid(self, form):
        form.instance.name = self.request.user
        form.instance.post_id = self.kwargs['pk']
        res = super().form_valid(form)
        return res
    
    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.kwargs['pk']})

class CommentDeleteView(DeleteView):
    model = Comment
    
    template_name = 'blog/delete_comment.html'
    
    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.name:
            return True
        return False

    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Comment, id=id_)

    def get_success_url(self):
        post_id = self.object.post.id
        return reverse_lazy("post-detail", kwargs={"pk": post_id})
