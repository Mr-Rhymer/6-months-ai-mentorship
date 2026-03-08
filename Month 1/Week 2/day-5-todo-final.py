import json
import os

filename = "todos.json"


if os.path.exists(filename):
    with open(filename, "r") as f:
        todos = json.load(f)
else:
    todos = {}

for j in range(10):
    print("\nTo-Do List:")

    priority_order = {"high": 0, "medium": 1, "low": 2}
    sorted_todos = sorted(todos.items(), key=lambda x: priority_order.get(x[1]["priority"], 3))
    
    for i, (task, task_info) in enumerate(sorted_todos, 1):
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

with open(filename,"w") as f:
    json.dump(todos, f, indent=2)

pending_tasks = [task for task, task_info in todos.items() if task_info["status"] == "pending"]
if pending_tasks:
    print("\n Your pending tasks are:")
    for task in pending_tasks:
        print(f"  • {task.title()}")
else:
    print("\n No pending tasks! Great job!")
print("\n" + "\n")
completed_tasks =[task for task, task_info in todos.items() if task_info["status"] == "DONE"]
if completed_tasks:
    print("\n Your completed tasks are:")
    for task in completed_tasks:
        print(f"  • {task.title()}")