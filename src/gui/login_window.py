import customtkinter as ctk
from tkinter import messagebox
from src.utils.database import Database

class LoginWindow:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.db = Database()

        # Default appearance
        ctk.set_appearance_mode("light")  # or "dark"
        ctk.set_default_color_theme("blue")

        self.root.title("Mata Raksha - Login")
        self.root.geometry("520x460")
        self.root.resizable(True, True)

        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = ctk.CTkLabel(
            self.root,
            text="MATA RAKSHA",
            font=('Arial', 28, 'bold')
        )
        title_label.pack(pady=(35, 5))

        subtitle_label = ctk.CTkLabel(
            self.root,
            text="AI-Enhanced Biometric Blockchain Voting System",
            font=('Arial', 20)
        )
        subtitle_label.pack(pady=(0, 20))

        # Role Selection Dropdown
        self.role_var = ctk.StringVar(value="Admin")
        role_label = ctk.CTkLabel(
            self.root,
            text="Select Role:",
            font=('Arial', 13)
        )
        role_label.pack(pady=(5, 3))
        
        self.role_menu = ctk.CTkOptionMenu(
            self.root,
            values=["Admin", "Registrar", "Officer"],
            variable=self.role_var,
            width=250,
            height=40,
            corner_radius=8
        )
        self.role_menu.pack(pady=(0, 15))

        # Username Entry
        self.username_entry = ctk.CTkEntry(
            self.root,
            placeholder_text="Username",
            width=250,
            height=40,
            corner_radius=10
        )
        self.username_entry.pack(pady=10)

        # Password Entry
        self.password_entry = ctk.CTkEntry(
            self.root,
            placeholder_text="Password",
            show="*",
            width=250,
            height=40,
            corner_radius=10
        )
        self.password_entry.pack(pady=10)
        self.password_entry.bind("<Return>", lambda e: self.login())

        # Rounded Login Button
        login_button = ctk.CTkButton(
            self.root,
            text="Login",
            width=200,
            height=40,
            corner_radius=20,
            fg_color="#27ae60",
            hover_color="#2ecc71",
            command=self.login
        )
        login_button.pack(pady=(25, 10))

        # Theme toggle switch
        self.theme_switch = ctk.CTkSwitch(
            self.root,
            text="Dark Mode",
            command=self.toggle_theme
        )
        self.theme_switch.pack(pady=(5, 10))

        # Info label
        info_label = ctk.CTkLabel(
            self.root,
            text="Default Credentials:\nadmin/admin123",
            font=('Arial', 9)
        )
        info_label.pack(pady=(10, 5))
        info_label2 = ctk.CTkLabel(
            self.root,
            text="DESIGNED & DEVELOPED BY",
            font=('Arial', 15, "bold")
        )
        info_label2.pack(pady=(1, 5))
        info_label3 = ctk.CTkLabel(
            self.root,
            text="Devaraju K G\nBharath H R\nDepartment of MCA - RNSIT",
            font=('Times New Roman', 12)
        )
        info_label3.pack(pady=(1, 5))
        info_label4 = ctk.CTkLabel(
            self.root,
            text="UNDER THE GUIDANCE OF",
            font=('Arial', 15, "bold")
        )
        info_label4.pack(pady=(10, 5))
        info_label5 = ctk.CTkLabel(
            self.root,
            text="Dr.Nagesh B S\nRoopa H M",
            font=('Times New Roman', 12)
        )
        info_label5.pack(pady=(10, 5))
    def toggle_theme(self):
        """Toggle between light and dark modes"""
        if ctk.get_appearance_mode().lower() == "light":
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        selected_role = self.role_var.get().lower()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        if selected_role == "admin":
            db_role = self.db.verify_login(username, password)
        elif selected_role == "registrar":
            db_role = self.db.verify_login_registrar(username, password)
        elif selected_role == "officer":
            db_role = self.db.verify_login_officer(username, password)
        print(db_role, selected_role)
        if db_role and db_role.lower() == selected_role:
            messagebox.showinfo("Success", f"Welcome! Logged in as {db_role.upper()}")
            self.on_login_success(db_role, username)
        else:
            messagebox.showerror("Error", "Invalid credentials or role mismatch")
            self.password_entry.delete(0, 'end')


