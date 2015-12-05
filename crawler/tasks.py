from django_crawler_sample.celery import app as celery_app
from django.core.files.base import ContentFile
from crawler.models import *
from crawler.parser import TrendingParser
import requests
from celery.schedules import crontab


@celery_app.task
def run_all_crawler():
    crawlers = TrendingCrawler.objects.all()
    for c in crawlers:
        fetch_trending.delay(c.id)


@celery_app.task(rate_limit="60/m")
def fetch_trending(crawler_id):
    crawler = TrendingCrawler.objects.get(pk=crawler_id)
    resp = requests.get(crawler.url())
    page = GithubPage(
        url=crawler.url(),
        page_type="trending",
    )
    page.page.save("trend_{}.html".format(crawler.id), ContentFile(resp.text))
    page.save()
    parse_trending.delay(page.id)


@celery_app.task
def parse_trending(page_id):
    page = GithubPage.objects.get(pk=page_id)
    parser = TrendingParser(page.page.read())
    for data in parser.parse():
        repo, created = TrendingRepository.objects.get_or_create(
            url=data["url"],
            defaults={
                "name": data["name"],
                "language": data["language"]
            }
        )
        fetch_repository.delay(repo.id)


@celery_app.task(rate_limit="60/m")
def fetch_repository(repo_id):
    repo = TrendingRepository.objects.get(pk=repo_id)
    resp = requests.get(repo.url)
    page = GithubPage(
        url=repo.url,
        page_type="repo",
    )
    page.page.save("repo_{}.html".format(repo.id), ContentFile(resp.text))
    page.save()
    parse_repository.delay(page.id)


@celery_app.task()
def parse_repository(page_id):
    page = GithubPage.objects.get(pk=page_id)
