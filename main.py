# Feedback Form 
# Tkinter front-end with SQLite Back-end


from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3


class Form:

    def __init__(self, master):
        
        master.title('Foods\'R\'Us - Feedback Form')
        master.resizable(False, False)
        master.configure(background = '#DAF7A6')
        
        self.style = ttk.Style()
        self.style.configure('TFrame', background = '#DAF7A6')
        self.style.configure('TButton', background = '#DAF7A6')
        self.style.configure('TLabel', background = '#DAF7A6', foreground = '#00554E', font = ('Calibri', 11))
        self.style.configure('Header.TLabel', font = ('Calibri', 18, 'bold'))      

        self.frame_header = ttk.Frame(master)
        self.frame_header.pack()
        
        self.logo = PhotoImage(file = 'grapes.png')
        ttk.Label(self.frame_header, image = self.logo).grid(row = 0, column = 0, rowspan = 2)
        ttk.Label(self.frame_header, text = 'Thanks for Shopping!', style = 'Header.TLabel').grid(row = 0, column = 1)
        ttk.Label(self.frame_header, wraplength = 300,
                  text = ("I hope you have enjoyed your time here.  "
                          "Please tell us what you think about our service in the Feedback Section below.")).grid(row = 1, column = 1)
        
        self.frame_content = ttk.Frame(master)
        self.frame_content.pack()

        ttk.Label(self.frame_content, text = 'Name:').grid(row = 0, column = 0, padx = 5, sticky = 'sw')
        ttk.Label(self.frame_content, text = 'Email:').grid(row = 0, column = 1, padx = 5, sticky = 'sw')
        ttk.Label(self.frame_content, text = 'Feedback:').grid(row = 2, column = 0, padx = 5, sticky = 'sw')
        
        self.entry_name = ttk.Entry(self.frame_content, width = 24, font = ('Calibri', 11))
        self.entry_email = ttk.Entry(self.frame_content, width = 24, font = ('Calibri', 11))
        self.text_feedback = Text(self.frame_content, width = 50, height = 10, font = ('Calibri', 11))
        
        self.entry_name.grid(row = 1, column = 0, padx = 5)
        self.entry_email.grid(row = 1, column = 1, padx = 5)
        self.text_feedback.grid(row = 3, column = 0, columnspan = 2, padx = 5)
        
        ttk.Button(self.frame_content, text = 'Submit',
                   command = self.submit).grid(row = 4, column = 0, padx = 5, pady = 5, sticky = 'e')
        ttk.Button(self.frame_content, text = 'Clear',
                   command = self.clear).grid(row = 4, column = 1, padx = 5, pady = 5, sticky = 'w')

    def submit(self):
        name = self.entry_name.get()
        email = self.entry_email.get()
        feedback = self.text_feedback.get(1.0, 'end')
        print('Name: {}'.format(name))
        print('Email: {}'.format(email))
        print('Feedback: {}'.format(feedback))
        with sqlite3.connect("feedback.db") as db:
            cursor = db.cursor()
            cursor.execute("select name from sqlite_master where name=?",("tblFeedback",))
            result = cursor.fetchall()
            if len(result) == 1:
                cursor.execute("""INSERT INTO tblFeedback (Name,Email,Feedback)
                     VALUES(?,?,?)""",(name,email,feedback))
                db.commit()
                print("Feedback stored in tblFeedback")
            else:
                cursor.execute("""create table tblFeedback
                (FeedbackID integer,
                Name text,
                Email text,
                Feedback text,
                primary key(FeedbackID))""")
                cursor.execute("""INSERT INTO tblFeedback (Name,Email,Feedback)
                VALUES(?,?,?)""",(name,email,feedback))
                db.commit()
                print("Feedback stored in tblFeedback")
        self.clear()
        messagebox.showinfo(title='Thank you for your feedback', message='Comments Saved!')
    
    def clear(self):
        self.entry_name.delete(0, 'end')
        self.entry_email.delete(0, 'end')
        self.text_feedback.delete(1.0, 'end')


def main():            

    root = Tk()
    Form(root)
    root.mainloop()
    
if __name__ == "__main__": main()
