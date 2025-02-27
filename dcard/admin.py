from dcard.models import Post, UserProfile
from django.contrib import admin

class DcardAdmin(admin.ModelAdmin):
    list_display = ('category', 'title', 'author', 'pub_date')
    
admin.site.register(Post, DcardAdmin)
admin.site.register(UserProfile)