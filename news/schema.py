import imp
from importlib.metadata import requires
import graphene
from .types import UserType, ArticleType
from .models import Action, Article, User

class Query(graphene.ObjectType):
    all_articles = graphene.List(ArticleType)
    all_users = graphene.List(UserType)
    articles_by_action = graphene.List(ArticleType, username=graphene.String(required=True), action=graphene.Int(required=True)) 

    def resolve_all_articles(root, info):
        # We can easily optimize query count in the resolve method
        return Article.objects.all()

    def resolve_articles_by_action(root, info, username, action):
        try:
            user = User.objects.get(username=username)
            actions = Action.objects.filter(action=action, user=user)
            return [a.article for a in actions]
        except User.DoesNotExist:
            return None


class ActionMutation(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        article_id = graphene.Int(required=True)
        action = graphene.Int(required=True)

    article = graphene.Field(ArticleType)

    @classmethod
    def mutate(cls, root, info, username, article_id, action):
        user = User.objects.get(username=username)
        article = Article.objects.get(pk=article_id)
        action_obj = Action.objects.filter(user=user, article=article, action=bool(action))
        if action_obj:
            action_obj[0].delete()
        else:
            action_obj, created = Action.objects.get_or_create(user=user, article=article)
            action_obj.action = bool(action)
            action_obj.save()
        
        return ActionMutation(article=article)


class Mutation(graphene.ObjectType):
    update_question = ActionMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
