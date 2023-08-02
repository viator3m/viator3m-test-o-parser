from django.db import models


class Parsing(models.Model):
    date_field = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class Product(models.Model):
    title = models.CharField(max_length=256)
    price = models.IntegerField()
    link = models.URLField(max_length=512)
    parsing = models.ForeignKey(
        'Parsing',
        on_delete=models.CASCADE,
        related_name='products',
    )

    def __str__(self):
        return self.title[:100]
