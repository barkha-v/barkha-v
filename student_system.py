# Student Performance Analysis System
# A simple console application that manages student marks and analyzes performance.

import csv
import os

# ---------- Constants (values that never change) ----------
FILE_NAME = "students.csv"
SUBJECTS = ["Maths", "Physics", "Chemistry", "English", "Computer"]
PASS_MARK = 35

# ---------- Global list that stores all students while the program runs ----------
# Each student is a dictionary: {"roll_no": "101", "name": "Aarav", "marks": [85, 90, 78, 88, 92]}
students = []


# =====================================================
# FILE HANDLING FUNCTIONS
# =====================================================

def load_students():
    """Read students from the CSV file into the students list."""
    if not os.path.exists(FILE_NAME):
        print("No saved file found. Starting with empty records.")
        return

    try:
        with open(FILE_NAME, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                marks = []
                for subject in SUBJECTS:
                    marks.append(int(row[subject]))
                student = {
                    "roll_no": row["roll_no"],
                    "name": row["name"],
                    "marks": marks
                }
                students.append(student)
        print(f"Loaded {len(students)} student record(s) from {FILE_NAME}.")
    except (ValueError, KeyError, TypeError):
        print("The CSV file is damaged or in the wrong format. Starting with empty records.")
        students.clear()


def save_students():
    """Write all students from the list into the CSV file."""
    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["roll_no", "name"] + SUBJECTS)  # header row
        for student in students:
            writer.writerow([student["roll_no"], student["name"]] + student["marks"])


# =====================================================
# CALCULATION FUNCTIONS
# =====================================================

def calculate_total(marks):
    """Return the sum of all marks."""
    return sum(marks)


def calculate_average(marks):
    """Return the average of all marks."""
    return sum(marks) / len(marks)


def is_passed(marks):
    """PASS/FAIL RULE: a student passes only if every subject is 35 or more."""
    for mark in marks:
        if mark < PASS_MARK:
            return False
    return True


def calculate_grade(average, passed):
    """GRADE RULE: uses the average. Failed students always get F."""
    if not passed:
        return "F"
    elif average >= 80:
        return "A"
    elif average >= 60:
        return "B"
    else:
        return "C"


def get_result(student):
    """Return total, average, status and grade of one student."""
    marks = student["marks"]
    total = calculate_total(marks)
    average = calculate_average(marks)
    passed = is_passed(marks)
    grade = calculate_grade(average, passed)
    status = "Pass" if passed else "Fail"
    return total, average, status, grade


# =====================================================
# HELPER FUNCTIONS
# =====================================================

def find_student(roll_no):
    """Return the student dictionary with this roll number, or None if not found."""
    for student in students:
        if student["roll_no"] == roll_no:
            return student
    return None


def read_mark(subject):
    """Keep asking until the user enters a whole number from 0 to 100."""
    while True:
        text = input(f"Enter marks in {subject} (0-100): ").strip()
        try:
            mark = int(text)
        except ValueError:
            print("Invalid input! Please enter a whole number.")
            continue
        if 0 <= mark <= 100:
            return mark
        print("Marks must be between 0 and 100.")


def print_student_details(student):
    """Print full details of one student."""
    total, average, status, grade = get_result(student)
    print("\n----- Student Details -----")
    print(f"{'Roll No':<10}: {student['roll_no']}")
    print(f"{'Name':<10}: {student['name']}")
    for i in range(len(SUBJECTS)):
        print(f"{SUBJECTS[i]:<10}: {student['marks'][i]}")
    print(f"{'Total':<10}: {total}")
    print(f"{'Average':<10}: {average:.2f}")
    print(f"{'Grade':<10}: {grade}")
    print(f"{'Status':<10}: {status}")
    print("---------------------------")


# =====================================================
# MENU OPERATION FUNCTIONS
# =====================================================

def add_student():
    """Option 1: add a new student."""
    print("\n--- Add Student ---")

    # Roll number: must not be empty and must not already exist
    while True:
        roll_no = input("Enter roll number: ").strip()
        if roll_no == "":
            print("Roll number cannot be empty.")
        elif find_student(roll_no) is not None:
            print("This roll number already exists. Please enter a different one.")
        else:
            break

    # Name: must not be empty
    while True:
        name = input("Enter student name: ").strip()
        if name == "":
            print("Name cannot be empty.")
        else:
            break

    # Marks in each subject
    marks = []
    for subject in SUBJECTS:
        marks.append(read_mark(subject))

    student = {"roll_no": roll_no, "name": name, "marks": marks}
    students.append(student)
    save_students()
    print(f"Student '{name}' added successfully!")


