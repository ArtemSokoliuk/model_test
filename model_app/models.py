from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __repr__(self):
        return '<Tag(name={})>'.format(self.name)


class Article(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    favourite = models.BooleanField(default=False)
    archive = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag)

    def __repr__(self):
        return '<Article(id={}, title={}, url={}, favourite={}, archive={}, ' \
               'tags={})>'.format(self.id, self.title, self.url,
                                  self.favourite, self.archive,
                                  self.tags.all().__repr__())


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    picture = models.CharField(max_length=500)
    articles = models.ManyToManyField(Article)

    def __repr__(self):
        return '<UserProfile(id={}, user={}, picture={}, articles={})>'.format(
            self.id, self.user, self.picture, self.articles.all().__repr__()
        )
