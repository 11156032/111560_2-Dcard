from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.core.files.storage import FileSystemStorage
from django.http import Http404, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
import pytz
from dcard.models import Post, Comment, User  # 確保 User 模型在這裡
from dcard.forms import UserRegistrationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from dcard.models import UserProfile

def homepage(request, slug):
    if not Post.objects.filter(topic_no=slug).exists() and slug != "0":
        raise Http404

    context = {"data": []}
    if slug == "0":
        posts = Post.objects.all()
    else:
        posts = Post.objects.filter(topic_no=slug)

    for post in posts:
        sub_data = {field.name: getattr(post, field.name) for field in post._meta.fields}
        sub_data['comments'] = Comment.objects.filter(post=post)
        context["data"].append(sub_data)

    return render(request, 'homepage.html', context)

def post_detail(request, slug):
    try:
        post = Post.objects.get(post_no=slug)
        return render(request, 'post.html', {'post': post})
    except Post.DoesNotExist:
        return HttpResponse("文章未找到")

def register(request):
    registration_form = UserRegistrationForm()

    if request.method == 'POST' and 'register' in request.POST:
        registration_form = UserRegistrationForm(request.POST)
        if registration_form.is_valid():
            # 檢查電子郵件是否已註冊
            email = registration_form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                messages.error(request, "此電子郵件已註冊，請登入或使用其他電子郵件。")
                return redirect('register')
            
            # 檢查用戶名是否已被使用
            username = registration_form.cleaned_data.get('username')
            if User.objects.filter(username=username).exists():
                messages.error(request, "此用戶名已被使用，請選擇其他用戶名。")
                return redirect('register')
            
            # 保存用戶
            user = registration_form.save(commit=False)
            user.password = make_password(registration_form.cleaned_data['password'])
            user.save()
        
            messages.success(request, '註冊成功，歡迎加入')
            return redirect('register') 
        else:
            messages.error(request, "註冊失敗，請檢查您的輸入。")
            return render(request, 'register.html', {'registration_form': registration_form})  # 返回表單頁面
    else:
        return render(request, 'register.html', {'registration_form': registration_form})  # 返回表單頁面

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # 嘗試查找用戶
        user = User.objects.filter(username=username).first()
        
        if user is not None:
            # 嘗試認證用戶
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user) 
                return redirect('/')  # 登入成功後重定向到首頁
            else:
                messages.error(request, "密碼錯誤，請再試一次。")
        else:
            messages.error(request, "用戶名不存在，請檢查你的用戶名。")
    
    return render(request, 'login.html')

@login_required
def update_comment(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return JsonResponse({"success": False, "error": "留言不存在"}, status=404)

    if comment.user != request.user:
        return JsonResponse({"success": False, "error": "您沒有權限編輯此留言"}, status=403)

    if request.method == 'POST':
        new_content = request.POST.get('content')
        if not new_content:
            return JsonResponse({
                "success": False,
                "error": "留言內容不能為空"
            }, status=400)

        comment.content = new_content
        comment.save()
        return JsonResponse({
            "success": True,
            "message": "留言更新成功！"
        })
    else:
        return JsonResponse({
            "success": False,
            "error": "無效的請求方法"
        }, status=405)

@login_required
def delete_comment(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return JsonResponse({"success": False, "error": "留言不存在"}, status=404)

    if comment.user != request.user:
        return JsonResponse({"success": False, "error": "您沒有權限刪除此留言"}, status=403)

    if request.method == 'POST':
        comment.delete()
        return JsonResponse({
            "success": True,
            "message": "留言已成功刪除！"
        })
    else:
        return JsonResponse({
            "success": False,
            "error": "無效的請求方法"
        }, status=405)

@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    user_profile = UserProfile.objects.get(user = user)

    if request.method == 'POST' and request.FILES.get('profile_picture'):
        profile_picture = request.FILES['profile_picture']
        user_profile.avatar = profile_picture
        user_profile.save()
        messages.success(request, '個人頭貼已更新！')
        return redirect('user_profile', username=username)

    context = {
        'user': user,
        'email': user.email,
        'join_date': user.date_joined,
        'last_login': user.last_login,
        'profile_picture': user_profile.avatar.url
    }
    return render(request, 'user_profile.html', context)
from django.contrib.auth import logout as auth_logout

def logout_view(request):
    auth_logout(request)
    return redirect('/0')

from django.http import JsonResponse

def add_comment(request, post_no):
    if request.method == 'POST' and request.user.is_authenticated:
        content = request.POST.get('comment')
        
        if not content:
            return JsonResponse({'success': False, 'error': '留言內容不能為空'})
        
        try:
            post = Post.objects.get(post_no=post_no)
        except Post.DoesNotExist:
            return JsonResponse({'success': False, 'error': '文章不存在'})
        
        comment = Comment.objects.create(
            post=post,
            user=request.user,
            content=content
        )
        
        taiwan_tz = pytz.timezone('Asia/Taipei')
        if comment.created_at.tzinfo is None:
            comment_created_at = pytz.utc.localize(comment.created_at)
        else:
            comment_created_at = comment.created_at

        comment_created_at = comment_created_at.astimezone(taiwan_tz)

        return JsonResponse({
            'success': True,
            'comment_id': comment.id,
            'content': comment.content,
            'username': comment.user.username,
            'created_at': comment_created_at.strftime("%Y/%m/%d %H:%M")
        })
    else:
        return JsonResponse({'success': False, 'error': '未授權的請求'})

