import random
import sqlite3
from datetime import datetime
import os
import json


# Connect to SQLite database
conn = sqlite3.connect("math_learning.db")
cursor = conn.cursor()


def create_table_not_exists():
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS results (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        datetime TEXT,
                        correct INTEGER,
                        incorrect INTEGER,
                        difficulty TEXT,
                        quiz_timer REAL NOT NULL,
                        per_question TEXT NOT NULL)"""
    )
    conn.commit()


# Create table if not exists


def get_problem(digits, operation):
    if operation == "addition":
        num1 = random.randint(10 ** (digits - 1), 10**digits - 1)
        num2 = random.randint(10 ** (digits - 1), 10**digits - 1)
        return num1, num2, num1 + num2
    elif operation == "subtraction":
        num1 = random.randint(10 ** (digits - 1), 10**digits - 1)
        num2 = random.randint(10 ** (digits - 1), 10**digits - 1)
        return num1, num2, num1 - num2
    else:
        raise ValueError("Unsupported operation")


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")
    print("WELCOME TO YOUR DADs COOLEST MATH LEARNING PROGRAM!")


def convert_problem_type(convert):
    if convert == "a":
        convert = "addition"
    elif convert == "s":
        convert = "subtraction"
    elif convert == "c":
        convert = "combination"
    return convert


def convert_problem_timer_into_json(timer_dict):
    json_timing_data = json.dumps(timer_dict)
    return json_timing_data


def main():
    name = input("Enter your name: ")
    digits = int(input("How many digits for problems (1, 2, or 3)? "))
    operation = input("Choose operation (\033[92ma\033[0m)ddition, (\033[92ms\033[0m)btraction, (\033[92mc\033[0m)ombination): ").lower()
    if len(operation) == 1:
        operation = convert_problem_type(operation)
    how_many_problems = int(input("How many problems do you want to solve?"))

    correct = 0
    incorrect = 0
    problem_count = 0
    start_quiz = datetime.now()
    timing_dict = {}
    while True:
        if operation == "combination":
            operation_choice = random.choice(["addition", "subtraction"])
        else:
            operation_choice = operation
        # start timer
        start_timer = datetime.now()

        num1, num2, answer = get_problem(digits, operation_choice)
        user_answer = int(input(f"What is {num1} {'+' if operation_choice == 'addition' else '-'} {num2}? "))

        if user_answer is None:
            print("You need to enter an answer!")
            incorrect += 1

        if user_answer == answer:
            print("\033[92mCORRECT!\033[0m")
            correct += 1
            end_timer = datetime.now()

        else:
            print("INCORRECT, would you like to try again? (yes/no)")
            incorrect += 1

            retry = input().lower()
            if retry == "yes" or retry == "y":
                user_answer = int(input(f"What is {num1} {'+' if operation_choice == 'addition' else '-'} {num2}? "))
                if user_answer == answer:
                    print("\033[92mCORRECT!\033[0m")
                    end_timer = datetime.now()
                else:
                    print("INCORRECT")
                    incorrect += 1
            else:
                incorrect += 1
                end_timer = datetime.now()

        problem_count += 1
        # make dict of problem and time taken
        time_taken = round((end_timer - start_timer).total_seconds(), 1)
        timing_dict[f"{num1}{'+' if operation_choice == 'addition' else '-'}{num2}"] = time_taken
        if problem_count == how_many_problems:
            time_per_problem = convert_problem_timer_into_json(timing_dict)
            break

    quiz_timer = round((datetime.now() - start_quiz).total_seconds(), 1)

    # Create the table if doesnt exist
    create_table_not_exists()

    # Store results in the database
    cursor.execute(
        "INSERT INTO results (name, datetime, correct, incorrect, difficulty, quiz_timer, per_question ) " "VALUES (?, ?, ?, ?, ?," "?, ?)",
        (name, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), correct, incorrect, f"{digits}-digit {operation}", quiz_timer, time_per_problem),
    )
    conn.commit()

    print(f"Thank you, {name}! You got {correct} correct and {incorrect} incorrect.")


if __name__ == "__main__":
    clear_screen()
    main()

# Close the database connection
conn.close()
