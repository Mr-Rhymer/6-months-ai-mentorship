todos = {}  

for j in range(6):
    print("\nTo-Do List:")
    for i, (task, task_info) in enumerate(todos.items(), 1):
        # When printing priority
        if task_info["priority"] == "high":
            print(f"{i}. !!! {task.title()} [HIGH PRIORITY] [{task_info['status']}]")
        elif task_info["priority"] == "medium":
            print(f"{i}. {task.title()} [MEDIUM] [{task_info['status']}]")
        else:
            print(f"{i}. {task.title()} [{task_info['status']}]")

    
    action = input("\nAdd (a), Mark done (d), Remove (r), Quit (q): ").strip().lower()

    if action == 'q':
        break
    elif action == 'a':
        task = input("New task: ").strip()
        # When adding with priority
        priority = input("Priority (high/medium/low): ").lower().strip()
        todos[task] = {"status": "pending", "priority": priority}
    elif action == 'd':
        try:
            num = int(input("Task number to mark done: ")) - 1
            task_name = list(todos.keys())[num]
            todos[task_name]["status"] = "DONE"
        except:
            print("Invalid!")
    elif action == 'r':
        try:
            num = int(input("Remove number: ")) - 1
            task_name = list(todos.keys())[num]
            del todos[task_name]
        except:
            print("Invalid!")

pending_tasks = [task for task, task_info in todos.items() if task_info["status"] == "pending"]
if pending_tasks:
    print("\n Your pending tasks are:")
    for task in pending_tasks:
        print(f"  • {task.title()}")
else:
    print("\n No pending tasks! Great job!")

