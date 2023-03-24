from celery import Celery

broker_url = 'amqp://guest:guest@localhost:5672//'
result_backend = 'rpc://'

app = Celery('web_crawler', broker=broker_url, backend=result_backend)

app.conf.task_serializer = 'json'
app.conf.result_serializer = 'json'
app.conf.accept_content = ['json']

app.conf.task_routes = {
    'tasks.crawl_worker': {'queue': 'crawl_worker'}
}

app.conf.update(
    include=[
        'web_crawler.tasks',
    ],
)


