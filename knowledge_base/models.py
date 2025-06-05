from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    category = models.ForeignKey(Category, related_name='faqs', on_delete=models.CASCADE)

    class Meta:
        ordering = ['question']

    def __str__(self):
        return self.question

