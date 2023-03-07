import random

from celery import group
from celery.result import GroupResult
from apis.test.tasks import check_registration_number_from_hometax


def generates_number() -> str:
    return "".join(str(random.randint(0, 9)) for _ in range(10))


tasks = [
    check_registration_number_from_hometax.si(generates_number()) for _ in range(20)
]
grouped = group(tasks)
grouped_task: GroupResult = grouped()

print("# 1. Check Tasks")
print(f"tasks is {tasks}")

print("# 2. Check Grouped Tasks and Id")
print(f"grouped_task is {grouped_task}")
print(f"grouped_tasks's id is {grouped_task.id}")

print("# 3. Check Grouped Tasks's Status")
print(f"grouped_task status is {grouped_task.ready()}")

print("# 4. Check result of Grouped Task")
print(f"How many tasks are compeleted >> {grouped_task.completed_count()}")
print(f"Get the result of grouped_task >> {grouped_task.get()}")
print(f"Get grouped_task.join() >> {grouped_task.join()}")
print(f"How many tasks are compeleted again >> {grouped_task.completed_count()}")

print("# 5. Check Grouped Tasks's Status again")
print(f"grouped_task status is {grouped_task.ready()}")
print(f"Success status >> {grouped_task.successful()}")
print(f"Faile status >> {grouped_task.failed()}")
