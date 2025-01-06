from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    post_no = models.CharField(max_length=100)
    category = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)
    topic_no = models.CharField(max_length=20)
    
    class Meta:
        ordering = ('-pub_date',)
        
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-created_at',)
        
    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"