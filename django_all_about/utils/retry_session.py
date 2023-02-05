from requests import Session
from requests.adapters import HTTPAdapter, Retry


def get_retry_session() -> Session:
    """
    - request 모듈에서 제공해주는 adapter pattern 활용
    - retry 내장 request session object 만들기
    """
    retries_number = 3
    backoff_factor = 0.3
    status_forcelist = (500, 400)

    retry = Retry(
        total=retries_number,
        read=retries_number,
        connect=retries_number,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    session = Session()
    session.mount("http://", HTTPAdapter(max_retries=retry))
    return session
