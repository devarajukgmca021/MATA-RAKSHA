"""from dotenv import load_dotenv
load_dotenv()
import tkinter as tk
from src.gui.login_window import LoginWindow
from src.gui.admin_dashboard import AdminDashboard
from src.gui.registrar_dashboard import RegistrarDashboard
from src.gui.officer_dashboard import OfficerDashboard
from src.gui.voter_dashboard import VoterDashboard

class MataRakshaApp:
    def __init__(self):
        self.root = tk.Tk()
        self.current_window = None
        self.show_login()
    
    def show_login(self):
        self.clear_window()
        self.current_window = LoginWindow(self.root, self.on_login_success)
    
    def on_login_success(self, role, username):
        self.clear_window()
        
        if role == 'admin':
            self.current_window = AdminDashboard(self.root, username, self.show_login)
        elif role == 'registrar':
            self.current_window = RegistrarDashboard(self.root, username, self.show_login)
        elif role == 'officer':
            self.current_window = OfficerDashboard(self.root, username, self.show_login)
        elif role == 'voter':
            self.current_window = VoterDashboard(self.root, username, self.show_login)
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MataRakshaApp()
    app.run()"""
from dotenv import load_dotenv
load_dotenv()
import customtkinter as ctk
from src.gui.login_window import LoginWindow
from src.gui.admin_dashboard import AdminDashboard
from src.gui.registrar_dashboard import RegistrarDashboard
from src.gui.officer_dashboard import OfficerDashboard
from src.gui.voter_dashboard import VoterDashboard

class MataRakshaApp:
    def __init__(self):
        ctk.set_appearance_mode('light')
        ctk.set_default_color_theme('blue')
        self.root = ctk.CTk()
        self.current_window = None
        self.show_login()
    
    def show_login(self):
        self.clear_window()
        self.current_window = LoginWindow(self.root, self.on_login_success)
    
    def on_login_success(self, role, username):
        self.clear_window()
        
        if role == 'admin':
            self.current_window = AdminDashboard(self.root, username, self.show_login)
        elif role == 'registrar':
            self.current_window = RegistrarDashboard(self.root, username, self.show_login)
        elif role == 'officer':
            self.current_window = OfficerDashboard(self.root, username, self.show_login)
        elif role == 'voter':
            self.current_window = VoterDashboard(self.root, username, self.show_login)
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MataRakshaApp()
    app.run()
