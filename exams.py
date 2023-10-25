import random
import os 
from datetime import datetime, timedelta

class Exam:
    def __init__(self, time_limit_minutes):
        self.questions = []
        self.time_limit = time_limit_minutes  

    def load_questions(self, filename):
        # Load exam questions from a text file
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
                question = None
                for line in lines:
                    line = line.strip()
                    if line.startswith("M:"):
                        if question:
                            self.questions.append(question)
                        question = {"type": "multiple", "question": line[2:], "choices": [], "answer": None}
                    elif line.startswith("S:"):
                        if question:
                            self.questions.append(question)
                        question = {"type": "single", "question": line[2:], "choices": [], "answer": None}
                    elif line.startswith("T:"):
                        if question:
                            self.questions.append(question)
                        question = {"type": "short", "question": line[2:], "answer": None}
                    elif line.startswith("A:"):
                        if question["type"] != "short":
                            question["answer"] = list(map(int, line[2:].split(',')))
                        else:
                            question["answer"] = line[2:]
                    elif line.startswith("C:"):
                        question["choices"].append(line[2:])
                if question:
                    self.questions.append(question)
        except FileNotFoundError:
            print("File not found.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def start(self, student_sid, student_extra_time=0):
        start_time = datetime.now()  # Record the start time of the exam
        end_time = start_time + timedelta(minutes=self.time_limit)  # Calculate the end time
        # Verify student SID
        student_info = get_student_info(student_sid)
        if student_info is None:
            print("Student with SID not found. Access denied.")
            return

        print(f"Welcome, {student_info['name']} (SID: {student_sid})")
        student_extra_time = student_info['extra_time']  # Get extra time from student data
        total_time = time_limit_minutes + student_extra_time  # Add extra time to the total time
        print(f"Your start time is: {start_time} and you have {total_time} Minutes to complete it.")
        # print(f"Your start time is : {start_time} and you have: {time_limit_minutes+student_extra_time} Minutes to complete it.")

        random.shuffle(self.questions)
        score = 0
        total_multiple_choice = 0  # Counter for multiple-choice questions
        total_other_questions = 0  # Counter for other question types
        # for i in range(len(self.questions)):
        for i in range(len(self.questions)):
            # Calculate remaining time for the exam
            remaining_time = (end_time - datetime.now()).total_seconds() / 60
            if remaining_time <= 0:
                print("Time's up! The exam has ended.")
                break

            print("*************************************************")
            question = self.questions[i]
            print(f"Question {i + 1}")
            print (f"({question['type']})") 
            print(f"{question['question']}")

            if question['type'] == "multiple":
                total_multiple_choice += 1
                for j in range(len(question['choices'])):
                    choice = question['choices'][j]
                    print(f"{j + 1}. {choice}")
                input_prompt = "Your answer ('1,2,3'): "
                answer = input(input_prompt)
                student_answers = [int(a) for a in answer.split(",")]
            elif question['type'] == "single":
                total_other_questions += 1
                for j in range(len(question['choices'])):
                    choice = question['choices'][j]
                    print(f"{j + 1}. {choice}")
                input_prompt = "Your answer: "
                answer = input(input_prompt)
                student_answers = [int(answer)]
            elif question['type'] == "short":
                total_other_questions += 1
                input_prompt = "Your answer: "
                answer = input(input_prompt)
                student_answers = [answer]

            correct_answers = question['answer']

            if question['type'] == "short":
                if student_answers[0] == correct_answers or student_answers[0] == str(correct_answers):
                    print("Correct!\n")
                    score += 1
                else:
                    print(f"Wrong! The correct answer is: {correct_answers}\n")
            elif question['type'] in ["multiple", "single"]:
                if set(student_answers) == set(correct_answers):
                    print("Correct!\n")
                    score += 2
                else:
                    if question['type'] == "single":
                        correct_choice = correct_answers[0]
                        correct_choice_text = question['choices'][correct_choice - 1]
                        print(f"Wrong! The correct answer is: {correct_choice_text}\n")
                    else:
                        print(f"Wrong! The correct answer(s) are: {', '.join(map(str, correct_answers))}\n")
                    
        # Calculate overall marks based on the counters
        overall_marks = (total_multiple_choice * 2) + (total_other_questions * 1)
        # print(f"You scored {score} out of {total_multiple_choice * 2 + total_other_questions}.")
        print(f"Overall marks: {score} out of {overall_marks}")


        # Calculate and print the time taken
        end_time = datetime.now()
        time_taken = end_time - start_time
        print(f"Time taken for the exam: {time_taken} minutes")

def get_student_info(student_sid):
    for student in students:
        if student['sid'] == student_sid:
            return student
    return None

def read_student_data(file_path):
    students = []
    try:
        with open(file_path, 'r', newline='', encoding='utf-8-sig') as file:
            header = file.readline().strip().replace('\ufeff', '').split(',')
            # print("Actual Header:", header) 
            if header and header[0] == 'sid' and header[1] == 'name' and header[2] == 'extra_time':
                for line in file:
                    values = line.strip().split(',')
                    if len(values) == 3:
                        student = {
                            'sid': values[0],
                            'name': values[1],
                            'extra_time': int(values[2])
                        }
                        students.append(student)
                    else:
                        print(f"Skipping invalid line: {', '.join(values)}")
            else:
                print("Header is missing or incorrect.")
    except FileNotFoundError:
        print("Student data file not found.")
    return students


if __name__ == "__main__":
    # Specify the time limit for the entire exam (in minutes)
    time_limit_minutes = 20  
    exam = Exam(time_limit_minutes)

    # Load questions from a file
    questions_file_path = "questions.txt"  
    exam.load_questions(questions_file_path)

    # Read student data from a CSV file
    students_data_file_path = "students.csv"  
    students = read_student_data(students_data_file_path)

    # Prompt the student to enter his/her SID
    student_sid = input("Enter your SID to proceed: ")
    exam.start(student_sid)

    