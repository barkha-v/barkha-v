# Student Performance Analysis System

A beginner-friendly, menu-driven **console application in Python** that manages student marks and analyses academic performance. Records are saved in a CSV file, so data is not lost when the program closes.

## Features
- Add a student (name, roll number, marks in 5 subjects)
- View all students with total, average, grade and pass/fail status
- Search a student by roll number
- Update a student's marks
- Delete a student (with confirmation)
- Find the topper (handles ties)
- Class summary: number of students, class average, passed, failed
- Auto-save to `students.csv` and auto-load on startup
- Input validation: marks must be whole numbers from 0 to 100; no empty or duplicate roll numbers
- Handles missing, empty, and damaged CSV files without crashing

## Tech used
- Python 3 (no external libraries)
- Built-in `csv` and `os` modules only
- Concepts: lists, dictionaries, functions, loops, conditions, file handling, exception handling

## How to run
1. Install Python 3.8 or newer.
2. Download or clone this repository.
3. Open a terminal in the project folder and run:

```bash
python student_system.py
```
(On Mac/Linux use `python3 student_system.py`.)

`students.csv` is created automatically after you add the first student.

**Want demo data?** Copy `sample_data/students_sample.csv` into the project folder and rename it to `students.csv` before running.

## Rules
| Rule | Logic |
|---|---|
| Pass / Fail | Fails if **any** subject mark is below 35 |
| Grade A | Average >= 80 |
| Grade B | Average >= 60 and < 80 |
| Grade C | Average >= 35 and < 60 |
| Grade F | Any failed student |

Pass/fail (`is_passed`) and grade (`calculate_grade`) are separate functions, so the logic is easy to follow.

## Project structure
```
student_performance_system/
├── student_system.py            # main program
├── sample_data/
│   └── students_sample.csv      # demo records
├── README.md
└── .gitignore
```

## Design notes
- Each student is a dictionary: `{"roll_no": "101", "name": "Aarav", "marks": [85, 90, 78, 88, 92]}`
- Total, average, grade and status are **calculated on demand**, not stored, so they never go out of date after an update.
- Data is saved to the CSV after every add, update, or delete.

## Future improvements
- Store students in a dictionary keyed by roll number for O(1) search
- Use a `Student` class
- Sort students by total marks (rank list)
- Add charts with matplotlib
