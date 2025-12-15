import math
import numpy as np

COURSE_CREDITS = {
    "CS101": 3, "MA101": 4, "PH101": 3, "EC201": 2 
}

class Entity:
    """Base class for Encapsulation and utility."""
    def __init__(self, _id, name): self._id, self._name = _id, name
    def get_id(self): return self._id
    def get_name(self): return self._name
    def _get_input(self, p, t=str): 
        while True:
            try: return t(input(p))
            except: print("Invalid input type. Please try again.")

class Student(Entity):
    def __init__(self, s_id, name, dob, gpa=0.0):
        super().__init__(s_id, name)
        self._dob = dob
        self._gpa = gpa
    def __str__(self): 
        return f"ID: {self._id:<5} | Name: {self._name:<20} | DoB: {self._dob} | GPA: {self._gpa:.2f}"
    @classmethod
    def input(cls, d):
        s_id = input("   ID: ").strip()
        if s_id in d: return print("Error: ID already exists.")
        return cls(s_id, input("   Name: ").strip(), input("   DoB: ").strip())
    def set_gpa(self, gpa): self._gpa = gpa
    def get_gpa(self): return self._gpa

class Course(Entity):
    def __str__(self): return f"ID: {self._id:<5} | Course: {self._name} | Credits: {COURSE_CREDITS.get(self._id, 3)}"
    @classmethod
    def input(cls, d):
        c_id = input("   ID: ").strip()
        if c_id in d: return print("Error: ID already exists.")
        return cls(c_id, input("   Name: ").strip())

class MarkManagementSystem:
    def __init__(self):
        self._students, self._courses, self._marks = {}, {}, {}

    # --- INPUT METHODS (with math.floor rounding) ---
    def input_students_data(self):
        num = Entity._get_input(self, "-> Num students: ", int)
        for i in range(num):
            s = Student.input(self._students)
            if s: self._students[s.get_id()] = s

    def input_courses_data(self):
        num = Entity._get_input(self, "-> Num courses: ", int)
        for i in range(num):
            c = Course.input(self._courses)
            if c:
                self._courses[c.get_id()] = c
                self._marks[c.get_id()] = {}

    def input_marks_for_course(self):
        if not self._courses or not self._students: return print("Warning: Add data first.")
        self.list_courses()
        c_id = input("-> Course ID to mark: ").strip()
        if c_id not in self._courses: return print("Error: Invalid ID.")
        
        for s_id, student in self._students.items():
            while True:
                # Use np.float64 for NumPy compatibility
                mark = Entity._get_input(self, f"  Mark (0-20) for {student.get_name()} ({s_id}): ", np.float64) 
                
                # REQUIREMENT: Round down to 1-digit decimal using math.floor()
                mark_floored = math.floor(mark * 10) / 10
                
                if 0 <= mark_floored <= 20:
                    self._marks[c_id][s_id] = mark_floored
                    print(f"   (Score stored: {mark_floored})")
                    break
                else: print("Warning: Score must be 0-20.")
        self.calculate_all_gpas() 

    # --- MATHS & NUMPY (GPA Calculation and Sorting) ---
    def calculate_student_gpa(self, s_id):
        """Calculates Weighted Average GPA using NumPy."""
        marks_array, credits_array = [], []
        for c_id, course_marks in self._marks.items():
            if s_id in course_marks:
                mark = course_marks[s_id]
                credits = COURSE_CREDITS.get(c_id, 3)
                gpa_score = mark * (4.0/20.0) # Convert mark (0-20) to GPA (0-4.0)
                marks_array.append(gpa_score)
                credits_array.append(credits)

        if not marks_array: return 0.0
        
        marks_np = np.array(marks_array)
        credits_np = np.array(credits_array)
        weighted_sum = np.sum(marks_np * credits_np)
        total_credits = np.sum(credits_np)
        
        return weighted_sum / total_credits if total_credits > 0 else 0.0

    def calculate_all_gpas(self):
        """Recalculates GPA for all students."""
        for s_id in self._students:
            self._students[s_id].set_gpa(self.calculate_student_gpa(s_id))

    def sort_students_by_gpa(self):
        """Sorts student list by GPA descending."""
        student_list = list(self._students.items())
        student_list.sort(key=lambda item: item[1].get_gpa(), reverse=True)
        
        print("\n--- Sorted Students (GPA Descending) ---")
        print("--- GPA RANKING ---") # Decoration
        for _, student in student_list:
            print(f"| {student} |")
        print("------------------------------------------")

    # --- LISTING METHODS ---
    def list_courses(self):
        print("\n--- Courses ---")
        if not self._courses: return print("Warning: No courses.")
        for c in self._courses.values(): print(f"| {c} |")
    def list_students(self):
        print("\n--- Students ---")
        if not self._students: return print("Warning: No students.")
        for s in self._students.values(): print(f"| {s} |")
    def show_student_marks_for_given_course(self):
        if not self._courses: return print("Warning: Add courses first.")
        self.list_courses()
        c_id = input("-> Course ID to view marks: ").strip()
        if c_id not in self._courses: return print("Error: Invalid ID.")
        m = self._marks.get(c_id, {})
        print(f"\n--- Marks for {self._courses[c_id].get_name()} ---")
        print(f"| {'ID':<10} | {'Name':<20} | {'Mark':<5} |")
        for s_id, s in self._students.items():
            print(f"| {s_id:<10} | {s.get_name():<20} | {m.get(s_id, 'N/A'):<5} |")


def main_menu():
    system = MarkManagementSystem()
    actions = {
        '1': system.input_students_data, '2': system.input_courses_data, 
        '3': system.input_marks_for_course, '4': system.list_courses, 
        '5': system.list_students, '6': system.show_student_marks_for_given_course,
        '7': system.sort_students_by_gpa, 
    }
    while True:
        print("\n=== PRACTICAL WORK 3 MANAGER ===") # Decoration
        print("1. Input Student | 2. Input Course | 3. Input Marks (Floored)")
        print("4. List Courses | 5. List Students | 6. Show Marks")
        print("7. Show Students Sorted by GPA | 0. Exit")
        c = input("-> Choice: ").strip()
        if c == '0': print("Exiting system."); break
        elif c in actions: actions[c]()
        else: print("Invalid choice.")

if __name__ == "__main__":
    main_menu()