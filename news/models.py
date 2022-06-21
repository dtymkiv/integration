from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    title = models.TextField(unique=True)
    content = models.TextField(null=False)
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return f'[{self.id}]: {self.title[:15]}'


class Action(models.Model):
    user = models.ForeignKey(User, related_name="actions", on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name="actions", on_delete=models.CASCADE)
    action = models.BooleanField(null=False, default=False)

    def __str__(self):
        return f'{"++" if self.action else "--"} ({self.user.username}) ({str(self.article)})'
