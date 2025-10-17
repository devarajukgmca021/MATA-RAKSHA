import tkinter as tk
from tkinter import ttk, messagebox
from src.utils.database import Database
from src.utils.biometric import BiometricSimulator
from src.utils.blockchain import BlockchainManager

class RegistrarDashboard:
    def __init__(self, root, username, on_logout):
        self.root = root
        self.username = username
        self.on_logout = on_logout
        self.db = Database()
        self.biometric = BiometricSimulator()
        self.blockchain = BlockchainManager()
        
        self.root.title("Mata Raksha - Voter Registrar Dashboard")
        self.root.geometry("700x600")
        self.root.configure(bg='#2c3e50')
        
        self.create_widgets()
    
    def create_widgets(self):
        header_frame = tk.Frame(self.root, bg='#34495e', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="VOTER REGISTRAR DASHBOARD",
            font=('Arial', 20, 'bold'),
            bg='#34495e',
            fg='#ecf0f1'
        )
        title_label.pack(side='left', padx=20, pady=20)
        
        logout_btn = tk.Button(
            header_frame,
            text="Logout",
            font=('Arial', 11),
            bg='#e74c3c',
            fg='white',
            command=self.on_logout,
            cursor='hand2',
            padx=20,
            pady=8
        )
        logout_btn.pack(side='right', padx=20, pady=20)
        
        form_frame = tk.Frame(self.root, bg='#ecf0f1', padx=30, pady=30)
        form_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(form_frame, text="Voter Registration", font=('Arial', 16, 'bold'), bg='#ecf0f1').pack(pady=10)
        
        fields_frame = tk.Frame(form_frame, bg='#ecf0f1')
        fields_frame.pack(pady=20)
        
        tk.Label(fields_frame, text="Full Name:", font=('Arial', 12), bg='#ecf0f1').grid(row=0, column=0, sticky='w', pady=10)
        self.name_entry = tk.Entry(fields_frame, font=('Arial', 12), width=30)
        self.name_entry.grid(row=0, column=1, pady=10, padx=10)
        
        tk.Label(fields_frame, text="Date of Birth:", font=('Arial', 12), bg='#ecf0f1').grid(row=1, column=0, sticky='w', pady=10)
        self.dob_entry = tk.Entry(fields_frame, font=('Arial', 12), width=30)
        self.dob_entry.insert(0, "YYYY-MM-DD")
        self.dob_entry.grid(row=1, column=1, pady=10, padx=10)
        
        tk.Label(fields_frame, text="District:", font=('Arial', 12), bg='#ecf0f1').grid(row=2, column=0, sticky='w', pady=10)
        self.district_var = tk.StringVar()
        district_combo = ttk.Combobox(fields_frame, textvariable=self.district_var, font=('Arial', 12), width=28, state='readonly')
        district_combo['values'] = self.db.get_karnataka_districts()
        district_combo.grid(row=2, column=1, pady=10, padx=10)
        
        biometric_frame = tk.Frame(form_frame, bg='#ecf0f1')
        biometric_frame.pack(pady=20)
        
        self.fingerprint_label = tk.Label(
            biometric_frame,
            text="Fingerprint: Not Captured",
            font=('Arial', 12),
            bg='#ecf0f1',
            fg='#e74c3c'
        )
        self.fingerprint_label.pack(side='left', padx=10)
        
        capture_btn = tk.Button(
            biometric_frame,
            text="Capture Fingerprint",
            font=('Arial', 11),
            bg='#3498db',
            fg='white',
            command=self.capture_fingerprint,
            cursor='hand2',
            padx=15,
            pady=8
        )
        capture_btn.pack(side='left', padx=10)
        
        register_btn = tk.Button(
            form_frame,
            text="Register Voter",
            font=('Arial', 14, 'bold'),
            bg='#27ae60',
            fg='white',
            command=self.register_voter,
            cursor='hand2',
            padx=30,
            pady=12
        )
        register_btn.pack(pady=20)
        
        self.fingerprint_hash = None
    
    def capture_fingerprint(self):
        name = self.name_entry.get().strip()
        
        if not name:
            messagebox.showerror("Error", "Please enter voter name first")
            return
        
        self.fingerprint_hash, template_path = self.biometric.generate_fingerprint_template(name)
        
        self.fingerprint_label.config(
            text=f"Fingerprint: Captured (ID: {self.fingerprint_hash[:16]}...)",
            fg='#27ae60'
        )
        
        messagebox.showinfo("Success", f"Fingerprint captured successfully!\nTemplate saved: {template_path}")
    
    def register_voter(self):
        name = self.name_entry.get().strip()
        dob = self.dob_entry.get().strip()
        district = self.district_var.get()
        
        if not all([name, dob, district, self.fingerprint_hash]):
            messagebox.showerror("Error", "Please fill all fields and capture fingerprint")
            return
        
        try:
            blockchain_address, private_key = self.blockchain.create_voter_account()
            
            self.blockchain.fund_voter_account(blockchain_address, 0.1)
            
            voter_id = self.db.register_voter(name, dob, district, self.fingerprint_hash, blockchain_address, private_key)
            
            messagebox.showinfo(
                "Success",
                f"Voter registered successfully!\n\nVoter ID: {voter_id}\nName: {name}\nDistrict: {district}\nBlockchain Address: {blockchain_address[:20]}..."
            )
            
            self.name_entry.delete(0, tk.END)
            self.dob_entry.delete(0, tk.END)
            self.dob_entry.insert(0, "YYYY-MM-DD")
            self.district_var.set('')
            self.fingerprint_hash = None
            self.fingerprint_label.config(text="Fingerprint: Not Captured", fg='#e74c3c')
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to register voter: {str(e)}")
