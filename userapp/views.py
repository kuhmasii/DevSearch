from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, get_user


from .forms import RegistrationForm, ProfileForm, SkillForm, ContactForm
from .models import Profile, Skill 
from newapp.models import Project
from .utils import search, userappPaginator


from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail, get_connection


User = get_user_model()

def register(request):
    page = "registration"
    
    if request.user.is_authenticated:
        return redirect('userapp:dashboard')

    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            ins = [form.cleaned_data.get(x.name) for x in form]
            # Be careful in the nearest future a change in the userapp.forms variables can affect 
            # the way user's information is been saved
            user = User(first_name=ins[0].upper(), last_name=ins[1].upper(),
                    username=ins[2], email=ins[4], password=ins[6])
            user.set_password(user.password)
            user.save()
            messages.success(request, "User account was created successfully.")

            login(request, user)
            return redirect('userapp:editDashboard')
        
        else:
            messages.error(request, "An error has occurred during registration")

    context = {'form':form, 'page': page}

    return render(request, "userapp/signup_login.html", context)

def signIn(request):

    if request.user.is_authenticated:
        return redirect('userapp:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist!')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('userapp:dashboard')
        else:
            messages.error(request, f"Invalid details for the user '{username}'")
    return render(request, 'userapp/signup_login.html')

def profiles(request):
    search_profiles = search(request)
    profiles = userappPaginator(request, search_profiles, 3)
    context = {"profiles":profiles}
    return render(request, 'userapp/developers.html', context)

def userProfile(request, username=None):
    profile = Profile.objects.get(user__username=username)
    context = {"profile":profile}
    return render(request, 'userapp/profile.html', context)

@login_required(login_url='userapp:signIn')
def dashboard(request):
    user = get_user(request)
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = {}.fromkeys(['social_github', 'social_twitter',
        'social_linkedin','social_website','short_info', 
        "location"], "'No Data Yet:)'")
    context = {'user':user, 'profile':profile}
    return render(request, 'userapp/account.html', context)

@login_required(login_url='userapp:signIn')
def editDashboard(request):
    profile = Profile.objects.filter(user=get_user(request))

    if profile.exists(): 
        form = ProfileForm(instance=profile[0])
        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES, instance=profile[0])
            if form.is_valid():
                form.save()
                return redirect("userapp:dashboard")
            else:
                messages.error(request, 'There was an error in validating the form.')
    else:
        form = ProfileForm()
        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = get_user(request)
                profile.save()
                return redirect("userapp:dashboard")
            else:
                messages.error(request, 'Error occured during form handling.')
    context = {'form':form}
    return render(request, 'userapp/editpage.html', context)

@login_required(login_url='userapp:signIn')
def create_skill(request):
    profile = Profile.objects.get(user=get_user(request))
    form = SkillForm()
    
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.profile = profile
            skill.save()
            messages.success(request, "Skill added successfully...")
            return redirect("userapp:dashboard")
        else:
            messages.error(request, 'Error during form handling...')

    context = {'form':form}
    return render(request, 'userapp/skill_form.html', context)

@login_required(login_url='userapp:signIn')
def update_skill(request, skill_id):
    try:
        profile = Profile.objects.get(user=get_user(request))
        skill = profile.get_skill(skill_id)
        form = SkillForm(instance=skill)

        if request.method == 'POST':
            form = SkillForm(request.POST, instance=skill)
            if form.is_valid():
                form.save()
                messages.success(request, 'Successfully Updated')
                return redirect('userapp:dashboard')
            else:
                messages.error(request, 'Error occured during form handling.')

        context = {'form':form}
        return render(request, 'userapp/skill_form.html', context)

    except Skill.DoesNotExist:
        print("Skiil does not exist!!!")

@login_required(login_url='userapp:signIn')
def delete_skill(request, skill_id):
    profile = Profile.objects.get(user=get_user(request))
    skill = profile.get_skill(skill_id)
    
    if request.method == "POST":
        skill.delete()
        messages.success(request, 'Successfully Deleted')
        return redirect("userapp:dashboard")

    return render(request, 'delete.html', {"obj":skill})

@login_required(login_url='userapp:signIn')
def signOut(request):
    logout(request)
    messages.info(request, 'User was logged out!')
    return redirect("newapp:index")

def sendMail(request, email_id):
    profile = Profile.objects.get(id=email_id)
    recipient_email = profile.user.email
    
    contact_form = ContactForm()

    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            subject, message = contact_form.get_details()
            send_mail(
                subject=subject,
                message=message,
                from_email= settings.EMAIL_HOST_USER,
                recipient_list=[recipient_email],
                fail_silently=False,
            )
            messages.success(request, f'Email was successfully sent to {recipient_email}.')
            return redirect('userapp:profiles')

    context = {'form':contact_form}
    return render(request, 'contact.html', context)