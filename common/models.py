from django.db import models


# Create your models here.
class CommonModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 실제 db 에 반영되지 않도록 abstract 설정 !
    class Meta:
        abstract = True
