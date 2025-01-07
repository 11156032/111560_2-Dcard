from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #一對一關聯User
    avatar = models.ImageField(upload_to='avatars/') #頭像

    def __str__(self):
        return self.user.username
    
    @receiver(post_save, sender=User)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        """
        在 User 建立或更新後，自動建立或更新 Profile
        """
        if created:
            # 當新建立 User 時，自動建立對應 Profile
            model_UserProfile = UserProfile()
            model_UserProfile.user = instance
            model_UserProfile.avatar = f"avatars/11156000.jpg"
            model_UserProfile.save()