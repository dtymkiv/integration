from graphene_django import DjangoObjectType
from .models import User, Action, Article


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'username', 'actions')
        

class ArticleType(DjangoObjectType):
    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'date_created', 'actions')
