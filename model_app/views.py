import json
from django.http import HttpResponse
from model_app.models import User, UserProfile, Tag, Article
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


def index(request):
    return HttpResponse("Resp")


@csrf_exempt
def users(request):
    if request.method == 'POST':
        json_request = json.loads(request.body.decode('utf-8'))
        username = json_request.get('username')
        password = json_request.get('password')
        user = User.objects.filter(username=username)
        if not username or not password or user:
            return HttpResponse(status=400)
        user = User(username=username, password=password)
        user.save()
        user_profile = UserProfile(user=user)
        user_profile.save()
        if json_request.get('picture'):
            user_profile.picture = json_request.get('picture')
        return JsonResponse({'user_id': user_profile.id})
    elif request.method == 'GET':
        user_profiles = [{'user_id': user_profile.id}
                         for user_profile in UserProfile.objects.all()]
        return JsonResponse(user_profiles, safe=False)

    return HttpResponse(status=501)


@csrf_exempt
def tags(request):
    if request.method == 'GET':
        tags_group = [{'tag_id': tag.id}
                      for tag in Tag.objects.all()]
        return JsonResponse(tags_group, safe=False)
    elif request.method == 'POST':
        json_request = json.loads(request.body.decode('utf-8'))
        tag_name = json_request.get('name')
        tag = Tag.objects.filter(name=tag_name).first()
        if tag:
            return HttpResponse(status=400)
        tag = Tag(name=tag_name)
        tag.save()
        return JsonResponse({'tag_id': tag.id})

    return HttpResponse(status=501)


@csrf_exempt
def articles(request):
    if request.method == 'GET':
        # TODO: add more filters
        articles_objects = Article.objects.all()
        if request.GET.get('user'):
            articles_objects = articles_objects.filter(
                userprofile=request.GET.get('user'))
        if request.GET.get('tag'):
            articles_objects = articles_objects.filter(
                tags=request.GET.get('tag'))
        articles_group = [{'article_id': article.id,
                           'url': article.url}
                          for article in articles_objects]

        return JsonResponse(articles_group, safe=False)
    elif request.method == 'POST':
        json_request = json.loads(request.body.decode('utf-8'))
        title = json_request.get('title')
        url = json_request.get('url')
        article = Article.objects.filter(url=url).first()
        if not title or not url or article:
            return HttpResponse(status=400)

        article = Article(title=title, url=url)
        article.save()
        if json_request.get('favourite'):
            article.favourite = True
        if json_request.get('archive'):
            article.archive = True
        if json_request.get('users'):
            for user in json_request.get('users'):
                article.userprofile_set.add(user)
        if json_request.get('tags'):
            for tag in json_request.get('tags'):
                article.tags.add(tag)

        print(article)
        return JsonResponse({'article_id': article.id})

    return HttpResponse(status=501)


@csrf_exempt
def tag_id(request, arg_id):
    tag = Tag.objects.filter(id=arg_id).first()
    if not tag:
        return HttpResponse(status=404)
    if request.method == 'GET':
        return JsonResponse({'id': tag.id,
                             'name': tag.name})
    elif request.method == 'DELETE':
        tag.delete()
        return HttpResponse(status=200)
    elif request.method == 'PUT':
        json_request = json.loads(request.body.decode('utf-8'))
        # TODO: check new name
        # if Tag.objects.filter(name=json_request.get('name')):
        #     return HttpResponse(status=400)
        if json_request.get('name'):
            tag.name = json_request.get('name')
        return HttpResponse(status=200)

    return HttpResponse(status=501)


@csrf_exempt
def user_id(request, arg_id):
    user = UserProfile.objects.filter(id=arg_id).first()
    if not user:
        return HttpResponse(status=404)
    if request.method == 'GET':
        return JsonResponse({'id': user.id,
                             'username': user.user.username,
                             'articles': list(map(lambda x: x.id,
                                                  user.articles.all()))})
    elif request.method == 'DELETE':
        user.delete()
        return HttpResponse(status=200)
    elif request.method == 'PUT':
        json_request = json.loads(request.body.decode('utf-8'))
        # TODO: check new username
        # if User.objects.filter(username=json_request.get('username')):
        #     return HttpResponse(status=400)
        if json_request.get('username'):
            user.username = json_request.get('username')
        if json_request.get('password'):
            user.username = json_request.get('password')
        if json_request.get('picture'):
            user.picture = json_request.get('picture')
        return HttpResponse(status=200)

    return HttpResponse(status=501)


@csrf_exempt
def article_id(request, arg_id):
    article = Article.objects.filter(id=arg_id).first()
    if not article:
        return HttpResponse(status=404)
    if request.method == 'GET':
        return JsonResponse({'id': article.id,
                             'url': article.url,
                             'title': article.title,
                             'favourite': article.favourite,
                             'archive': article.archive,
                             'users': list(map(lambda x: x.id,
                                               article.userprofile_set.all())),
                             'tags': list(map(lambda x: x.id,
                                              article.tags.all()))})
    elif request.method == 'DELETE':
        article.delete()
        return HttpResponse(status=200)
    elif request.method == 'PUT':
        json_request = json.loads(request.body.decode('utf-8'))
        # TODO: check new url
        # if Article.objects.filter(url=json_request.get('url')):
        if json_request.get('title'):
            article.title = json_request.request.get('title')
        if json_request.get('url'):
            article.title = json_request.request.get('url')
        if json_request.get('favourite'):
            article.title = json_request.request.get('favourite')
        if json_request.get('archive'):
            article.title = json_request.request.get('archive')
        if json_request.get('users'):
            article.userprofile_set.clear()
            for user in json_request.get('users'):
                article.userprofile_set.add(user)
        if json_request.get('tags'):
            article.tags.clear()
            for tag in json_request.get('tags'):
                article.tags.add(tag)

        return HttpResponse(status=200)

    return HttpResponse(status=501)
