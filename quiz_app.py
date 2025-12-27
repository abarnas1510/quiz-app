import tkinter as tk
from tkinter import messagebox
import json

with open("quiz_data.json","r",encoding ="utf-8") as file:
    quiz_data=json.load(file)
    
topics=list(quiz_data.keys())

BG_COLOR="#f4f6f8"
HEADER_COLOR="#2c3e50"
BTN_COLOR="#3498db"
BTN_TEXT="white"
CARD_COLOR="white"

class QuizApp:
    def __init__(self, root):
        self.root=root
        self.root.title("GK Quiz App")
        self.root.geometry("600x450")
        self.root.configure(bg=BG_COLOR)
        
        self.topic=None
        self.questions=[]
        self.q_index=0
        self.score=0
        self.selected_answer=tk.IntVar()
        
        self.show_start_screen()
        
    def header(self, text):
        tk.Label(self.root, text=text, bg=HEADER_COLOR, fg="white",font=("Arial",18 , "bold"),pady=10).pack(fill="x")
        
    def show_start_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="GK QUIZ ",bg=HEADER_COLOR, fg="white",font=("Arial", 22,"bold"),pady=20).pack(fill="x")
        frame=tk.Frame(self.root, bg=BG_COLOR)
        frame.pack(expand=True)
        tk.Label(frame, text="Test your General knowledge ",font=("Arial",14, ),bg=BG_COLOR,justify="center").pack(pady=20)
        tk.Button(frame, text="START QUIZ",bg=BTN_COLOR,fg="white",font=("Arial",14, "bold"),width=20, height=2,relief="flat",command=self.show_topic_selection).pack(pady=10)  
        
    def show_topic_selection(self):
        self.clear_screen()
        self.header("Select Quiz Topic")
        frame=tk.Frame(self.root, bg=BG_COLOR)
        frame.pack(pady=30)
        
        for topic in topics:
            tk.Button(
                self.root,text=topic, width=30, bg=BTN_COLOR, fg=BTN_TEXT,font=("Arial", 11, "bold"), relief="flat", command=lambda t=topic:self.start_quiz(t)
            ).pack(pady=6)
            
    def start_quiz(self, topic):
        self.topic=topic
        self.questions=quiz_data[topic]
        self.q_index=0
        self.score=0
        self.show_question()
        
    def show_question(self):
        self.clear_screen()
        self.header(f"Question {self.q_index + 1}")
        card=tk.Frame(self.root, bg=CARD_COLOR, padx=20,pady=20)
        card.pack(padx=20,pady=20,fill="both",expand=True)
        self.selected_answer.set(-1)
        
        question_data=self.questions[self.q_index]
        tk.Label(card, text=f" {question_data['question']}", wraplength=520, justify="left", font=("Arial", 13)).pack(anchor="w", pady=10)
        for i, option in enumerate(question_data["options"]):
            tk.Radiobutton(card, text=option, bg=CARD_COLOR, variable=self.selected_answer, value=i, font=("Arial", 11), anchor="w").pack(fill="x", pady=4)
        tk.Button(self.root, text="Next", bg=BTN_COLOR, font=("Arial",11, "bold"),width=15,relief="flat", command=self.next_question).pack(pady=10)
        
    def next_question(self):
        if self.selected_answer.get()== -1:
            messagebox.showwarning("Warning", "Please select an answer!")
            return
        correct_answer=self.questions[self.q_index]["answer"]
        if self.selected_answer.get()== correct_answer:
            self.score+=1
        self.q_index+=1
        if self.q_index<len(self.questions):
            self.show_question()
        else:
            self.show_result()
            
    def show_result(self):
        self.clear_screen()
        self.header("Quiz Result")
        
        frame=tk.Frame(self.root, bg=CARD_COLOR, padx=30,pady=30)
        frame.pack(pady=40)
        total=len(self.questions)
        tk.Label(frame, text="🎊 Quiz Completed!", font=("Arial", 18 ,"bold"), bg=CARD_COLOR).pack(pady=10)
        tk.Label(frame, text=f"Your Score: {self.score}/{total}", font=("Arial", 18, "bold"),bg=CARD_COLOR).pack(pady=10)
        tk.Button(frame, text="Back to Topics", bg=BTN_COLOR,fg=BTN_TEXT,font=("Arial", 11 ,"bold"), width=20, relief="flat", command=self.show_topic_selection).pack(pady=5)
        tk.Button(frame, text="Exit",bg="#e74c3c",fg="white",font=("Arial", 11 ,"bold"), width=20, relief="flat", command=self.root.destroy).pack(pady=5)
        
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
            
root=tk.Tk()
app=QuizApp(root)
root.mainloop()