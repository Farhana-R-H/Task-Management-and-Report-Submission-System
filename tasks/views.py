from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from .models import Task, User 
from .forms import TaskCompletionForm, EditProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils import timezone

User = get_user_model()

from datetime import date


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        
        if not username or not email or not password1:
            messages.error(request, "All fields are required.")
            return redirect('signup')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('signup')

        
        role = 'user'
        

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            role=role
        )

        messages.success(request, f"Account created successfully as {role}. Please login.")
        return redirect('login')

    return render(request, 'tasks/signup.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect_role_home(request.user)

    next_url = request.GET.get('next', '')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        remember = bool(request.POST.get('remember'))
        next_url = request.POST.get('next') or request.GET.get('next', '')

        user = authenticate(request, username=username, password=password)
        if user:
            if not user.is_active:
                messages.error(request, "Account disabled. Contact admin.")
                return redirect('login')
            
            login(request, user)

           
            if remember:
                request.session.set_expiry(settings.SESSION_COOKIE_AGE)
            else:
                request.session.set_expiry(0)

           
            if next_url:
                return redirect(next_url)
            return redirect_role_home(user)
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'tasks/login.html', {'next': next_url})

def redirect_role_home(user):
    if user.is_superuser:
        return redirect('superadmin_home')  
    if user.role == 'superadmin':
        return redirect('superadmin_home')
    if user.role == 'admin':
        return redirect('admin_home')
    return redirect('home') 



def password_reset_request(request):
    
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
            request.session['reset_user_id'] = user.id  
            return redirect('password_reset_new')
        except User.DoesNotExist:
            messages.error(request, "Email not registered.")
            return redirect('password_reset_request')

    return render(request, 'tasks/password_reset_request.html')


def password_reset_new(request):
    
    user_id = request.session.get('reset_user_id')
    if not user_id:
        messages.error(request, "Please enter your email first.")
        return redirect('password_reset_request')

    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
        else:
            user.set_password(password)
            user.save()
            messages.success(request, "Password updated successfully. You can login now.")
            request.session.pop('reset_user_id', None)
            return redirect('login') 

    return render(request, 'tasks/password_reset_new.html', {'user_email': user.email})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    User = get_user_model()
    
    current_user = request.user if request.user.is_authenticated else User.objects.first()
    
   
    active_tasks = Task.objects.filter(
        assigned_to=current_user,
        status__in=['pending', 'inprogress']
    )
    
    recent_completed_tasks = Task.objects.filter(
        assigned_to=current_user,
        status='completed'
    ).order_by('-id')[:5]
    
    total_tasks = Task.objects.filter(assigned_to=current_user).count()
    completed_tasks = Task.objects.filter(assigned_to=current_user, status='completed').count()
    pending_tasks = Task.objects.filter(assigned_to=current_user, status='pending').count()
    due_today_tasks = Task.objects.filter(assigned_to=current_user, status='pending', due_date=date.today()).count()
    
    
    
    context = {
        'active_tasks': active_tasks,
        'recent_completed_tasks': recent_completed_tasks,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'due_today_tasks': due_today_tasks,
       
       
    }
    
    return render(request, 'tasks/home.html', context)
def my_tasks(request):
    user = request.user  
    tasks = Task.objects.filter(assigned_to=user)  
    return render(request, 'tasks/my_tasks.html', {'tasks': tasks})

def complete_task(request, task_id):
   
    task = get_object_or_404(Task, id=task_id, assigned_to=request.user)
    
    if request.method == 'POST':
        form = TaskCompletionForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.status = 'completed' 
            task.completed_date = timezone.now() 
            task.save()
            return redirect('home') 
    else:
        form = TaskCompletionForm(instance=task)
    
    return render(request, 'tasks/complete_task.html', {'form': form, 'task': task})


def view_completed_task(request, task_id):
    
    task = get_object_or_404(Task, id=task_id, status='completed')
    return render(request, 'tasks/completed_task.html', {'task': task})


def view_report(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'tasks/view_report.html', {'task': task})

@login_required
def admin_home(request):
    
    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(status='completed').count()
    pending_tasks = Task.objects.filter(status='pending').count()
    reports_count = Task.objects.exclude(completion_report="").count()
    all_users_count = User.objects.filter(is_active=True).count()

   
    tasks = Task.objects.all()

   
    reports = Task.objects.filter(status='completed')

   
    users = list(User.objects.filter(role='user').values_list('username', flat=True))
    tasks_per_user = [
        Task.objects.filter(assigned_to__username=u, status='completed').count()
        for u in users
    ]
    task_status_distribution = [
        Task.objects.filter(status='pending').count(),
        Task.objects.filter(status='inprogress').count(),
        Task.objects.filter(status='completed').count()
    ]

   
    users_list = User.objects.filter(role='user')  
    all_users = User.objects.filter(role='user')   

   
    context = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'reports_count': reports_count,
        'tasks': tasks,
        'reports': reports,
        'users': users,
        'tasks_per_user': tasks_per_user,
        'task_status_distribution': task_status_distribution,
        'users_list': users_list,
        'all_users': all_users,   
         'all_users_count': all_users_count,
    }

    return render(request, 'tasks/admin_home.html', context)

