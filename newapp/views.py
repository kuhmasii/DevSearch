import imp
from webbrowser import get
from django.contrib import messages
from django.shortcuts import render,redirect
from .models import Project, Tag
from userapp.models import Profile
from django.contrib.auth import get_user
from .forms import ProjectForm, ReviewForm
from django.contrib.auth.decorators import login_required
from .utils import search, newappPaginator


def index(request):
    search_prj = search(request)
    projects = newappPaginator(request, search_prj, 3)
    context = {"projects": projects}
    return render(request, 'newapp/projectpage.html',context)

def detail(request, detail_id):
    user = get_user(request)

    warning, caution = None, None

    if not user.is_anonymous:
        profile = Profile.objects.get(user=user)
    try:
        project = Project.objects.get(id=detail_id)
        form = ReviewForm()
        
        if not user.is_anonymous:
            if profile.id in project.get_reviews():
                warning = "You have already submitted your review for this project"
            if profile == project.owner:
                caution = "You cannot review your own work"

        
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            review = form.save(commit=False)
            review.owner = profile
            review.project = project
            review.save()

            project.getVote
        
            messages.success(request, 'Your review has been successfully submitted')
            return redirect('newapp:index')

        context = {"project":project, 'form':form, 'user':user, 'warning':warning, 'caution':caution}
        return render(request, 'newapp/projectdetail.html', context)


    except Project.DoesNotExist:
        print("Project not in database!!!")

@login_required(login_url='userapp:signIn')
def create_project(request):
    profile = Profile.objects.get(user=get_user(request))
    form = ProjectForm()
    if request.method == "POST":
        tags = request.POST.get("newtags").replace(",", " ").split()
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()

            for tag_ in tags:
                tag, created = Tag.objects.get_or_create(name=tag_)
                project.tag.add(tag)

            return redirect("userapp:dashboard")

    context = { "form":form }
    return render(request, 'newapp/projectform.html', context)

@login_required(login_url='userapp:signIn')
def update_project(request, detail_id):
    profile = Profile.objects.get(user=get_user(request))
    project = profile.get_project(detail_id)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect("userapp:dashboard")
 
    context = {'form':form,}
    return render(request, 'newapp/projectform.html', context)

@login_required(login_url='userapp:signIn')
def delete_project(request, detail_id):
    profile = Profile.objects.get(user=get_user(request))
    project = profile.get_project(detail_id)
    
    if request.method == "POST":
        project.delete()
        return redirect("userapp:dashboard")

    return render(request, 'delete.html', {"obj":project})

    # project such excess rabbit measure earn 
    # original habit chair become swarm family