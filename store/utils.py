from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def paginatore_objects(request, objects, per_page=3):
    page_number = request.GET.get("page")
    paginator = Paginator(objects, per_page)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return page_obj