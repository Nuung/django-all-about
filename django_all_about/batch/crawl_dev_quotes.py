import logging
import json
from celery import Task
from datetime import datetime
from requests import Response
from dataclasses import dataclass, asdict
from django.core.cache import cache

from config.celery import app
from utils.retry_session import get_retry_session


logger = logging.getLogger(__name__)


@dataclass
class DevQuote:
    """
    - crawl_dev_quotes_batch 에 활용되는 datamodel
    """

    description: str
    author: str
    author2: str
    created_at: datetime

    def to_dict(self):
        return {k: str(v) for k, v in asdict(self).items()}


@app.task(bind=True)
def crawl_dev_quotes_batch(self: Task):
    """
    - tistory1 api 활용, dev quotes 얻어와서 cache update 하는 batch task
    """
    s = get_retry_session()
    try:
        url = "https://tistory1.daumcdn.net/tistory/4939852/skin/images/quote.json"
        headers = {"Accept": "application/xml; charset=UTF-8"}
        res: Response = s.get(url, headers=headers, timeout=2)
        res: list[dict] = json.loads(res.content)  # encoding이 깨져서 jsonfiy 하는 부분 분리
        dev_quotes_list = list()
        for r in res:
            r["created_at"] = datetime.now()
            dev_quote = DevQuote(**r)  # data 검증, vaildation
            dev_quotes_list.append(dev_quote.to_dict())

        # cache update
        if cache.get("dev-quotes", None) != dev_quotes_list:
            cache.set("dev-quotes", dev_quotes_list, None)
            logger.info("crawl_dev_quotes_batch cache update")
            return dev_quotes_list
        return None
    except Exception as exc:
        logger.warning(f"crawl_dev_quotes_batch exc: {exc}, {exc.with_traceback()}")
        raise exc
