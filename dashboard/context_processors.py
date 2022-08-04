from .models import Category, Tag


def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)
