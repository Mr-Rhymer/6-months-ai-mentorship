import sys
todos = {}  


for j in range(5):
    print("\nTo-Do List:")
    for i, (task, status) in enumerate(todos.items(), 1):
        print(f"{i}. {task.title()} [{status}]")

    
    action = input("\nAdd (a), Mark done (d), Remove (r), Quit (q): ").strip().lower()


    if action == 'q':
        sys.exit()
    elif action == 'a':
        task = input("New task: ").strip()
        todos[task] = "pending"
        priority = input("Priority (high/medium/low): ").lower().strip()
        todos[task] = {"status": "pending", "priority": priority}

       
    elif action == 'd':
        try:
            num = int(input("Task number to mark done: ")) - 1
            task_name = list(todos.keys())[num]
            todos[task_name] = "DONE "
        except:
            print("Invalid!")
    elif action == 'r':
        try:
            num = int(input("Remove number: ")) - 1
            task_name = list(todos.keys())[num]
            del todos[task_name]
        except:
            print("Invalid!")

pending_tasks = [task for task, status in todos.items() if status == "pending"]
if pending_tasks:
    print("\n Your pending tasks are:")
    for task in pending_tasks:
        print(f"  • {task.title()}")
else:
    print("\n No pending tasks! Great job!")