def assign_task(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        assigned_to_id = request.POST.get("assigned_to")
        due_date = request.POST.get("due_date")

        assigned_to = User.objects.get(id=assigned_to_id)

        
        Task.objects.create(
            title=title,
            description=description,
            assigned_to=assigned_to,
            due_date=due_date if due_date else None,
            status="pending",
            created_by=request.user  
        )
        return redirect("admin_home")  

   
    users_list = User.objects.filter(role="user")  
    return render(request, "tasks/admin_home.html", {"users_list": users_list})

@login_required

def superadmin_home(request):
    users = User.objects.all()   
    admins = User.objects.filter(role='admin')

   
    total_users = User.objects.filter(role='user').count()
    total_admins = User.objects.filter(role='admin').count()
    total_tasks = Task.objects.count()
    total_reports = Task.objects.exclude(completion_report='').count()
    all_users_count = User.objects.filter(is_active=True).count()
    

    all_users = User.objects.filter(role='user')
    all_tasks = Task.objects.all()

   
    admin_users = User.objects.filter(role='admin')
    admin_usernames = list(admin_users.values_list('username', flat=True))

  
    tasks_completed_per_admin = []
    for admin in admin_users:
       
        single_tasks_completed = Task.objects.filter(assigned_to=admin, status='completed').count()

        

    

   
    task_status_distribution = [
        Task.objects.filter(status='pending').count(),
        Task.objects.filter(status='inprogress').count(),
        Task.objects.filter(status='completed').count(),
    ]

    context = {
        'users': users,   
        'total_users': total_users,
        'total_admins': total_admins,
        'total_tasks': total_tasks,
        'total_reports': total_reports,
        'all_users': all_users,
        'all_tasks': all_tasks,
        'admin_usernames': admin_usernames,
        'tasks_completed_per_admin': tasks_completed_per_admin,
        'task_status_distribution': task_status_distribution,
        'all_users_count': all_users_count,
    }

    return render(request, 'tasks/superadmin_home.html', context)

def all_reports(request):
   
    task_reports = Task.objects.filter(assigned_to=request.user, status='completed')
    return render(request, 'tasks/all_report.html', {'task_reports': task_reports})


def assign_task(request):
    users_list = User.objects.filter(role='user')

    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        task_type = request.POST.get('task_type')
        due_date = request.POST.get('due_date') or date.today()

        if task_type == 'single':
            assigned_user_id = request.POST.get('assigned_to')
            assigned_user = User.objects.get(id=assigned_user_id)
            task = Task.objects.create(
                title=title,
                description=description,
                assigned_to=assigned_user,
                due_date=due_date,  
                created_by=request.user  
            )
        else:  
            task = Task.objects.create(
                title=title,
                description=description,
                due_date=due_date,  
                created_by=request.user
            )
            team_ids = request.POST.getlist('assigned_to_team')
            for user_id in team_ids:
                user = User.objects.get(id=user_id)
                task.assigned_to_team.add(user)

        messages.success(request, "Task assigned successfully!")
        return redirect('admin_home')

    return render(request, 'tasks/assign_task.html', {'users_list': users_list})


def manage_admin_view(request):
    users = User.objects.all()
    
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        action = request.POST.get("action")
        user = get_object_or_404(User, id=user_id)

        if action == "promote":
            user.role = "admin"
            user.save()
            messages.success(request, f"{user.username} promoted to Admin.")
        elif action == "demote":
            user.role = "user"
            user.save()
            messages.warning(request, f"{user.username} removed from Admin role.")
        
        return redirect("superadmin_home")

    return render(request, "tasks/manage_admin.html", {"users": users})





def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('superadmin_home')
    else:
        form = EditProfileForm(instance=user)

    return render(request, 'tasks/edit_profile.html', {'form': form})
def superadmin_task_management(request):
   
    tasks = Task.objects.all().order_by('-due_date') 

    context = {
        'tasks': tasks,
    }
    return render(request, 'tasks/superadmin_task_management.html', context)


def admin_assigned_tasks(request):
   
    tasks = Task.objects.filter(created_by=request.user).order_by('-due_date')

    context = {
        'tasks': tasks,
    }
    return render(request, 'tasks/admin_assigned_tasks.html', context)


def all_users_view(request):
    if not request.user.is_superuser:
        messages.error(request, "Access denied!")
        return redirect("home")
    users = User.objects.all()
    return render(request, "tasks/all_users.html", {"users": users})

def delete_user_view(request):
    if request.method == "POST" and request.user.is_superuser:
        user_id = request.POST.get("user_id")
        user = get_object_or_404(User, id=user_id)
        user.delete()
        messages.success(request, f"User '{user.username}' deleted successfully.")
    return redirect("all_users")