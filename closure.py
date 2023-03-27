from requests import get
from multiprocessing import Pool
import json

from datetime import datetime


def get_detail(id: int):
    url = f"https://yts.mx/api/v2/movie_details.json?movie_id={id}"
    res = get(url)
    res = json.loads(res.content)
    print(res["data"]["movie"]["title_long"])


def get_movie_ids(target_movie_ids: list):
    for page in range(1, 5):
        print(f"PAGE >> {page}")
        url = f"https://yts.mx/api/v2/list_movies.json?page={page}"
        res = get(url)
        res = json.loads(res.content)
        target_movie_ids.extend([movie["id"] for movie in res["data"]["movies"]])


if __name__ == "__main__":
    start_time = datetime.now()
    target_movie_ids = list()
    get_movie_ids(target_movie_ids)

    # type1
    # for id in target_movie_ids:
    #     get_detail(id)

    # type2
    with Pool(processes=14) as p:
        p.map(get_detail, target_movie_ids)
        p.close()

    end_time = datetime.now()
    print(f"total running time >> {end_time - start_time}")