def view_all_students():
    """Option 2: show all students in a table."""
    print("\n--- All Students ---")
    if len(students) == 0:
        print("No student records found.")
        return

    print(f"{'Roll No':<10}{'Name':<15}{'Total':<8}{'Average':<10}{'Grade':<7}{'Status'}")
    print("-" * 56)
    for student in students:
        total, average, status, grade = get_result(student)
        print(f"{student['roll_no']:<10}{student['name']:<15}{total:<8}{average:<10.2f}{grade:<7}{status}")


def search_student():
    """Option 3: search by roll number."""
    print("\n--- Search Student ---")
    if len(students) == 0:
        print("No student records found.")
        return

    roll_no = input("Enter roll number to search: ").strip()
    student = find_student(roll_no)
    if student is None:
        print("Student not found.")
    else:
        print_student_details(student)


def update_student_marks():
    """Option 4: change the marks of one subject for a student."""
    print("\n--- Update Student Marks ---")
    if len(students) == 0:
        print("No student records found.")
        return

    roll_no = input("Enter roll number of the student: ").strip()
    student = find_student(roll_no)
    if student is None:
        print("Student not found.")
        return

    print(f"Current marks of {student['name']}:")
    for i in range(len(SUBJECTS)):
        print(f"{i + 1}. {SUBJECTS[i]}: {student['marks'][i]}")

    # Ask which subject to update (1 to 5)
    while True:
        choice = input(f"Enter subject number to update (1-{len(SUBJECTS)}): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(SUBJECTS):
            break
        print("Invalid choice. Please enter a valid subject number.")

    index = int(choice) - 1          # list positions start from 0
    new_mark = read_mark(SUBJECTS[index])
    student["marks"][index] = new_mark
    save_students()
    print("Marks updated successfully!")
    print_student_details(student)


def delete_student():
    """Option 5: delete a student after confirmation."""
    print("\n--- Delete Student ---")
    if len(students) == 0:
        print("No student records found.")
        return

    roll_no = input("Enter roll number to delete: ").strip()
    student = find_student(roll_no)
    if student is None:
        print("Student not found.")
        return

    confirm = input(f"Are you sure you want to delete {student['name']}? (y/n): ").strip().lower()
    if confirm == "y":
        students.remove(student)
        save_students()
        print("Student record deleted successfully!")
    else:
        print("Deletion cancelled.")


def display_topper():
    """Option 6: show the student(s) with the highest total marks."""
    print("\n--- Topper ---")
    if len(students) == 0:
        print("No student records found.")
        return

    # Step 1: find the highest total
    highest_total = -1
    for student in students:
        total = calculate_total(student["marks"])
        if total > highest_total:
            highest_total = total

    # Step 2: show every student who has that total (handles ties)
    for student in students:
        if calculate_total(student["marks"]) == highest_total:
            print("Topper of the class:")
            print_student_details(student)


def display_class_summary():
    """Option 7: show class statistics."""
    print("\n--- Class Summary ---")
    if len(students) == 0:
        print("No student records found.")
        return

    total_students = len(students)
    sum_of_averages = 0
    passed_count = 0
    failed_count = 0

    for student in students:
        total, average, status, grade = get_result(student)
        sum_of_averages += average
        if status == "Pass":
            passed_count += 1
        else:
            failed_count += 1

    class_average = sum_of_averages / total_students

    print(f"Number of students : {total_students}")
    print(f"Class average      : {class_average:.2f}")
    print(f"Students passed    : {passed_count}")
    print(f"Students failed    : {failed_count}")


# =====================================================
# MAIN PROGRAM
# =====================================================

def show_menu():
    print("\n===== STUDENT PERFORMANCE ANALYSIS SYSTEM =====\n")
    print("1. Add Student")
    print("2. View All Students")
    print("3. Search Student")
    print("4. Update Student Marks")
    print("5. Delete Student")
    print("6. Display Topper")
    print("7. Display Class Summary")
    print("8. Exit")


def main():
    load_students()   # load saved data when the program starts

    while True:
        show_menu()
        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            view_all_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            update_student_marks()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            display_topper()
        elif choice == "7":
            display_class_summary()
        elif choice == "8":
            print("Thank you for using the system. Goodbye!")
            break
        else:
            print("Invalid choice! Please enter a number from 1 to 8.")


# This line runs main() only when you run this file directly
if __name__ == "__main__":
    main()
