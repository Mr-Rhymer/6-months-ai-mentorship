

todos = []

while True:
    print("\nTo-Do List:")
    for i, task in enumerate(todos, 1):
        print(f"{i}. {task.title()}")

    action = input("\nAdd task (a), Remove by number (r), Quit (q), Clear all (c): ").strip().lower()

    if action == 'q':
        break
    elif action == 'a':
        task = input("New task: ").strip()
        todos.append(task)
        print("Added!")
    elif action == 'c':
        todos.clear()
        print("All tasks cleared!")
    elif action == 'r':
        try:
            num = int(input("Remove number: ")) - 1
            removed = todos.pop(num)
            print(f"Removed: {removed}")
        except:
            print("Invalid number!")
    else:
        print("Invalid action.")