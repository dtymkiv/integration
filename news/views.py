from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, logout, login
from django.core.paginator import Paginator
from python_graphql_client import GraphqlClient
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page

from .models import Article
from .celery_tasks import get_recent_news

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
ENDPOINT = getattr(settings, 'GRAPHQL_ENDPOINT', "http://127.0.0.1:8000/graphql/")

client = GraphqlClient(endpoint=ENDPOINT)

query = """
query {
  articlesByAction(username: "%s", action: %i) {
    title
  }
}
"""

query_all = """
query {
  allArticles{
    id
    title
    content
    dateCreated
  }
}
"""

mutation = """
mutation {
  updateQuestion(username: "%s", articleId: %i, action: %i){
    article {
      id
    }
  }
}
"""

def add_action(atricles, actions, action):
    for article in atricles:
        for l in actions:
            if l['title'] == article['title']:
                article['has_action'] = True
                article['action'] = action
                break


def feed(request):
    if request.user.is_authenticated:
        data = client.execute(query=query_all)['data']['allArticles']
        liked_posts = client.execute(query=query % (request.user.username, 1))['data']['articlesByAction']
        disliked_posts = client.execute(query=query % (request.user.username, 0))['data']['articlesByAction']
        add_action(data, liked_posts, 1)
        add_action(data, disliked_posts, 0)

        paginator = Paginator(data, 15) # Show 5 articles per page.

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    return render(request, 'news/feed.html', {'page_obj': page_obj})


def set_action(request):
    print("DATA", list(request.POST.keys())[1])
    username = request.user.username
    action, article_id = list(request.POST.keys())[1].split('_')
    action = int(action == 'like')
    mut = mutation % (username, int(article_id), action)
    client.execute(query=mut)
    get_recent_news.delay()

    return redirect('/')


@cache_page(CACHE_TTL)
def get_article(request, article_id):
    article = Article.objects.get(id=article_id)
    article.content = article.content.split('</br>')
    print(article.content)
    return render(request, 'news/article.html', {'article': article})


def login_view(request):
    if request.method.lower() == 'post':
        user = authenticate(
            request=request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            context = {'error_message': 'Incorrect username or password.'}
            return render(request, 'panel/login.html', context)

    return render(request, 'panel/login.html')


def logout_view(request):
    logout(request)
    return redirect('/')