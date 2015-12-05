from django.db import models
from urllib.parse import quote_plus


class GithubPage(models.Model):
    PAGE_TYPE = (
        ('trending', "Trending"),
        ('repo', "Repository"),
    )
    url = models.URLField(null=False, max_length=255)
    page_type = models.CharField(max_length=10, choices=PAGE_TYPE)
    page = models.FileField(upload_to='uploads/%Y/%m/%d/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TrendingRepository(models.Model):
    url = models.URLField(unique=True, null=False, max_length=255)
    name = models.CharField(null=False, max_length=255)
    language = models.CharField(null=False, max_length=50)
    readme = models.FileField(null=True,blank=True)
    star = models.IntegerField(null=True,blank=True)
    fork = models.IntegerField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "name:{}\tlanguage:{}".format(self.name, self.language)


class TrendingCrawler(models.Model):
    language = models.CharField(max_length=100, null=True, blank=True)
    since = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return "lang={}&since={}".format(self.language, self.since)

    def url(self):
        query = []
        if self.language is not None:
            query.append("l={}".format(quote_plus(self.language)))
        if self.since is not None:
            query.append("since={}".format(quote_plus(self.since)))
        return "https://github.com/trending?" + "&".join(query)
