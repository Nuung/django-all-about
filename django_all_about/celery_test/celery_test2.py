from typing import List
from celery.result import AsyncResult
from celery.canvas import Signature
from apis.test.tasks import check_registration_number_from_hometax

# Signature
stask_1: Signature = check_registration_number_from_hometax.si("1208801280")
stask_2: Signature = check_registration_number_from_hometax.signature(
    args=["3898602190"], ignore_result=False
)
stask_3: Signature = check_registration_number_from_hometax.signature(
    ignore_result=True
)
num_list = ["4535", "23415457463", "3424354673241", "23141", "23435329", "9992"]
task_list: List[Signature] = [
    check_registration_number_from_hometax.si(num) for num in num_list
]

print("# 1. Check SubTask(Signature) UUID")
print(f"task_1 is {stask_1.id}")
print(f"task_2 is {stask_2.id}")
print(f"task_3 is {stask_3.id}")
print(f"task_4 is {task_list}")

# Excute Signature
task_1: AsyncResult = stask_1.delay()
task_2: AsyncResult = stask_2.apply_async(args=[], kwargs={}, countdown=3)
task_3: AsyncResult = stask_3.apply_async(args=["898989"], kwargs={})

print("# 2. SubTask(Signature) Status")
print(f"task_1 is ready? {task_1.ready()}")
print(f"task_2 is ready? {task_2.ready()}")
print(f"task_3 is ready? {task_3.ready()}")

print("# 3. SubTask(Signature) Run and get return")
print(f"task_1 is {task_1.get()}")
print(f"task_2 is {task_2.get()}")
print(f"task_3 is {task_3.get()}")

print("# 4. SubTask(Signature) List Run and get return")
task_list_result = list()
for task in task_list:
    temp = task.delay()
    print(temp.get())
    task_list_result.append(temp)

print("# 5. SubTask(Signature) Status again")
print(f"task_1 is ready? {task_1.ready()}")
print(f"task_2 is ready? {task_2.ready()}")
print(f"task_3 is ready? {task_3.ready()}")
for task in task_list_result:
    print(task.ready())

print("# 6. When is the time task was done")
print(f"task_1 is {task_1.date_done}")
print(f"task_2 is {task_2.date_done}")
print(f"task_3 is {task_3.date_done}")
for task in task_list_result:
    print(task.date_done)
