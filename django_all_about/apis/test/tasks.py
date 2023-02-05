# python lib
import logging
from requests import Response
from bs4 import BeautifulSoup

from config.celery import app
from apis.test.models import CheckedCrn
from utils.retry_session import get_retry_session

logger = logging.getLogger(__name__)


@app.task
def check_registration_number_from_hometax(registration_number="1208801280"):

    # logging & test 할 때는 sleep 주고 체크하는게 좋다.
    # from time import sleep
    # sleep(1)

    s = get_retry_session()

    url = "https://teht.hometax.go.kr/wqAction.do"
    querystring = {"actionId": "ATTABZAA001R08"}
    payload = f"""
        <map id="ATTABZAA001R08">
            <pubcUserNo/>
            <mobYn>N</mobYn>
            <inqrTrgtClCd>1</inqrTrgtClCd>
            <txprDscmNo>{registration_number}</txprDscmNo>
            <dongCode>88</dongCode>
            <psbSearch>Y</psbSearch>
            <map id="userReqInfoVO"/>
        </map>
    """

    headers = {"Accept": "application/xml; charset=UTF-8"}
    res: Response = s.post(
        url, data=payload, headers=headers, params=querystring, timeout=2
    )

    # xml return 이라 직접 parsing or parser 필요, bs4 & lxml 활용
    res: BeautifulSoup = BeautifulSoup(res.content, "lxml")
    result: str = res.find("map").find("smpcbmantrtcntn").get_text().strip()
    logger.info(f"{res}, {registration_number}")

    is_closed = True
    if result == "등록되어 있는 사업자등록번호 입니다.":
        is_closed = False

    new_check_crn: CheckedCrn
    try:
        new_check_crn = CheckedCrn(
            registration_number=registration_number, is_closed=is_closed
        )
        new_check_crn.save()
    except Exception:
        return None
    return new_check_crn.__str__()
