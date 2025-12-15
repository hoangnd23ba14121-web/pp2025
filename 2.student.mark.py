class Entity:
    """Base class for Student/Course and utility."""
    def __init__(self, _id, name):
        self._id = _id
        self._name = name
    def get_id(self): return self._id
    def get_name(self): return self._name
    def _get_input(self, p, t=str):
        while True:
            try: return t(input(p))
            except: print(" Invalid input type.")

class Student(Entity):
    def __init__(self, s_id, name, dob):
        super().__init__(s_id, name)
        self._dob = dob
    def __str__(self): return f"ID: {self._id:<5} | Name: {self._name:<20} | DoB: {self._dob}"
    @classmethod
    def input(cls, d):
        s_id = input("   ID: ").strip()
        if s_id in d: return print(" ID exists.")
        return cls(s_id, input("   Name: ").strip(), input("   DoB: ").strip())

class Course(Entity):
    def __str__(self): return f"ID: {self._id:<5} | Course: {self._name}"
    @classmethod
    def input(cls, d):
        c_id = input("   ID: ").strip()
        if c_id in d: return print(" ID exists.")
        return cls(c_id, input("   Name: ").strip())

class MarkManagementSystem:
    def __init__(self):
        self._students, self._courses, self._marks = {}, {}, {}

    def input_students_data(self):
        num = self._get_input("-> Num students: ", int)
        for i in range(num):
            s = Student.input(self._students)
            if s: self._students[s.get_id()] = s

    def input_courses_data(self):
        num = self._get_input("-> Num courses: ", int)
        for i in range(num):
            c = Course.input(self._courses)
            if c:
                self._courses[c.get_id()] = c
                self._marks[c.get_id()] = {}

    def input_marks_for_course(self):
        if not self._courses or not self._students: return print(" Add data first.")
        self.list_courses()
        c_id = input("-> Course ID to mark: ").strip()
        if c_id not in self._courses: return print(" Invalid ID.")
        
        for s_id, student in self._students.items():
            while True:
                mark = self._get_input(f"  Mark (0-20) for {student.get_name()} ({s_id}): ", float)
                if 0 <= mark <= 20:
                    self._marks[c_id][s_id] = mark; break
                else: print(" 0-20 only.")

    def list_courses(self):
        print("\n--- Courses ---")
        if not self._courses: return print(" No courses.")
        for c in self._courses.values(): print(f"| {c} |")

    def list_students(self):
        print("\n--- Students ---")
        if not self._students: return print(" No students.")
        for s in self._students.values(): print(f"| {s} |")

    def show_student_marks_for_given_course(self):
        if not self._courses: return print(" Add courses first.")
        self.list_courses()
        c_id = input("-> Course ID to view marks: ").strip()
        if c_id not in self._courses: return print(" Invalid ID.")

        m = self._marks.get(c_id, {})
        print(f"\n--- Marks for {self._courses[c_id].get_name()} ---")
        print(f"| {'ID':<10} | {'Name':<20} | {'Mark':<5} |")
        for s_id, s in self._students.items():
            print(f"| {s_id:<10} | {s.get_name():<20} | {m.get(s_id, 'N/A'):<5} |")

    def _get_input(self, p, t=str):
        """Helper for robustness (inherited by Entity but also needed here)."""
        while True:
            try: return t(input(p))
            except: print(" Invalid input.")

def main_menu():
    system = MarkManagementSystem()
    actions = {
        '1': system.input_students_data,
        '2': system.input_courses_data,
        '3': system.input_marks_for_course,
        '4': system.list_courses,
        '5': system.list_students,
        '6': system.show_student_marks_for_given_course,
    }
    while True:
        print("\n=== OOP MARK MANAGER ===")
        print("1. Input Student | 2. Input Course | 3. Input Marks")
        print("4. List Courses | 5. List Students | 6. Show Marks | 0. Exit")
        c = input("-> Choice: ").strip()
        if c == '0': print(" Exiting."); break
        elif c in actions: actions[c]()
        else: print(" Invalid choice.")

if __name__ == "__main__":
    main_menu()