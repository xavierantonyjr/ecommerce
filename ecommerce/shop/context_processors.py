from .models import Category

def links(request):
    c = Category.objects.all()
    return {'cat':c }