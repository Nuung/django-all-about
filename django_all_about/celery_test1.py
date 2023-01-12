from apis.test.tasks import check_registration_number_from_hometax

# delay와 apply_async
task_1 = check_registration_number_from_hometax.delay("1208801280")
task_2 = check_registration_number_from_hometax.apply_async( args=["3898602190"], ignore_result=True )
task_3 = check_registration_number_from_hometax.apply_async( args=["123"], kwargs={} )
 
print("# 1. Task UUID")
print(f"task_1 is {task_1.id}")
print(f"task_2 is {task_2.id}")
print(f"task_3 is {task_3.id}")
 
print("# 2. Task Status")
print(f"task_1 is ready? {task_1.ready()}")
print(f"task_2 is ready? {task_2.ready()}")
print(f"task_3 is ready? {task_3.ready()}")
 
print("# 3. Task Run and get return")
print(f"task_1 is {task_1.get()}")
print(f"task_2 is {task_2.get()}")
print(f"task_3 is {task_3.get()}")
 
print("# 4. Task Status again")
print(f"task_1 is ready? {task_1.ready()}")
print(f"task_2 is ready? {task_2.ready()}")
print(f"task_3 is ready? {task_3.ready()}")
