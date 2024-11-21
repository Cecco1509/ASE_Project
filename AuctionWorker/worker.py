from celery import Celery, shared_task
from python_json_config import ConfigBuilder

config = builder.parse_config('/app/config.json')

worker = Celery('auction_worker',
                    broker='amap://admin:mypass@rabbit:5672', 
                    backend=' rpc://')
