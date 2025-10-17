import tkinter as tk
from tkinter import ttk, messagebox
from src.utils.database import Database

class LoginWindow:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.db = Database()
        
        self.root.title("Mata Raksha - Login")
        self.root.geometry("500x400")
        self.root.configure(bg='#2c3e50')
        
        self.create_widgets()
    
    def create_widgets(self):
        title_frame = tk.Frame(self.root, bg='#2c3e50')
        title_frame.pack(pady=30)
        
        title_label = tk.Label(
            title_frame,
            text="MATA RAKSHA",
            font=('Arial', 28, 'bold'),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Blockchain-Based Biometric E-Voting System",
            font=('Arial', 12),
            bg='#2c3e50',
            fg='#bdc3c7'
        )
        subtitle_label.pack()
        
        login_frame = tk.Frame(self.root, bg='#34495e', padx=40, pady=30)
        login_frame.pack(pady=20)
        
        username_label = tk.Label(
            login_frame,
            text="Username:",
            font=('Arial', 12),
            bg='#34495e',
            fg='#ecf0f1'
        )
        username_label.grid(row=0, column=0, sticky='w', pady=10)
        
        self.username_entry = tk.Entry(login_frame, font=('Arial', 12), width=25)
        self.username_entry.grid(row=0, column=1, pady=10, padx=10)
        
        password_label = tk.Label(
            login_frame,
            text="Password:",
            font=('Arial', 12),
            bg='#34495e',
            fg='#ecf0f1'
        )
        password_label.grid(row=1, column=0, sticky='w', pady=10)
        
        self.password_entry = tk.Entry(login_frame, font=('Arial', 12), width=25, show='*')
        self.password_entry.grid(row=1, column=1, pady=10, padx=10)
        
        button_frame = tk.Frame(self.root, bg='#2c3e50')
        button_frame.pack(pady=20)
        
        login_button = tk.Button(
            button_frame,
            text="Login",
            font=('Arial', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            padx=30,
            pady=10,
            command=self.login,
            cursor='hand2'
        )
        login_button.pack()
        
        info_label = tk.Label(
            self.root,
            text="Default Credentials:\nadmin/admin123 | registrar/registrar123 | officer/officer123",
            font=('Arial', 9),
            bg='#2c3e50',
            fg='#95a5a6'
        )
        info_label.pack(pady=10)
        
        self.password_entry.bind('<Return>', lambda e: self.login())
    
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        role = self.db.verify_login(username, password)
        
        if role:
            messagebox.showinfo("Success", f"Welcome! Logged in as {role.upper()}")
            self.on_login_success(role, username)
        else:
            messagebox.showerror("Error", "Invalid username or password")
            self.password_entry.delete(0, tk.END)
