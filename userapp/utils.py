from .models import Profile
from django.db.models import Q
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage


def userappPaginator(request, profiles, number):
    
    page_number = request.GET.get('page')
    paginate = Paginator(profiles, number)
    try:
        page_obj = paginate.page(page_number)
    except PageNotAnInteger:
        page_obj = paginate.page(1)
    except EmptyPage:
        page_obj = paginate.page(paginate.num_pages)
        
    return page_obj

def search(request):
    if (q:=request.GET.get('q')):
        
        profiles = Profile.objects.filter(
                Q(user__username__iexact=q)|
                Q(user__first_name__icontains=q)|
                Q(user__last_name__icontains=q)|
                Q(short_intro__icontains=q)
            )
    else:
        profiles = Profile.objects.all()
    return profiles