from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.utils.text import slugify


# Create your models here.
class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)


# https://docs.djangoproject.com/en/1.9/topics/db/managers/
class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self, *args, **kwargs):
        return self.get_queryset()


class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    active = models.BooleanField(default=True)

    objects = ProductManager()

    def __unicode__(self):  ##def __str__(self):
        return self.title
        # slug
        # inventory?

    def get_absolute_url(self):
        # return "/products/%s" % (self.pk)
        return reverse("product_detail", kwargs={"pk": self.pk})

        # Product Images


        # Product Category

class Variation(models.Model):
    product = models.ForeignKey(Product)
    title = models.CharField(max_length=120)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    sale_price = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
    active = models.BooleanField(default=True)
    inventory = models.IntegerField(default="-1", null=True, blank=True)  # refer none == unlimited amount

    def __unicode__(self):
        return self.title

    def get_price(self):
        if self.sale_price is None:
            return self.sale_price
        else:
            return self.price

    def get_absolute_url(self):
        return self.product.get_absolute_url()


def product_saved_receiver(sender, instance, created, *args, **kwargs):
    print sender
    product = instance
    variations = product.variation_set.all()
    if variations.count() == 0:
        new_var  = Variation()
        new_var.product = product
        new_var.title = "Default"
        new_var.price = product.price
        new_var.save()

    #variations = product.objects.filter(product=product)
    #print created


post_save.connect(product_saved_receiver, sender=Product)


#
# class Test(models.Model):
#     aname = models.CharField(max_length=120)
#     gname = models.CharField(max_length=120)
#
#     def __unicode__(self):
#         return self.aname

def image_upload_to(instance, filename):
    title = instance.product.title
    slug = slugify(title)
    basename, file_extension = filename.split(".")
    new_filename = "%s-%s.%s"  %(slug, instance.id, file_extension)
    return "products/%s/%s" %(slug, new_filename)


class ProductImage(models.Model):
    product = models.ForeignKey(Product)
    #image = models.ImageField(upload_to='products/')
    image = models.ImageField(upload_to=image_upload_to)

    def __unicode__(self):
        return self.product.title
