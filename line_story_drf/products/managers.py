from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class ProductManager(models.Manager):
    def get_product(self, object_id):
        try:
            return self.prefetch_related('product_file').get(id=object_id)
        except ObjectDoesNotExist:
            return None

