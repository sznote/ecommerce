from django.db.models import Q
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.utils import timezone


# Create your views here.


from .models import Product

# https://docs.djangoproject.com/en/1.9/ref/class-based-views/generic-display/
class ProductListView(ListView):
    model = Product
    #queryset = Product.objects.filter(active=False)
    #queryset = Product.objects.all()
    #queryset =  Product.objects.get_queryset()
    queryset = Product.objects.all()

    def get_context_data(self,*args, **kwargs):
        context = super(ProductListView,self).get_context_data(*args, **kwargs)
        #print context
        context["now"] = timezone.now()
        return context

    def get_queryset(self, *arg, **kwargs):
        qs = super(ProductListView, self).get_queryset(*arg, **kwargs)
        query = self.request.GET.get("q")
        if query:
            # qs = self.model.objects.filter(title__contains=query)
            qs = self.model.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )
            try:
                qs2 = self.model.objects.filter(
                    Q(price=query)
                )
                qs = (qs | qs2)#.distinctl()
            except:
                pass
        return qs


class ProductDetailView(DetailView):
    model = Product
    # template_name  = "<appname>/modelname_detail.html"


def product_detail_view_func(request, id):
    # product_instance = Product.objects.get(id=id)
    product_instance = get_object_or_404(Product, id=id)
    try:
        product_instance = Product.objects.get(id=id)
    except Product.DoesNotExist:
        raise Http404
    except:
        raise Http404

    template = "products/product_detail.html"
    context = {
        "object": product_instance
    }

    return render(request, template, context)
