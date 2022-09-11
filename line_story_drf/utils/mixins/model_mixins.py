from django.db import models


class CreatedAtMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        abstract = True
