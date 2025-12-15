import math
import numpy as np

COURSE_CREDITS = {
    "CS101": 3,
    "MA101": 4,
    "PH101": 3,
    "EC201": 2
}

class Entity:
    """Base class for encapsulation and input utility"""
    def __init__(self, _id, name):
        self._id = _id
        self._name = name

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def _get_input(self, prompt, data_type=str):
        while True:
            try:
                return data_type(input(prompt))
            except:
                print("Invalid input type. Please try again.")

class Student(Entity):
    def __init__(self, s_id, name, dob, gpa=0.0):
        super().__init__(s_id, name)
        self._dob = dob
        self._gpa = gpa

    def __str__(self):
        return f"ID: {self._id:<5} | Name: {self._name:<20} | DoB: {self._dob:<10} | GPA: {self._gpa:.2f}"

    @classmethod
    def input(cls, existing_students):
        s_id = input("   ID: ").strip()
        if s_id in existing_students:
            print("Error: ID already exists.")
            return None
        name = input("   Name: ").strip()
        dob = input("   DoB: ").strip()
        return cls(s_id, name, dob)

    def set_gpa(self, gpa):
        self._gpa = gpa

    def get_gpa(self):
        return self._gpa

class Course(Entity):
    def __str__(self):
        return f"ID: {self._id:<5} | Course: {self._name:<15} | Credits: {COURSE_CREDITS.get(self._id, 3)}"

    @classmethod
    def input(cls, existing_courses):
        c_id = input("   ID: ").strip()
        if c_id in existing_courses:
            print("Error: ID already exists.")
            return None
        name = input("   Name: ").strip()
        return cls(c_id, name)

class MarkManagementSystem:
    def __init__(self):
        self._students = {}
        self._courses = {}
        self._marks = {}

    def input_students_data(self):
        num = Entity._get_input(self, "-> Number of students: ", int)
        for _ in range(num):
            s = Student.input(self._students)
            if s:
                self._students[s.get_id()] = s

    def input_courses_data(self):
        num = Entity._get_input(self, "-> Number of courses: ", int)
        for _ in range(num):
            c = Course.input(self._courses)
            if c:
                self._courses[c.get_id()] = c
                self._marks[c.get_id()] = {}

    def input_marks_for_course(self):
        if not self._students or not self._courses:
            print("Warning: Please input students and courses first.")
            return

        self.list_courses()
        c_id = input("-> Course ID to input marks: ").strip()
        if c_id not in self._courses:
            print("Error: Invalid course ID.")
            return

        for s_id, student in self._students.items():
            while True:
                mark = Entity._get_input(
                    self,
                    f"   Mark (0-20) for {student.get_name()} ({s_id}): ",
                    np.float64
                )

                mark = math.floor(mark * 10) / 10

                if 0 <= mark <= 20:
                    self._marks[c_id][s_id] = mark
                    break
                else:
                    print("Warning: Score must be between 0 and 20.")

        self.calculate_all_gpas()

    def calculate_student_gpa(self, s_id):
        marks = []
        credits = []

        for c_id, course_marks in self._marks.items():
            if s_id in course_marks:
                gpa_score = course_marks[s_id] * (4.0 / 20.0)
                marks.append(gpa_score)
                credits.append(COURSE_CREDITS.get(c_id, 3))

        if not marks:
            return 0.0

        return np.average(marks, weights=credits)

    def calculate_all_gpas(self):
        for s_id in self._students:
            self._students[s_id].set_gpa(self.calculate_student_gpa(s_id))

    def list_students(self):
        print("\n--- STUDENTS ---")
        if not self._students:
            print("No students.")
        for s in self._students.values():
            print(f"| {s} |")

    def list_courses(self):
        print("\n--- COURSES ---")
        if not self._courses:
            print("No courses.")
        for c in self._courses.values():
            print(f"| {c} |")

    def show_marks_for_course(self):
        self.list_courses()
        c_id = input("-> Course ID: ").strip()
        if c_id not in self._courses:
            print("Error: Invalid ID.")
            return

        print(f"\n--- MARKS FOR {self._courses[c_id].get_name()} ---")
        for s_id, s in self._students.items():
            print(f"{s_id:<10} | {s.get_name():<20} | {self._marks[c_id].get(s_id, 'N/A')}")

    def sort_students_by_gpa(self):
        print("\n--- GPA RANKING (DESCENDING) ---")
        students_sorted = sorted(
            self._students.values(),
            key=lambda s: s.get_gpa(),
            reverse=True
        )
        for s in students_sorted:
            print(f"| {s} |")

def main():
    system = MarkManagementSystem()

    actions = {
        '1': system.input_students_data,
        '2': system.input_courses_data,
        '3': system.input_marks_for_course,
        '4': system.list_courses,
        '5': system.list_students,
        '6': system.show_marks_for_course,
        '7': system.sort_students_by_gpa
    }

    while True:
        print("\n=== PRACTICAL WORK 4 MANAGER ===")
        print("1. Input Students")
        print("2. Input Courses")
        print("3. Input Marks (Floored)")
        print("4. List Courses")
        print("5. List Students")
        print("6. Show Marks for Course")
        print("7. Sort Students by GPA")
        print("0. Exit")

        choice = input("-> Choice: ").strip()
        if choice == '0':
            print("Exiting program.")
            break
        elif choice in actions:
            actions[choice]()
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
