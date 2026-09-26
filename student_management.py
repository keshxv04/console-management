import json
import os


class Student:
    """Represents a single student."""
    def __init__(self, student_id, name, age, grade):
        self.student_id = student_id
        self.name = name.title() # Capitalize names automatically
        self.age = age
        self.grade = grade.upper()

    def to_dict(self):
        """Converts the student object to a dictionary for JSON saving."""
        return {
            "name": self.name,
            "age": self.age,
            "grade": self.grade
        }

    @staticmethod
    def from_dict(student_id, data):
        """Creates a Student object from a dictionary."""
        return Student(student_id, data["name"], data["age"], data["grade"])

    def display_info(self):
        return f"{self.student_id:<10} | {self.name:<20} | {self.age:<5} | {self.grade:<10}"
class StudentManager:
    """Handles the logic, data storage, and file management."""
    def __init__(self, filename="students_data.json"):
        self.filename = filename
        self.students = {} # Dictionary to hold students {ID: Student Object}
        self.load_data()

    def add_student(self, student_id, name, age, grade):
        if student_id in self.students:
            return False, "Error: Student ID already exists!"
        
        self.students[student_id] = Student(student_id, name, age, grade)
        self.save_data()
        return True, f"Success: Student '{name}' added successfully."

    def delete_student(self, student_id):
        if student_id in self.students:
            name = self.students[student_id].name
            del self.students[student_id]
            self.save_data()
            return True, f"Success: Student '{name}' deleted."
        return False, "Error: Student ID not found."

    def update_student(self, student_id, name, age, grade):
        if student_id in self.students:
            self.students[student_id] = Student(student_id, name, age, grade)
            self.save_data()
            return True, "Success: Student details updated."
        return False, "Error: Student ID not found."

    def search_student(self, search_term):
        """Searches by ID or Name (case-insensitive)."""
        results = []
        search_term = search_term.lower()
        for sid, student in self.students.items():
            if search_term in sid.lower() or search_term in student.name.lower():
                results.append(student)
        return results

    def get_all_students(self):
        return list(self.students.values())

    def save_data(self):
        """Saves the current dictionary of students to a JSON file."""
        data_to_save = {sid: student.to_dict() for sid, student in self.students.items()}
        with open(self.filename, 'w') as file:
            json.dump(data_to_save, file, indent=4)

    def load_data(self):
        """Loads students from the JSON file if it exists."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    data = json.load(file)
                    for sid, details in data.items():
                        self.students[sid] = Student.from_dict(sid, details)
            except json.JSONDecodeError:
                print("Warning: Data file corrupted. Starting with empty database.")
class ConsoleUI:
    """Handles the visual presentation and user inputs."""
    
    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def print_header(title):
        ConsoleUI.clear_screen()
        width = 55
        print("=" * width)
        print(f"{'STUDENT MANAGEMENT SYSTEM':^{width}}")
        print(f"{title:^{width}}")
        print("=" * width)

    @staticmethod
    def print_main_menu():
        print("\n[ MAIN MENU ]")
        print("1. Add New Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Student Details")
        print("5. Delete Student")
        print("6. Exit System")
        print("-" * 55)

    @staticmethod
    def print_student_table(students):
        if not students:
            print("\n⚠️  No students found in the database.\n")
            return

        print(f"\n{'ID':<10} | {'Name':<20} | {'Age':<5} | {'Grade':<10}")
        print("-" * 55)
        for student in students:
            print(student.display_info())
        print("-" * 55)
        print(f"Total Records: {len(students)}\n")

    @staticmethod
    def get_valid_integer(prompt):
        """Ensures the user enters a valid number."""
        while True:
            try:
                value = int(input(prompt))
                if value <= 0:
                    print("⚠️  Please enter a positive number.")
                    continue
                return value
            except ValueError:
                print("⚠️  Invalid input! Please enter a numerical value.")

    @staticmethod
    def show_message(success, message):
        if success:
            print(f"\n✅ {message}")
        else:
            print(f"\n❌ {message}")
        input("\nPress Enter to continue...")
def main():
    manager = StudentManager()
    ui = ConsoleUI()

    while True:
        ui.print_header("MAIN DASHBOARD")
        ui.print_main_menu()
        
        choice = input("Enter your choice (1-6): ").strip()

        if choice == '1':
            ui.print_header("ADD NEW STUDENT")
            sid = input("Enter Student ID (e.g., S001): ").strip()
            name = input("Enter Student Name: ").strip()
            age = ui.get_valid_integer("Enter Student Age: ")
            grade = input("Enter Student Grade/Major: ").strip()
            
            success, msg = manager.add_student(sid, name, age, grade)
            ui.show_message(success, msg)

        elif choice == '2':
            ui.print_header("ALL STUDENTS RECORD")
            ui.print_student_table(manager.get_all_students())
            input("\nPress Enter to return to main menu...")

        elif choice == '3':
            ui.print_header("SEARCH STUDENT")
            term = input("Enter Student ID or Name to search: ").strip()
            results = manager.search_student(term)
            ui.print_student_table(results)
            input("\nPress Enter to return to main menu...")

        elif choice == '4':
            ui.print_header("UPDATE STUDENT DETAILS")
            sid = input("Enter the Student ID to update: ").strip()
            if sid in manager.students:
                print(f"\nUpdating details for: {manager.students[sid].name}")
                name = input(f"New Name [{manager.students[sid].name}]: ").strip() or manager.students[sid].name
                age = input(f"New Age [{manager.students[sid].age}]: ").strip()
                age = int(age) if age.isdigit() else manager.students[sid].age
                grade = input(f"New Grade [{manager.students[sid].grade}]: ").strip() or manager.students[sid].grade
                
                success, msg = manager.update_student(sid, name, age, grade)
                ui.show_message(success, msg)
            else:
                ui.show_message(False, "Student ID not found.")

        elif choice == '5':
            ui.print_header("DELETE STUDENT")
            sid = input("Enter the Student ID to delete: ").strip()
            success, msg = manager.delete_student(sid)
            ui.show_message(success, msg)

        elif choice == '6':
            print("\n👋 Thank you for using the Student Management System. Goodbye!\n")
            break
        
        else:
            ui.show_message(False, "Invalid choice! Please select a number between 1 and 6.")

if __name__ == "__main__":
    main()