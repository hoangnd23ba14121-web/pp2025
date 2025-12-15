students, courses, marks = {}, {}, {}

def get_int(p):
    try: return int(input(p))
    except: return 0

def input_students():
    n = get_int("-> Num students: ")
    for i in range(n):
        s_id = input(f"ID {i+1}: ").strip()
        if s_id in students: continue
        students[s_id] = {'name': input("Name: ").strip(), 'dob': input("DoB: ").strip()}

def input_courses():
    n = get_int("-> Num courses: ")
    for i in range(n):
        c_id = input(f"ID {i+1}: ").strip()
        if c_id in courses: continue
        courses[c_id] = input("Name: ").strip()
        marks[c_id] = {}

def input_marks():
    if not courses or not students: return print(" Add data first.")
    c_id = input("-> Course ID to mark: ").strip()
    if c_id not in courses: return print(" Invalid ID.")
    print(f"\n--- Marks for {courses[c_id]} ---")
    for s_id, data in students.items():
        try:
            mark = float(input(f"  Mark (0-20) for {data['name']} ({s_id}): "))
            if 0 <= mark <= 20: marks[c_id][s_id] = mark
            else: print(" 0-20 only.")
        except ValueError: continue

def list_data(data, title):
    print(f"\n--- {title} ---")
    if not data: return print(" No data.")
    for k, v in data.items():
        if isinstance(v, dict): print(f"| ID: {k:<5} | Name: {v['name']:<20}") 
        else: print(f"| ID: {k:<5} | Name: {v}") 

def show_marks():
    if not courses: return print(" Add courses first.")
    c_id = input("-> Course ID to view: ").strip()
    if c_id not in courses: return print(" Invalid ID.")
    m = marks.get(c_id, {})
    print(f"\n--- Marks for {courses[c_id]} ---")
    print(f"| {'ID':<10} | {'Name':<20} | {'Mark':<5} |")
    for s_id, data in students.items():
        print(f"| {s_id:<10} | {data['name']:<20} | {m.get(s_id, 'N/A'):<5} |")

def main_menu():
    while True:
        print("\n=== MARK MANAGEMENT ===")
        print("1. Input Student Info")
        print("2. Input Course Info")
        print("3. Input Marks")
        print("4. List Courses")
        print("5. List Students")
        print("6. Show Marks for Course")
        print("0. Exit")
        
        c = input("-> Choice (0-6): ").strip()
        if c == '1': input_students()
        elif c == '2': input_courses()
        elif c == '3': input_marks()
        elif c == '4': list_data(courses, "Courses")
        elif c == '5': list_data(students, "Students")
        elif c == '6': show_marks()
        elif c == '0': print(" Exiting."); break
        else: print(" Invalid choice.")

if __name__ == "__main__":
    main_menu()