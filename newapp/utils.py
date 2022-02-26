from .models import Project, Tag
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



def newappPaginator(request, projects, number):
    
    page_number = request.GET.get('page')
    paginate = Paginator(projects, number)
    try:
        page_obj = paginate.page(page_number)
    except PageNotAnInteger:
        page_obj = paginate.page(1)
    except EmptyPage:
        page_obj = paginate.page(paginate.num_pages)
        
    return page_obj

def search(request):

    if (q:=request.GET.get('q')):

        projects = Project.objects.filter(
                Q(owner__user__username__iexact=q)|
                Q(title__icontains=q)|
                Q(description__icontains=q)
            )
    else:
        projects = Project.objects.all()
    return projects


    