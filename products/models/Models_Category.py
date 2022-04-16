from products.models import *


class Category(models.Model):
    name = models.CharField(max_length=254)
    friendy_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendy_name
    