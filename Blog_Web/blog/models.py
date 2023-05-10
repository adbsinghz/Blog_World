from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    likes = models.ManyToManyField(User, related_name= 'blog_post_like')
    
    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})
    
    def totallLikes(self):
        return self.likes.count()
    
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name= 'blog_post_comments', on_delete = models.CASCADE)
    name = models.CharField(max_length=80)
    body = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return '%s - %s' % (self.post.title, self.name)
    
    