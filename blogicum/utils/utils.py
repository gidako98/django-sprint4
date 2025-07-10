from django.core.paginator import Paginator


def paginator(post, request, pages_amount):
    paginator = Paginator(post, pages_amount)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
