"""import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from src.utils.database import Database
from src.utils.blockchain import BlockchainManager

class AdminDashboard:
    def __init__(self, root, username, on_logout):
        self.root = root
        self.username = username
        self.on_logout = on_logout
        self.db = Database()
        self.blockchain = BlockchainManager()
        
        self.root.title("Mata Raksha - Admin Dashboard")
        self.root.geometry("900x650")
        self.root.configure(bg='#2c3e50')
        
        self.create_widgets()
    
    def create_widgets(self):
        header_frame = tk.Frame(self.root, bg='#34495e', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="ADMIN DASHBOARD",
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
        
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        election_tab = tk.Frame(notebook, bg='#ecf0f1')
        candidate_tab = tk.Frame(notebook, bg='#ecf0f1')
        results_tab = tk.Frame(notebook, bg='#ecf0f1')
        
        notebook.add(election_tab, text='Create Election')
        notebook.add(candidate_tab, text='Add Candidates')
        notebook.add(results_tab, text='View Results')
        
        self.create_election_tab(election_tab)
        self.create_candidate_tab(candidate_tab)
        self.create_results_tab(results_tab)
    
    def create_election_tab(self, parent):
        form_frame = tk.Frame(parent, bg='#ecf0f1')
        form_frame.pack(pady=30, padx=30)
        
        tk.Label(form_frame, text="Election Name:", font=('Arial', 12), bg='#ecf0f1').grid(row=0, column=0, sticky='w', pady=10)
        self.election_name_entry = tk.Entry(form_frame, font=('Arial', 12), width=30)
        self.election_name_entry.grid(row=0, column=1, pady=10, padx=10)
        
        tk.Label(form_frame, text="District:", font=('Arial', 12), bg='#ecf0f1').grid(row=1, column=0, sticky='w', pady=10)
        self.district_var = tk.StringVar()
        district_combo = ttk.Combobox(form_frame, textvariable=self.district_var, font=('Arial', 12), width=28, state='readonly')
        district_combo['values'] = self.db.get_karnataka_districts()
        district_combo.grid(row=1, column=1, pady=10, padx=10)
        
        tk.Label(form_frame, text="Start Date:", font=('Arial', 12), bg='#ecf0f1').grid(row=2, column=0, sticky='w', pady=10)
        self.start_date_entry = tk.Entry(form_frame, font=('Arial', 12), width=30)
        self.start_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.start_date_entry.grid(row=2, column=1, pady=10, padx=10)
        
        tk.Label(form_frame, text="End Date:", font=('Arial', 12), bg='#ecf0f1').grid(row=3, column=0, sticky='w', pady=10)
        self.end_date_entry = tk.Entry(form_frame, font=('Arial', 12), width=30)
        self.end_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.end_date_entry.grid(row=3, column=1, pady=10, padx=10)
        
        create_btn = tk.Button(
            form_frame,
            text="Create Election on Blockchain",
            font=('Arial', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            command=self.create_election,
            cursor='hand2',
            padx=20,
            pady=10
        )
        create_btn.grid(row=4, column=0, columnspan=2, pady=20)
    
    def create_candidate_tab(self, parent):
        form_frame = tk.Frame(parent, bg='#ecf0f1')
        form_frame.pack(pady=30, padx=30)
        
        tk.Label(form_frame, text="Select Election:", font=('Arial', 12), bg='#ecf0f1').grid(row=0, column=0, sticky='w', pady=10)
        self.election_var = tk.StringVar()
        self.election_combo = ttk.Combobox(form_frame, textvariable=self.election_var, font=('Arial', 12), width=28, state='readonly')
        self.election_combo.grid(row=0, column=1, pady=10, padx=10)
        self.load_elections()
        
        tk.Label(form_frame, text="Candidate Name:", font=('Arial', 12), bg='#ecf0f1').grid(row=1, column=0, sticky='w', pady=10)
        self.candidate_name_entry = tk.Entry(form_frame, font=('Arial', 12), width=30)
        self.candidate_name_entry.grid(row=1, column=1, pady=10, padx=10)
        
        tk.Label(form_frame, text="Party Name:", font=('Arial', 12), bg='#ecf0f1').grid(row=2, column=0, sticky='w', pady=10)
        self.party_name_entry = tk.Entry(form_frame, font=('Arial', 12), width=30)
        self.party_name_entry.grid(row=2, column=1, pady=10, padx=10)
        
        tk.Label(form_frame, text="Symbol:", font=('Arial', 12), bg='#ecf0f1').grid(row=3, column=0, sticky='w', pady=10)
        self.symbol_entry = tk.Entry(form_frame, font=('Arial', 12), width=30)
        self.symbol_entry.grid(row=3, column=1, pady=10, padx=10)
        
        add_btn = tk.Button(
            form_frame,
            text="Add Candidate to Blockchain",
            font=('Arial', 12, 'bold'),
            bg='#3498db',
            fg='white',
            command=self.add_candidate,
            cursor='hand2',
            padx=20,
            pady=10
        )
        add_btn.grid(row=4, column=0, columnspan=2, pady=20)
    
    def create_results_tab(self, parent):
        control_frame = tk.Frame(parent, bg='#ecf0f1')
        control_frame.pack(pady=20, padx=30, fill='x')
        
        tk.Label(control_frame, text="Select Election:", font=('Arial', 12), bg='#ecf0f1').pack(side='left', padx=10)
        self.results_election_var = tk.StringVar()
        self.results_election_combo = ttk.Combobox(control_frame, textvariable=self.results_election_var, font=('Arial', 12), width=30, state='readonly')
        self.results_election_combo.pack(side='left', padx=10)
        
        view_btn = tk.Button(
            control_frame,
            text="View Results",
            font=('Arial', 11),
            bg='#3498db',
            fg='white',
            command=self.view_results,
            cursor='hand2',
            padx=15,
            pady=5
        )
        view_btn.pack(side='left', padx=10)
        
        finalize_btn = tk.Button(
            control_frame,
            text="Finalize Election",
            font=('Arial', 11),
            bg='#e67e22',
            fg='white',
            command=self.finalize_election,
            cursor='hand2',
            padx=15,
            pady=5
        )
        finalize_btn.pack(side='left', padx=10)
        
        self.results_text = tk.Text(parent, font=('Arial', 11), height=20, bg='white')
        self.results_text.pack(fill='both', expand=True, padx=30, pady=10)
        
        self.load_elections_for_results()
    
    def create_election(self):
        name = self.election_name_entry.get().strip()
        district = self.district_var.get()
        start_date = self.start_date_entry.get().strip()
        end_date = self.end_date_entry.get().strip()
        
        if not all([name, district, start_date, end_date]):
            messagebox.showerror("Error", "Please fill all fields")
            return
        
        try:
            if not self.blockchain.w3.is_connected():
                messagebox.showerror("Error", "Not connected to Ganache. Please start Ganache first.")
                return
            
            if not self.blockchain.contract:
                contract_address = self.blockchain.deploy_contract()
                messagebox.showinfo("Success", f"Smart contract deployed at: {contract_address}")
            
            blockchain_election_id = self.blockchain.create_election(name, district)
            
            election_id = self.db.create_election(name, district, start_date, end_date)
            self.db.update_election_contract(election_id, self.blockchain.contract_address)
            
            messagebox.showinfo("Success", f"Election '{name}' created successfully!\nBlockchain ID: {blockchain_election_id}")
            
            self.election_name_entry.delete(0, tk.END)
            self.district_var.set('')
            self.load_elections()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create election: {str(e)}")
    
    def add_candidate(self):
        election_text = self.election_var.get()
        candidate_name = self.candidate_name_entry.get().strip()
        party_name = self.party_name_entry.get().strip()
        symbol = self.symbol_entry.get().strip()
        
        if not all([election_text, candidate_name, party_name]):
            messagebox.showerror("Error", "Please fill all required fields")
            return
        
        try:
            election_id = int(election_text.split('ID:')[1].split(')')[0])
            
            elections = self.db.get_elections()
            blockchain_id = None
            contract_address = None
            
            for election in elections:
                if election[0] == election_id:
                    blockchain_id = election[0]
                    contract_address = election[5]
                    break
            
            if contract_address:
                self.blockchain.load_contract(contract_address)
            
            self.blockchain.add_candidate(blockchain_id, candidate_name, party_name)
            self.db.add_candidate(election_id, candidate_name, party_name, symbol)
            
            messagebox.showinfo("Success", f"Candidate '{candidate_name}' added successfully to blockchain!")
            
            self.candidate_name_entry.delete(0, tk.END)
            self.party_name_entry.delete(0, tk.END)
            self.symbol_entry.delete(0, tk.END)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add candidate: {str(e)}")
    
    def view_results(self):
        election_text = self.results_election_var.get()
        
        if not election_text:
            messagebox.showerror("Error", "Please select an election")
            return
        
        try:
            election_id = int(election_text.split('ID:')[1].split(')')[0])
            
            elections = self.db.get_elections()
            contract_address = None
            
            for election in elections:
                if election[0] == election_id:
                    contract_address = election[5]
                    break
            
            if contract_address:
                self.blockchain.load_contract(contract_address)
                results = self.blockchain.get_all_results(election_id)
                
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, f"ELECTION RESULTS - {election_text}\n")
                self.results_text.insert(tk.END, "=" * 60 + "\n\n")
                
                for result in results:
                    self.results_text.insert(tk.END, f"Candidate: {result['name']}\n")
                    self.results_text.insert(tk.END, f"Party: {result['party']}\n")
                    self.results_text.insert(tk.END, f"Votes: {result['votes']}\n")
                    self.results_text.insert(tk.END, "-" * 60 + "\n")
            else:
                messagebox.showerror("Error", "No blockchain contract found for this election")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to view results: {str(e)}")
    
    def finalize_election(self):
        election_text = self.results_election_var.get()
        
        if not election_text:
            messagebox.showerror("Error", "Please select an election")
            return
        
        try:
            election_id = int(election_text.split('ID:')[1].split(')')[0])
            
            elections = self.db.get_elections()
            contract_address = None
            
            for election in elections:
                if election[0] == election_id:
                    contract_address = election[5]
                    break
            
            if contract_address:
                self.blockchain.load_contract(contract_address)
                self.blockchain.finalize_election(election_id)
                
                winner = self.blockchain.get_winner(election_id)
                
                messagebox.showinfo(
                    "Election Finalized",
                    f"Winner: {winner[0]}\nParty: {winner[1]}\nVotes: {winner[2]}"
                )
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to finalize election: {str(e)}")
    
    def load_elections(self):
        elections = self.db.get_elections()
        election_list = [f"{e[1]} - {e[2]} (ID:{e[0]})" for e in elections]
        self.election_combo['values'] = election_list
        if election_list:
            self.election_combo.current(0)
    
    def load_elections_for_results(self):
        elections = self.db.get_elections()
        election_list = [f"{e[1]} - {e[2]} (ID:{e[0]})" for e in elections]
        self.results_election_combo['values'] = election_list
        if election_list:
            self.results_election_combo.current(0)
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from src.utils.database import Database
from src.utils.blockchain import BlockchainManager


class AdminDashboard:
    def __init__(self, root, username, on_logout):
        self.root = root
        self.username = username
        self.on_logout = on_logout
        self.db = Database()
        self.blockchain = BlockchainManager()

        # Window setup
        self.root.title("Mata Raksha - Admin Dashboard")
        self.root.geometry("900x650")
        self.root.configure(bg='#f4f6f9')  # light background

        self.create_widgets()

    def create_widgets(self):
        # ---------------- HEADER BAR ----------------
        header_frame = tk.Frame(self.root, bg='#0078d7', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="ADMIN DASHBOARD",
            font=('Segoe UI', 20, 'bold'),
            bg='#0078d7',
            fg='white'
        )
        title_label.pack(side='left', padx=20, pady=20)

        logout_btn = tk.Button(
            header_frame,
            text="Logout",
            font=('Segoe UI', 11, 'bold'),
            bg='#e81123',
            fg='white',
            relief='flat',
            command=self.on_logout,
            cursor='hand2',
            padx=20,
            pady=8
        )
        logout_btn.pack(side='right', padx=20, pady=20)

        # ---------------- NOTEBOOK (Tabs) ----------------
        style = ttk.Style()
        style.configure('TNotebook', background='#f4f6f9', borderwidth=0)
        style.configure('TNotebook.Tab', font=('Segoe UI', 11, 'bold'), padding=[12, 6])
        style.map('TNotebook.Tab', background=[('selected', '#0078d7')], foreground=[('selected', 'blue')])

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        election_tab = tk.Frame(notebook, bg='#f4f6f9')
        candidate_tab = tk.Frame(notebook, bg='#f4f6f9')
        results_tab = tk.Frame(notebook, bg='#f4f6f9')

        notebook.add(election_tab, text='🗳 Create Election')
        notebook.add(candidate_tab, text='👥 Add Candidates')
        notebook.add(results_tab, text='📊 View Results')

        self.create_election_tab(election_tab)
        self.create_candidate_tab(candidate_tab)
        self.create_results_tab(results_tab)

    # ---------------- TAB 1: CREATE ELECTION ----------------
    def create_election_tab(self, parent):
        form_frame = tk.Frame(parent, bg='#f4f6f9')
        form_frame.pack(pady=30, padx=30)

        tk.Label(form_frame, text="Election Name:", font=('Segoe UI', 12), bg='#f4f6f9').grid(row=0, column=0, sticky='w', pady=10)
        self.election_name_entry = tk.Entry(form_frame, font=('Segoe UI', 12), width=30)
        self.election_name_entry.grid(row=0, column=1, pady=10, padx=10)

        tk.Label(form_frame, text="District:", font=('Segoe UI', 12), bg='#f4f6f9').grid(row=1, column=0, sticky='w', pady=10)
        self.district_var = tk.StringVar()
        district_combo = ttk.Combobox(form_frame, textvariable=self.district_var, font=('Segoe UI', 12), width=28, state='readonly')
        district_combo['values'] = self.db.get_karnataka_districts()
        district_combo.grid(row=1, column=1, pady=10, padx=10)

        tk.Label(form_frame, text="Start Date:", font=('Segoe UI', 12), bg='#f4f6f9').grid(row=2, column=0, sticky='w', pady=10)
        self.start_date_entry = tk.Entry(form_frame, font=('Segoe UI', 12), width=30)
        self.start_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.start_date_entry.grid(row=2, column=1, pady=10, padx=10)

        tk.Label(form_frame, text="End Date:", font=('Segoe UI', 12), bg='#f4f6f9').grid(row=3, column=0, sticky='w', pady=10)
        self.end_date_entry = tk.Entry(form_frame, font=('Segoe UI', 12), width=30)
        self.end_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.end_date_entry.grid(row=3, column=1, pady=10, padx=10)

        create_btn = tk.Button(
            form_frame,
            text="Create Election on Blockchain",
            font=('Segoe UI', 12, 'bold'),
            bg='#0078d7',
            fg='white',
            relief='flat',
            command=self.create_election,
            cursor='hand2',
            padx=20,
            pady=10
        )
        create_btn.grid(row=4, column=0, columnspan=2, pady=20)

    # ---------------- TAB 2: ADD CANDIDATES ----------------
    def create_candidate_tab(self, parent):
        form_frame = tk.Frame(parent, bg='#f4f6f9')
        form_frame.pack(pady=30, padx=30)

        tk.Label(form_frame, text="Select Election:", font=('Segoe UI', 12), bg='#f4f6f9').grid(row=0, column=0, sticky='w', pady=10)
        self.election_var = tk.StringVar()
        self.election_combo = ttk.Combobox(form_frame, textvariable=self.election_var, font=('Segoe UI', 12), width=28, state='readonly')
        self.election_combo.grid(row=0, column=1, pady=10, padx=10)
        self.load_elections()

        tk.Label(form_frame, text="Candidate Name:", font=('Segoe UI', 12), bg='#f4f6f9').grid(row=1, column=0, sticky='w', pady=10)
        self.candidate_name_entry = tk.Entry(form_frame, font=('Segoe UI', 12), width=30)
        self.candidate_name_entry.grid(row=1, column=1, pady=10, padx=10)

        tk.Label(form_frame, text="Party Name:", font=('Segoe UI', 12), bg='#f4f6f9').grid(row=2, column=0, sticky='w', pady=10)
        self.party_name_entry = tk.Entry(form_frame, font=('Segoe UI', 12), width=30)
        self.party_name_entry.grid(row=2, column=1, pady=10, padx=10)

        tk.Label(form_frame, text="Symbol:", font=('Segoe UI', 12), bg='#f4f6f9').grid(row=3, column=0, sticky='w', pady=10)
        self.symbol_entry = tk.Entry(form_frame, font=('Segoe UI', 12), width=30)
        self.symbol_entry.grid(row=3, column=1, pady=10, padx=10)

        add_btn = tk.Button(
            form_frame,
            text="Add Candidate to Blockchain",
            font=('Segoe UI', 12, 'bold'),
            bg='#0078d7',
            fg='white',
            relief='flat',
            command=self.add_candidate,
            cursor='hand2',
            padx=20,
            pady=10
        )
        add_btn.grid(row=4, column=0, columnspan=2, pady=20)

    # ---------------- TAB 3: VIEW RESULTS ----------------
    def create_results_tab(self, parent):
        control_frame = tk.Frame(parent, bg='#f4f6f9')
        control_frame.pack(pady=20, padx=30, fill='x')

        tk.Label(control_frame, text="Select Election:", font=('Segoe UI', 12), bg='#f4f6f9').pack(side='left', padx=10)
        self.results_election_var = tk.StringVar()
        self.results_election_combo = ttk.Combobox(control_frame, textvariable=self.results_election_var, font=('Segoe UI', 12), width=30, state='readonly')
        self.results_election_combo.pack(side='left', padx=10)

        view_btn = tk.Button(
            control_frame,
            text="View Results",
            font=('Segoe UI', 11, 'bold'),
            bg='#0078d7',
            fg='white',
            relief='flat',
            command=self.view_results,
            cursor='hand2',
            padx=15,
            pady=5
        )
        view_btn.pack(side='left', padx=10)

        finalize_btn = tk.Button(
            control_frame,
            text="Finalize Election",
            font=('Segoe UI', 11, 'bold'),
            bg='#f39c12',
            fg='white',
            relief='flat',
            command=self.finalize_election,
            cursor='hand2',
            padx=15,
            pady=5
        )
        finalize_btn.pack(side='left', padx=10)

        self.results_text = tk.Text(parent, font=('Segoe UI', 11), height=20, bg='white', relief='flat', wrap='word')
        self.results_text.pack(fill='both', expand=True, padx=30, pady=10)

        self.load_elections_for_results()

    # ---------------- FUNCTIONALITY ----------------
    def create_election(self):
        name = self.election_name_entry.get().strip()
        district = self.district_var.get()
        start_date = self.start_date_entry.get().strip()
        end_date = self.end_date_entry.get().strip()

        if not all([name, district, start_date, end_date]):
            messagebox.showerror("Error", "Please fill all fields")
            return

        try:
            if not self.blockchain.w3.is_connected():
                messagebox.showerror("Error", "Not connected to Ganache. Please start Ganache first.")
                return

            if not self.blockchain.contract:
                contract_address = self.blockchain.deploy_contract()
                messagebox.showinfo("Success", f"Smart contract deployed at: {contract_address}")

            blockchain_election_id = self.blockchain.create_election(name, district)

            election_id = self.db.create_election(name, district, start_date, end_date)
            self.db.update_election_contract(election_id, self.blockchain.contract_address)

            messagebox.showinfo("Success", f"Election '{name}' created successfully!\nBlockchain ID: {blockchain_election_id}")

            self.election_name_entry.delete(0, tk.END)
            self.district_var.set('')
            self.load_elections()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to create election: {str(e)}")

    def add_candidate(self):
        election_text = self.election_var.get()
        candidate_name = self.candidate_name_entry.get().strip()
        party_name = self.party_name_entry.get().strip()
        symbol = self.symbol_entry.get().strip()

        if not all([election_text, candidate_name, party_name]):
            messagebox.showerror("Error", "Please fill all required fields")
            return

        try:
            election_id = int(election_text.split('ID:')[1].split(')')[0])

            elections = self.db.get_elections()
            contract_address = None

            for e in elections:
                if e[0] == election_id:
                    contract_address = e[5]
                    break

            if contract_address:
                self.blockchain.load_contract(contract_address)

            self.blockchain.add_candidate(election_id, candidate_name, party_name)
            self.db.add_candidate(election_id, candidate_name, party_name, symbol)

            messagebox.showinfo("Success", f"Candidate '{candidate_name}' added successfully to blockchain!")

            self.candidate_name_entry.delete(0, tk.END)
            self.party_name_entry.delete(0, tk.END)
            self.symbol_entry.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to add candidate: {str(e)}")

    def view_results(self):
        election_text = self.results_election_var.get()

        if not election_text:
            messagebox.showerror("Error", "Please select an election")
            return

        try:
            election_id = int(election_text.split('ID:')[1].split(')')[0])

            elections = self.db.get_elections()
            contract_address = None

            for e in elections:
                if e[0] == election_id:
                    contract_address = e[5]
                    break

            if contract_address:
                self.blockchain.load_contract(contract_address)
                results = self.blockchain.get_all_results(election_id)

                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, f"ELECTION RESULTS - {election_text}\n")
                self.results_text.insert(tk.END, "=" * 60 + "\n\n")

                for r in results:
                    self.results_text.insert(tk.END, f"Candidate: {r['name']}\n")
                    self.results_text.insert(tk.END, f"Party: {r['party']}\n")
                    self.results_text.insert(tk.END, f"Votes: {r['votes']}\n")
                    self.results_text.insert(tk.END, "-" * 60 + "\n")
            else:
                messagebox.showerror("Error", "No blockchain contract found for this election")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to view results: {str(e)}")

    def finalize_election(self):
        election_text = self.results_election_var.get()

        if not election_text:
            messagebox.showerror("Error", "Please select an election")
            return

        try:
            election_id = int(election_text.split('ID:')[1].split(')')[0])

            elections = self.db.get_elections()
            contract_address = None

            for e in elections:
                if e[0] == election_id:
                    contract_address = e[5]
                    break

            if contract_address:
                self.blockchain.load_contract(contract_address)
                self.blockchain.finalize_election(election_id)

                winner = self.blockchain.get_winner(election_id)

                messagebox.showinfo(
                    "Election Finalized",
                    f"Winner: {winner[0]}\nParty: {winner[1]}\nVotes: {winner[2]}"
                )

        except Exception as e:
            messagebox.showerror("Error", f"Failed to finalize election: {str(e)}")

    # ---------------- HELPERS ----------------
    def load_elections(self):
        elections = self.db.get_elections()
        election_list = [f"{e[1]} - {e[2]} (ID:{e[0]})" for e in elections]
        self.election_combo['values'] = election_list
        if election_list:
            self.election_combo.current(0)

    def load_elections_for_results(self):
        elections = self.db.get_elections()
        election_list = [f"{e[1]} - {e[2]} (ID:{e[0]})" for e in elections]
        self.results_election_combo['values'] = election_list
        if election_list:
            self.results_election_combo.current(0)"""
import customtkinter as ctk
from tkinter import messagebox, ttk
from src.utils.database import Database
from datetime import datetime
from src.utils.blockchain import BlockchainManager
from tkcalendar import Calendar
from tkinter import Toplevel
from src.utils.ctk_datepicker import CTkDatePicker


KARNATAKA_DISTRICTS = [
    "Bagalkot", "Bangalore Rural", "Bangalore Urban", "Belagavi", "Ballari",
    "Bidar", "Vijayapura", "Chamarajanagar", "Chikkaballapur", "Chikkamagaluru",
    "Chitradurga", "Dakshina Kannada", "Davanagere", "Dharwad", "Gadag",
    "Hassan", "Haveri", "Kalaburagi", "Kodagu", "Kolar", "Koppal",
    "Mandya", "Mysuru", "Raichur", "Ramanagara", "Shivamogga",
    "Tumakuru", "Udupi", "Uttara Kannada", "Yadgir"
]

class AdminDashboard(ctk.CTkFrame):
    def __init__(self, root, username, on_logout):
        super().__init__(root)
        self.root = root
        self.username = username
        self.on_logout = on_logout
        self.db = Database()
        self.blockchain = BlockchainManager()
        
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.root.title("Mata Raksha - Admin Dashboard")
        self.root.geometry("900x600")

        top_bar = ctk.CTkFrame(self.root, fg_color="#1a252f", height=50)
        top_bar.pack(fill="x", side="top")

        # App Title (left side)
        ctk.CTkLabel(
            top_bar, text="🗳️ Mata Raksha Admin Panel",
            font=("Arial", 18, "bold"),
            text_color="#ecf0f1"
        ).pack(side="left", padx=20, pady=10)

        # Logged-in Username (center/right)
        ctk.CTkLabel(
            top_bar, text=f"Welcome, {self.username}",
            font=("Arial", 13),
            text_color="#bdc3c7"
        ).pack(side="right", padx=110)

        # Logout Button (top-right)
        logout_btn = ctk.CTkButton(
            top_bar, text="Logout",
            fg_color="#e74c3c", hover_color="#c0392b",
            width=90, height=30, corner_radius=15,
            command=self.logout
        )
        logout_btn.pack(side="right", padx=20, pady=10)

        # ---- Main Tab View ----
        self.tabview = ctk.CTkTabview(self.root, )#fg_color="#2c3e50")
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)


        self.tab_registrar = self.tabview.add("Registrar")
        self.tab_officer = self.tabview.add("Officer")
        self.tab_election = self.tabview.add("Create Election")
        self.tab_candidate = self.tabview.add("Add Candidates")
        self.tab_lifecycle = self.tabview.add("Lifecycle")
        
        seg_btn = self.tabview._segmented_button
        seg_btn.configure(
            height=45,              # increase tab height
            corner_radius=8,        # make rounded corners
            font=("Arial", 15, "bold"),  # bigger tab text
            border_width=2,         # thicker border
        )

        # You can also add some spacing between tabs
        for button in seg_btn._buttons_dict.values():
            button.configure(width=140, height=40, corner_radius=8)


        # Load tab UIs
        self.create_registrar_tab()
        self.create_officer_tab()
        self.create_election_tab()
        self.create_candidate_tab()
        self.create_lifecycle_tab()

        self.active_tab = None
        self.monitor_tab_change()
        self.auto_update_status()

    def on_tab_change(self, event=None):
        """Automatically refresh data when switching tabs."""
        current_tab = self.tabview.get()

        if current_tab == "Registrar":
            print("registrar")
            self.load_registrars()
        elif current_tab == "Officer":
            print("officer")
            self.load_officers()
        elif current_tab == "Create Election":
            print("election")
            self.load_elections()
        elif current_tab == "Add Candidates":
            print("candidate")
            # Reload pending elections + reset candidate list
            self.load_pending_elections()
            self.load_candidate_elections()
            self.refresh_candidate_table()
            self.clear_candidate_form()
        elif current_tab == "Lifecycle":
            self.load_lifecycle_elections()
            
    def monitor_tab_change(self):
        """Continuously check if the user switched tabs."""
        current_tab = self.tabview.get()

        if current_tab != self.active_tab:
            self.active_tab = current_tab
            self.on_tab_change()  # Trigger refresh logic

        # Re-run this check every 700 milliseconds
        self.root.after(700, self.monitor_tab_change)

    # ============ REGISTRAR TAB =============
    def create_registrar_tab(self):
        frame = ctk.CTkFrame(self.tab_registrar)
        frame.pack(pady=15, padx=15, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Manage Registrars", font=('Arial', 16, 'bold')).pack(pady=5)

        # Input fields
        self.reg_name = ctk.CTkEntry(frame, placeholder_text="Name", width=200)
        self.reg_name.pack(pady=5)

        self.reg_district = ctk.CTkComboBox(frame, values=KARNATAKA_DISTRICTS, width=200)
        self.reg_district.pack(pady=5)

        self.reg_password = ctk.CTkEntry(frame, placeholder_text="Password", show="*", width=200)
        self.reg_password.pack(pady=5)

        # Buttons
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="Add Registrar", fg_color="#27ae60",
                      command=self.add_registrar).grid(row=0, column=0, padx=5)
        ctk.CTkButton(btn_frame, text="Edit Registrar", fg_color="#2980b9",
                      command=self.edit_registrar).grid(row=0, column=1, padx=5)
        ctk.CTkButton(btn_frame, text="Delete Registrar", fg_color="#e67e22",
                      command=self.delete_registrar).grid(row=0, column=2, padx=5)

        # Table
        self.registrar_tree = ttk.Treeview(frame, columns=("Name", "District"), show="headings", height=8)
        self.registrar_tree.heading("Name", text="Name")
        self.registrar_tree.heading("District", text="District")
        self.registrar_tree.bind("<<TreeviewSelect>>", self.on_registrar_select)
        self.registrar_tree.pack(pady=10)

        self.load_registrars()

    def add_registrar(self):
        name = self.reg_name.get().strip()
        district = self.reg_district.get().strip()
        password = self.reg_password.get().strip()

        if not all([name, district, password]):
            messagebox.showerror("Error", "All fields are required!")
            return

        self.db.add_registrar(name, district, password)
        messagebox.showinfo("Success", "Registrar added successfully!")
        self.clear_registrar_fields()
        self.load_registrars()

    def edit_registrar(self):
        selected = self.registrar_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a registrar to edit!")
            return

        old_name = self.registrar_tree.item(selected[0], "values")[0]
        new_name = self.reg_name.get().strip()
        new_district = self.reg_district.get().strip()
        new_password = self.reg_password.get().strip()

        if not all([new_name, new_district]):
            messagebox.showerror("Error", "All fields are required!")
            return

        self.db.update_registrar(old_name, new_name, new_district, new_password)
        messagebox.showinfo("Success", "Registrar updated successfully!")
        self.clear_registrar_fields()
        self.load_registrars()

    def delete_registrar(self):
        selected = self.registrar_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a registrar to delete!")
            return
        name = self.registrar_tree.item(selected[0], "values")[0]
        self.db.delete_registrar(name)
        messagebox.showinfo("Deleted", f"Registrar '{name}' removed.")
        self.load_registrars()

    def load_registrars(self):
        for i in self.registrar_tree.get_children():
            self.registrar_tree.delete(i)
        for reg in self.db.get_registrars():
            self.registrar_tree.insert("", "end", values=reg)

    def on_registrar_select(self, event):
        selected = self.registrar_tree.selection()
        if selected:
            name, district = self.registrar_tree.item(selected[0], "values")
            self.reg_name.delete(0, 'end')
            self.reg_name.insert(0, name)
            self.reg_district.set(district)

    def clear_registrar_fields(self):
        self.reg_name.delete(0, 'end')
        self.reg_password.delete(0, 'end')
        self.reg_district.set(KARNATAKA_DISTRICTS[0])

    # ================= Officer Tab =================
    def create_officer_tab(self):
        frame = ctk.CTkFrame(self.tab_officer)
        frame.pack(pady=15, padx=15, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Manage Officer", font=('Arial', 16, 'bold')).pack(pady=5)

        self.off_name = ctk.CTkEntry(frame, placeholder_text="Name", width=200)
        self.off_name.pack(pady=5)

        self.off_district = ctk.CTkComboBox(frame, values=KARNATAKA_DISTRICTS, width=200)
        self.off_district.pack(pady=5)

        self.off_password = ctk.CTkEntry(frame, placeholder_text="Password", width=200, show="*")
        self.off_password.pack(pady=5)

        # Action buttons
        btn_frame = ctk.CTkFrame(frame)
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="Add Officer", fg_color="#27ae60",
                      command=self.add_officer, width=120).grid(row=0, column=0, padx=5)

        ctk.CTkButton(btn_frame, text="Update Officer", fg_color="#2980b9",
                      command=self.update_officer, width=120).grid(row=0, column=1, padx=5)

        ctk.CTkButton(btn_frame, text="Delete Selected", fg_color="#e67e22",
                      command=self.delete_officer, width=120).grid(row=0, column=2, padx=5)
        # Officer table
        self.officer_tree = ttk.Treeview(frame, columns=("Name", "District"), show="headings", height=8)
        self.officer_tree.heading("Name", text="Name")
        self.officer_tree.heading("District", text="District")
        self.officer_tree.pack(pady=10)

        self.officer_tree.bind("<ButtonRelease-1>", self.on_officer_select)

        self.load_officers()
        self.selected_officer = None  # Track which officer is being edited

    def add_officer(self): 
        name = self.off_name.get().strip()
        district = self.off_district.get().strip()
        password = self.off_password.get().strip()

        if not all([name, district, password]):
            messagebox.showerror("Error", "All fields are required!")
            return

        # Ensure one officer per district
        if self.db.check_officer_exists(district):
            messagebox.showerror("Error", f"Officer already assigned for {district}.")
            return

        self.db.add_officer(name, district, password)
        messagebox.showinfo("Success", "Officer added successfully!")
        self.load_officers()
        self.clear_officer_form()

    def load_officers(self):
        for i in self.officer_tree.get_children():
            self.officer_tree.delete(i)
        for off in self.db.get_officers():
            self.officer_tree.insert("", "end", values=off)

    def on_officer_select(self, event):
        selected = self.officer_tree.selection()
        if not selected:
            return
        values = self.officer_tree.item(selected[0], "values")
        self.selected_officer = values[0]  # Officer name
        self.off_name.delete(0, 'end')
        self.off_name.insert(0, values[0])
        self.off_district.set(values[1])

    def update_officer(self):
        if not self.selected_officer:
            messagebox.showerror("Error", "No officer selected for update.")
            return

        new_name = self.off_name.get().strip()
        new_district = self.off_district.get().strip()
        new_password = self.off_password.get().strip()

        if not new_name or not new_district:
            messagebox.showerror("Error", "Name and District are required!")
            return

        self.db.update_officer(self.selected_officer, new_name, new_district, new_password)
        messagebox.showinfo("Success", "Officer details updated successfully!")
        self.load_officers()
        self.clear_officer_form()

    def delete_officer(self):
        selected = self.officer_tree.selection()
        if not selected:
            messagebox.showerror("Error", "No officer selected.")
            return
        name = self.officer_tree.item(selected[0], "values")[0]
        self.db.delete_officer(name)
        self.load_officers()

    def clear_officer_form(self):
        self.off_name.delete(0, 'end')
        self.off_password.delete(0, 'end')
        self.off_district.set("")
        self.selected_officer = None

    # ================= Create Election Tab =================
    def create_election_tab(self):
        frame = ctk.CTkFrame(self.tab_election)
        frame.pack(pady=15, padx=15, fill="both", expand=True)

    # --- Title ---
        ctk.CTkLabel(frame, text="Create Election", font=('Arial', 18, 'bold')).pack(pady=10)

    # --- Election Name Entry ---
        self.election_name = ctk.CTkEntry(frame, placeholder_text="Election Name", width=300)
        self.election_name.pack(pady=5)

    # --- Start & End Dates ---
        self.start_date = ctk.CTkEntry(frame, placeholder_text="Start Date (YYYY-MM-DD)", width=300)
        self.start_date.pack(pady=5)

        self.end_date = ctk.CTkEntry(frame, placeholder_text="End Date (YYYY-MM-DD)", width=300)
        self.end_date.pack(pady=5)

    # --- Create Button ---
        ctk.CTkButton(
            frame,
            text="Create Election for All Karnataka Districts",
            fg_color="#27ae60",
            command=self.create_election
        ).pack(pady=10)
                # ---------------- EXISTING ELECTION SECTION ----------------
        separator = ctk.CTkLabel(frame, text="View Existing Elections", font=('Arial', 14, 'bold'))
        separator.pack(pady=(20, 5))

            # --- Election ComboBox ---
        ctk.CTkLabel(frame, text="Select Election:", font=('Arial', 12)).pack(pady=(5, 0))
        self.election_var = ctk.StringVar()
        self.election_combo = ctk.CTkComboBox(
            frame, variable=self.election_var, width=300,
            values=[], state="readonly", command=self.on_election_select
        )
        self.election_combo.pack(pady=5)

        # --- District ComboBox ---
        ctk.CTkLabel(frame, text="Select District:", font=('Arial', 12)).pack(pady=(10, 0))
        self.district_var = ctk.StringVar()
        self.district_combo = ctk.CTkComboBox(
            frame, variable=self.district_var, width=300,
            values=[], state="readonly", command=self.on_district_select
        )
        self.district_combo.pack(pady=5)

        # --- Election Info Labels ---
        info_frame = ctk.CTkFrame(frame, )#fg_color="transparent")
        info_frame.pack(pady=15)

        self.start_label = ctk.CTkLabel(info_frame, text="Start Date: -", font=('Arial', 12))
        self.start_label.pack(side="left", padx=10)
        #self.start_date.bind("<Button-1>", self.open_calendar_start)
        
        self.end_label = ctk.CTkLabel(info_frame, text="End Date: -", font=('Arial', 12))
        self.end_label.pack(side="left", padx=10)
        #self.end_date.bind("<Button-1>", self.open_calendar_end)
        CTkDatePicker(self, self.start_date, mode="election")
        CTkDatePicker(self, self.end_date, mode="election")

        self.status_label = ctk.CTkLabel(info_frame, text="Status: -", font=('Arial', 12))
        self.status_label.pack(side="left", padx=10)


        # Load elections initially
        self.load_elections()

    def open_calendar_start(self, event=None):
        self.show_calendar(self.start_date)

    def open_calendar_end(self, event=None):
        self.show_calendar(self.end_date)

    def show_calendar(self, target_entry):
        # Prevent multiple popups
        if hasattr(self, "cal_window") and self.cal_window.winfo_exists():
            return

        # Create popup window
        self.cal_window = Toplevel(self)
        self.cal_window.title("Select Date")

        # Position popup near entry
        x = target_entry.winfo_rootx()
        y = target_entry.winfo_rooty() + 40
        self.cal_window.geometry(f"+{x}+{y}")

        # Calendar widget
        cal = Calendar(self.cal_window, selectmode="mounth", date_pattern="yyyy-mm-dd")
        cal.pack(pady=10)

        def set_date(event=None):
            date_val = cal.get_date()
            target_entry.delete(0, "end")
            target_entry.insert(0, date_val)
            self.cal_window.destroy()

        cal.bind("<<CalendarSelected>>", set_date)


    def create_election(self):
        name = self.election_name.get().strip()
        start = self.start_date.get().strip()
        end = self.end_date.get().strip()

        if not all([name, start, end]):
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            # Convert date strings to date objects
            start_date = datetime.strptime(start, "%Y-%m-%d").date()
            end_date = datetime.strptime(end, "%Y-%m-%d").date()
            today = datetime.now().date()
        except ValueError:
            messagebox.showerror("Error", "Invalid date format! Please use YYYY-MM-DD.")

        try:
            if not self.blockchain.w3.is_connected():
                messagebox.showerror("Error", "Not connected to Ganache. Please start Ganache first.")
                return

            if not self.blockchain.contract:
                contract_address = self.blockchain.deploy_contract()
                messagebox.showinfo("Success", f"Smart contract deployed at: {contract_address}")
            # ✅ Validation Rules
            """if start_date <= today:
                messagebox.showerror("Invalid Date", "Election cannot start today or in the past.")
                return"""

            # ✅ Create election for all Karnataka districts
            for district in KARNATAKA_DISTRICTS:
                blockchain_election_id = self.blockchain.create_election(name, district)
                election_id = self.db.create_election(name, district, start_date, end_date)
                print(blockchain_election_id)
                print(election_id)
                voters = self.db.get_voters_by_district_bc(district)  # list of (voter_id, name, district, blockchain_address)

                for voter in voters:
                    address,voter_id = voter

                    # register voter in that election
                    self.blockchain.register_voter_on_blockchain(election_id, address)

                self.db.update_election_contract(election_id, self.blockchain.contract_address)

            messagebox.showinfo("Success", f"Election '{name}' created for all Karnataka districts!")
            self.election_name.delete(0, 'end')
            self.start_date.delete(0, 'end')
            self.end_date.delete(0, 'end')

        except Exception as e:
            messagebox.showerror("Error", f"Failed to create elections: {e}")

        self.load_elections()

    def load_elections(self):
        """Load all elections into the first ComboBox."""
        self.elections = self.db.get_elections()
        election_names = sorted(list(set([e[1] for e in self.elections])))  # Unique election names
        self.election_combo.configure(values=election_names)
        if election_names:
            self.election_combo.set("Select Election")
        self.district_combo.configure(values=[])


    def on_election_select(self, selected_name):
        """Triggered when an election is selected."""
        # Get districts for the selected election
        districts = [e[2] for e in self.elections if e[1] == selected_name]
        self.district_combo.configure(values=districts)
        self.district_combo.set("Select District")

        # Reset info display
        self.start_label.configure(text="Start Date: -")
        self.end_label.configure(text="End Date: -")
        self.status_label.configure(text="Status: -")


    def on_district_select(self, selected_district):
        """Triggered when a district is selected."""
        selected_election = self.election_var.get()
        start_date = "-"
        end_date = "-"
        status = "-"
        for e in self.elections:
            if e[1] == selected_election and e[2] == selected_district:
                start_date = e[3]
                end_date = e[4]
                status = e[6]
                break
        self.start_label.configure(text=f"Start Date: {start_date}")
        self.end_label.configure(text=f"End Date: {end_date}")
        self.status_label.configure(text=f"Status: {status}")
            
        color = "#27ae60" if status.lower() == "active" else "#e67e22" if status.lower() == "pending" else "#e74c3c"
        self.status_label.configure(text=f"Status: {status}", text_color=color)




    def logout(self):
        self.destroy()
        self.on_logout()


        # ================= Candidate Tab =================
    def create_candidate_tab(self):
        print("create cand tab")
        frame = ctk.CTkFrame(self.tab_candidate)
        frame.pack(pady=15, padx=15, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Manage Candidates", font=('Arial', 16, 'bold')).pack(pady=5)

        # --- Election Selection (Pending Only) ---
        #ctk.CTkLabel(frame, text="Select Pending Election:", font=('Arial', 12)).pack(pady=(5, 0))
        self.cand_election = ctk.StringVar()
        self.cand_election_combo = ctk.CTkComboBox(
            frame, variable=self.cand_election, width=280,
            values=[], state="readonly"
        )
        self.cand_election_combo.pack(pady=5)
        self.load_pending_elections()

        # --- Candidate Name ---
        self.cand_name = ctk.CTkEntry(frame, placeholder_text="Candidate Name", width=280)
        self.cand_name.pack(pady=5)

        # --- District (auto-filled from election) ---
        #ctk.CTkLabel(frame, text="Select District:", font=('Arial', 12)).pack(pady=(5, 0))
        self.cand_district = ctk.CTkComboBox(frame, values=KARNATAKA_DISTRICTS, width=280)
        self.cand_district.pack(pady=5)

        # --- Party Selection ---
        #ctk.CTkLabel(frame, text="Select Party:", font=('Arial', 12)).pack(pady=(5, 0))

        # Official parties and their official symbols
        self.PARTY_SYMBOLS = {
            "Bharatiya Janata Party (BJP)": "Lotus 🌸",
            "Indian National Congress (INC)": "Hand ✋",
            "Janata Dal (Secular) (JD(S))": "Farmer Hat 👒",
            "Aam Aadmi Party (AAP)": "Broom 🧹",
            "Bahujan Samaj Party (BSP)": "Elephant 🐘",
            "Independent": None  # special case
        }

        self.party_var = ctk.StringVar(value="Independent")
        self.party_combo = ctk.CTkComboBox(
            frame,
            variable=self.party_var,
            width=280,
            values=list(self.PARTY_SYMBOLS.keys()),
            command=self.on_party_select
        )
        self.party_combo.pack(pady=5)

        # --- Party Symbol ComboBox ---
        # Two different symbol lists (one neutral set for independents only)
        self.independent_symbols = ["Star ⭐", "Candle 🕯️", "Clock 🕒", "Book 📘", "Tree 🌳", "Sun ☀️"]
        self.party_symbol_combo = ctk.CTkComboBox(
            frame,
            width=280,
            values=self.independent_symbols,  # default for independent
            state="normal"
        )
        self.party_symbol_combo.pack(pady=5)

        # Initialize
        self.on_party_select(self.party_var.get())


        # --- Buttons ---
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="Add Candidate", fg_color="#27ae60",
                      command=self.add_candidate, width=120).grid(row=0, column=0, padx=5)
        ctk.CTkButton(btn_frame, text="Update Candidate", fg_color="#2980b9",
                      command=self.update_candidate, width=120).grid(row=0, column=1, padx=5)
        ctk.CTkButton(btn_frame, text="Delete Candidate", fg_color="#e67e22",
                      command=self.delete_candidate, width=120).grid(row=0, column=2, padx=5)

        # ---------------- EXISTING CANDIDATES SECTION ----------------
        separator = ctk.CTkLabel(frame, text="View Existing Candidates", font=('Arial', 14, 'bold'))
        separator.pack(pady=(20, 5))

        # --- Election ComboBox ---
        srow = ctk.CTkFrame(frame, fg_color="transparent")
        srow.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(srow, text="Select Election:", font=('Arial', 13, 'bold')).pack(side="left",padx=(5, 0))
        self.cand_election_var = ctk.StringVar()
        self.cand_election_var_combo = ctk.CTkComboBox(
            srow, variable=self.cand_election_var, width=300,
            values=[], state="readonly", command=self.on_candidate_election_select
        )
        self.cand_election_var_combo.pack(side="left")

        # --- District ComboBox ---
        ctk.CTkLabel(srow, text="Select District:", font=('Arial', 13, 'bold')).pack(side="left",padx=(10, 0))
        self.cand_district_var = ctk.StringVar()
        self.cand_district_var_combo = ctk.CTkComboBox(
            srow, variable=self.cand_district_var, width=300,
            values=[], state="readonly", command=self.on_candidate_district_select
        )
        self.cand_district_var_combo.pack(side="left")

        # --- Candidate Table ---
        ctk.CTkLabel(frame, text="Candidates List", font=('Arial', 12, 'bold')).pack(pady=(15, 5))
        self.candidate_tree = ttk.Treeview(
            frame, columns=("Name", "Party", "Symbol"),
            show="headings", height=8
        )
        for col in ("Name", "Party", "Symbol"):
            self.candidate_tree.heading(col, text=col)
            self.candidate_tree.column(col, anchor="center", width=200)
        self.candidate_tree.pack(pady=10, fill="x", expand=True)
        self.candidate_tree.bind("<ButtonRelease-1>", self.on_candidate_select)

        # Load all existing elections
        self.load_candidate_elections()
        self.selected_candidate = None


    """def load_candidates(self):
        for i in self.candidate_tree.get_children():
            self.candidate_tree.delete(i)
        for cand in self.db.get_candidates():
            self.candidate_tree.insert("", "end", values=cand)"""

    def on_party_select(self, selected_party: str):
        """Automatically handle party symbol based on selection."""
        selected_party = selected_party.strip()

        if selected_party == "Independent":
            # Allow choosing from neutral symbols
            self.party_symbol_combo.configure(values=self.independent_symbols, state="normal")
            if not self.party_symbol_combo.get() or self.party_symbol_combo.get() not in self.independent_symbols:
                self.party_symbol_combo.set("Select Symbol")
        else:
            # Lock symbol to official one
            symbol = self.PARTY_SYMBOLS.get(selected_party, "")
            self.party_symbol_combo.configure(values=[symbol], state="disabled")
            self.party_symbol_combo.set(symbol)

    def load_pending_elections(self):
        """Load only pending elections into the dropdown."""
        all_elections = self.db.get_elections()
        pending = sorted(list(set([f"{e[1]}" for e in all_elections if e[6].lower() == "active"])))
        self.cand_election_combo.configure(values=pending)
        if pending:
            self.cand_election_combo.set("Select Election")

    def add_candidate(self):
        election_text = self.cand_election.get().strip()
        name = self.cand_name.get().strip()
        district = self.cand_district.get().strip()
        party = self.party_var.get().strip()
        symbol = self.party_symbol_combo.get().strip()

        # Independent candidate must pick neutral symbol
        if party == "Independent":
            if symbol not in self.independent_symbols:
                messagebox.showerror("Error", "Please select a valid neutral symbol for Independent candidate.")
                return
        else:
            # Force correct party symbol
            symbol = self.PARTY_SYMBOLS.get(party, symbol)

        if not all([election_text, name, district, party, symbol]):
            messagebox.showerror("Error", "All fields are required!")
            return

        # Get election_id from DB
        election_id = None
        for e in self.db.get_elections():
            if e[1] in election_text and e[2] in district:
                print(e[1],e[2])
                election_id = e[0]
                break

        if not election_id:
            messagebox.showerror("Error", "Invalid election selected!")
            return
        self.blockchain.add_candidate(election_id, name, party)
        self.db.add_candidate(election_id, name, party, symbol)
        messagebox.showinfo("Success", "Candidate added successfully!") 
        self.clear_candidate_form()

    def update_candidate(self):
        if not self.selected_candidate:
            messagebox.showerror("Error", "Select a candidate to update!")
            return

        election_text = self.cand_election.get().strip()
        name = self.cand_name.get().strip()
        district = self.cand_district.get().strip()
        party = self.party_var.get().strip()
        symbol = self.party_symbol_combo.get().strip()

        election_id = None
        for e in self.db.get_elections():
            if e[1] in election_text and e[2] in election_text:
                election_id = e[0]
                break

        if not all([name, district, party, symbol]) or not election_id:
            messagebox.showerror("Error", "All fields are required!")
            return

        self.db.update_candidate(self.selected_candidate, election_id, name, party, symbol)
        messagebox.showinfo("Success", "Candidate updated successfully!")
        self.clear_candidate_form()
        self.clear_candidate_table()

    def delete_candidate(self):
        selected = self.candidate_tree.selection()
        print(selected)
        if not selected:
            messagebox.showerror("Error", "Select a candidate to delete.")
            return
        name = self.candidate_tree.item(selected[0], "values")[0]
        print(name)
        confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete candidate '{name}'?")
        if not confirm:
            return
        self.db.delete_candidate(name)
        messagebox.showinfo("Deleted", f"Candidate '{name}' removed.")
        self.clear_candidate_form()
        self.clear_candidate_table()

    def clear_candidate_form(self):
        self.cand_name.delete(0, 'end')
        self.party_symbol_combo.set("Select Symbol")
        self.party_var.set('Independent')
        self.cand_district.set('')
        self.cand_election_combo.set('Select Election')

    def load_candidate_elections(self):
        """Load unique elections for filtering candidates."""
        elections = self.db.get_elections()
        election_names = sorted(list(set([e[1] for e in elections])))
        self.cand_election_var_combo.configure(values=election_names)
        if election_names:
            self.cand_election_var_combo.set("Select Election")
        self.cand_district_var_combo.configure(values=[])

    def on_candidate_election_select(self, selected_election):
        """Populate district ComboBox when election is selected."""
        elections = self.db.get_elections()
        districts = [e[2] for e in elections if e[1] == selected_election]
        self.cand_district_var_combo.configure(values=districts)
        if districts:
            self.cand_district_var_combo.set("Select District")
        self.clear_candidate_table()

    def on_candidate_district_select(self, selected_district):
        """Load candidates based on selected election and district."""
        selected_election = self.cand_election_var.get()
        candidates = self.db.get_candidates_filtered(selected_election, selected_district)
        self.clear_candidate_table()
        for cand in candidates:
            self.candidate_tree.insert("", "end", values=(cand[2], cand[3], cand[4]))

    def on_candidate_select(self, event):
        selected = self.candidate_tree.selection()
        selected_election = self.cand_election_var.get().strip()
        selected_district = self.cand_district_var.get().strip()
        if selected:
            vals = self.candidate_tree.item(selected[0], "values")
            print(vals)
            self.selected_candidate = vals[0]
            self.cand_election.set(selected_election)
            self.cand_name.delete(0, 'end')
            self.cand_name.insert(0, vals[0])
            self.cand_district.set(selected_district)
            self.party_var.set(vals[1])
            if vals[2]==["Independent"]:
                self.on_party_select(self.party_var.get())
            self.party_symbol_combo.set(vals[2])
            
    def clear_candidate_table(self):
        """Remove all rows from Treeview."""
        for i in self.candidate_tree.get_children():
            self.candidate_tree.delete(i)

    def refresh_candidate_table(self):
        """Refresh the candidate view table when switching tabs."""
        election = self.cand_election_var.get()
        district = self.cand_district_var.get()

        # Clear tree
        for i in self.candidate_tree.get_children():
            self.candidate_tree.delete(i)

        # Load only if both selected
        if election and district and election != "Select Election" and district != "Select District":
            for cand in self.db.get_candidates_by_election_district(election, district):
                self.candidate_tree.insert("", "end", values=cand)


        # ================= Lifecycle Tab =================
    def create_lifecycle_tab(self):
        self.lifecycle_timer_id = None  # for countdown refresh

        frame = ctk.CTkFrame(self.tab_lifecycle)
        frame.pack(pady=15, padx=15, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Election Lifecycle Management", font=('Arial', 18, 'bold')).pack(pady=(5, 15))

        # --- Top row: selections
        sel_row = ctk.CTkFrame(frame, fg_color="transparent")
        sel_row.pack(fill="x", pady=(0, 10))

        # Election selector
        ctk.CTkLabel(sel_row, text="Election:", font=('Arial', 12)).pack(side="left", padx=(0, 8))
        self.life_election_var = ctk.StringVar()
        self.life_election_combo = ctk.CTkComboBox(
            sel_row, variable=self.life_election_var, width=260,
            values=[], state="readonly", command=self.on_lifecycle_election_select
        )
        self.life_election_combo.pack(side="left")

        # District selector
        ctk.CTkLabel(sel_row, text="   District:", font=('Arial', 12)).pack(side="left", padx=(16, 8))
        self.life_district_var = ctk.StringVar()
        self.life_district_combo = ctk.CTkComboBox(
            sel_row, variable=self.life_district_var, width=260,
            values=[], state="readonly", command=self.on_lifecycle_district_select
        )
        self.life_district_combo.pack(side="left")

        # --- Info strip: start/end/status in one line
        info_strip = ctk.CTkFrame(frame, fg_color="transparent")
        info_strip.pack(fill="x", pady=(6, 6))

        self.life_start_lbl  = ctk.CTkLabel(info_strip, text="Start Date: -", font=('Arial', 12))
        self.life_end_lbl    = ctk.CTkLabel(info_strip, text="End Date: -", font=('Arial', 12))
        self.life_status_lbl = ctk.CTkLabel(info_strip, text="Status: -", font=('Arial', 12))

        self.life_start_lbl.pack(side="left", padx=8)
        self.life_end_lbl.pack(side="left", padx=8)
        self.life_status_lbl.pack(side="left", padx=8)

        # Countdown + Blockchain row
        meta_row = ctk.CTkFrame(frame, fg_color="transparent")
        meta_row.pack(fill="x", pady=(4, 10))

        self.label_1 = ctk.CTkLabel(meta_row, text="Live Voting Status:", font=('Arial', 16, 'bold'))
        self.label_1.pack(side="left", padx=8)

        self.bc_status_label = ctk.CTkLabel(meta_row, text="🔴 Blockchain Disconnected", font=('Arial', 12), text_color="#e74c3c")
        self.bc_status_label.pack(side="right", padx=8)

        # Vote progress
        prog_card = ctk.CTkFrame(frame)
        prog_card.pack(fill="x", pady=(6, 12), padx=2)

        ctk.CTkLabel(prog_card, text="Voting Progress", font=('Arial', 14, 'bold')).pack(pady=(10, 6))
        self.vote_progress = ctk.CTkProgressBar(prog_card)
        self.vote_progress.set(0)
        self.vote_progress.pack(fill="x", padx=12, pady=(0, 6))
        self.vote_summary_lbl = ctk.CTkLabel(prog_card, text="Votes Cast: 0/0 (0.00%)", font=('Arial', 12))
        self.vote_summary_lbl.pack(pady=(0, 10))

        # Actions row
        actions = ctk.CTkFrame(frame, fg_color="transparent")
        actions.pack(fill="x", pady=(6, 6))

        self.view_results_btn = ctk.CTkButton(actions, text="📊 View Results", fg_color="#2ecc71",
                                              command=self.view_results_shortcut)
        self.view_results_btn.pack(side="left", padx=6)

        self.finalize_btn = ctk.CTkButton(actions, text="✅ Finalize Election", fg_color="#8e44ad",
                                          command=self.finalize_selected_election)
        self.finalize_btn.pack(side="left", padx=6)

        # load data
        self.load_lifecycle_elections()
        self.update_blockchain_indicator()
        

    def load_lifecycle_elections(self):
        """Fill the lifecycle election combobox with unique election names."""
        self.elections = self.db.get_elections()  # same shape as elsewhere
        names = sorted(list({e[1] for e in self.elections}))  # unique names
        self.life_election_combo.configure(values=names or ["No elections"])
        self.life_election_combo.set("Select Election" if names else "No elections")
        self.life_district_combo.configure(values=[])
        # Clear info
        for lbl, text in zip(
            [self.life_start_lbl, self.life_end_lbl, self.life_status_lbl, self.vote_summary_lbl],
            ["Start Date: -", "End Date: -", "Status: -", "Votes Cast: 0/0 (0.00%)"]
        ):
            lbl.configure(text=text)
        self.vote_progress.set(0)
        self.set_action_buttons_state(enabled=False)

    def on_lifecycle_election_select(self, selected_name):
        """When an election name is chosen, fill districts."""
        if self.lifecycle_timer_id:
            self.after_cancel(self.lifecycle_timer_id)
            self.lifecycle_timer_id = None

        districts = [e[2] for e in self.elections if e[1] == selected_name]
        self.life_district_combo.configure(values=districts or [])
        self.life_district_combo.set("Select District" if districts else "")
        # Reset info
        for lbl, text in zip(
            [self.life_start_lbl, self.life_end_lbl, self.vote_summary_lbl],
            ["Start Date: -", "End Date: -", "Votes Cast: 0/0 (0.00%)"]
        ):
            lbl.configure(text=text)
        self.vote_progress.set(0)
        self.set_action_buttons_state(enabled=False)

    def on_lifecycle_district_select(self, selected_district):
        """When district selected, show info + start countdown + progress."""
        rec = self._get_selected_election_record()
        if not rec:
            return
        # rec format: (id, name, district, start_date, end_date, contract_address, status, created_at)
        _, _, _, start_date, end_date, _, status, _ = rec

        self.life_start_lbl.configure(text=f"Start Date: {start_date}")
        self.life_end_lbl.configure(text=f"End Date: {end_date}")

        # color badge
        color = {"active": "#2ecc71", "pending": "#f1c40f", "completed": "#3498db", "archived": "#7f8c8d"}.get(status.lower(), "#7f8c8d")
        self.life_status_lbl.configure(text=f"Status: {status.title()}", text_color=color)

        # vote progress
        self.update_vote_progress()

        # enable/disable action buttons
        self.set_action_buttons_state(enabled=True, status=status)

    def _get_selected_election_record(self):
        """Return the single election row for current lifecycle selections."""
        name = self.life_election_var.get().strip()
        district = self.life_district_var.get().strip()
        for e in self.elections:
            if e[1] == name and e[2] == district:
                return e
        return None

    """def _start_countdown(self, end_date_str):
        #Start a 1-second ticking countdown to standard end time 17:00.
        from datetime import datetime, timedelta
        try:
            # standard voting window 08:00–17:00; countdown to end of day time
            end_dt = datetime.fromisoformat(f"{end_date_str} 17:00:00")
        except Exception:
            self.countdown_label.configure(text="🕒 Time Remaining: -")
            return

        def tick():
            from datetime import datetime
            now = datetime.now()
            remaining = (end_dt - now).total_seconds()
            if remaining > 0:
                hrs = int(remaining // 3600)
                mins = int((remaining % 3600) // 60)
                secs = int(remaining % 60)
                self.countdown_label.configure(text=f"🕒 Time Remaining: {hrs:02}:{mins:02}:{secs:02}")
                self.lifecycle_timer_id = self.after(1000, tick)
            else:
                self.countdown_label.configure(text="🕒 Voting Ended")

        # start ticking
        if self.lifecycle_timer_id:
            self.after_cancel(self.lifecycle_timer_id)
        tick()"""

    def update_vote_progress(self):
        """Compute total votes vs voters for this district election and update progress bar."""
        rec = self._get_selected_election_record()
        if not rec:
            self.vote_progress.set(0)
            self.vote_summary_lbl.configure(text="Votes Cast: 0/0 (0.00%)")
            return
        election_id, _, district, *_ = rec
        total_voters = self.db.count_voters_in_district(district)
        total_votes  = self.db.count_votes_in_election(election_id)
        percent = (total_votes / total_voters) * 100 if total_voters else 0.0
        self.vote_progress.set(percent / 100.0)
        self.vote_summary_lbl.configure(text=f"Votes Cast: {total_votes}/{total_voters} ({percent:.2f}%)")

    def auto_update_status(self):
        """Update lifecycle based on current datetime and standard window."""
        from datetime import datetime
        now = datetime.now()

        changed = False
        for e in self.elections:
            election_id, _, _, start_date, end_date, _, status, _ = e
            try:
                start_dt = datetime.fromisoformat(f"{start_date} 06:00:00")
                end_dt   = datetime.fromisoformat(f"{end_date} 22:00:00")
            except Exception:
                continue

            new_status = status
            if status == "archived":
                continue
            elif now < start_dt:
                new_status = "pending"
            elif start_dt <= now <= end_dt:
                new_status = "active"
            elif now > end_dt:
                new_status = "completed"

            if new_status != status:
                self.db.update_election_status(election_id, new_status)
                changed = True

        if changed:
            # reload lists and keep current selections if possible
            prev_name = self.life_election_var.get()
            prev_dist = self.life_district_var.get()
            self.load_lifecycle_elections()
            # restore selections if still present
            if prev_name in [e[1] for e in self.elections]:
                self.life_election_combo.set(prev_name)
                self.on_lifecycle_election_select(prev_name)
                dists = [e[2] for e in self.elections if e[1] == prev_name]
                if prev_dist in dists:
                    self.life_district_combo.set(prev_dist)
                    self.on_lifecycle_district_select(prev_dist)
        else:
            # just refresh current view
            self.on_lifecycle_district_select(self.life_district_var.get())

        self.update_blockchain_indicator()
        self.after(1000*60, self.auto_update_status)

    def set_action_buttons_state(self, enabled: bool, status: str = "-"):
        if not enabled:
            self.view_results_btn.configure(state="disabled")
            self.finalize_btn.configure(state="disabled")
            return
        st = (status or "").lower()
        self.view_results_btn.configure(state=("normal" if st in ("completed", "archived") else "disabled"))
        self.finalize_btn.configure(state=("normal" if st == "completed" else "disabled"))

    def update_blockchain_indicator(self):
        # optional: lazy import to avoid hard dependency if not present
        try:
            from src.utils.blockchain import BlockchainManager
            if not hasattr(self, "_bc"):
                self._bc = BlockchainManager()
            ok = self._bc.w3.is_connected()
        except Exception:
            ok = False
        if ok:
            self.bc_status_label.configure(text="🟢 Blockchain Connected", text_color="#2ecc71")
        else:
            self.bc_status_label.configure(text="🔴 Blockchain Disconnected", text_color="#e74c3c")

    def view_results_shortcut(self):
        """Open results for selected election (reuse your existing results logic)."""
        rec = self._get_selected_election_record()
        if not rec:
            messagebox.showerror("Error", "Select election and district first.")
            return
        election_id = rec[0]
        # If you already have a results viewer, call it here.
        # Minimal inline popup:
        try:
            results = self._bc.get_all_results(election_id)
            print(results)
            # Build a simple popup
            win = ctk.CTkToplevel(self)
            win.title("Election Results")
            win.geometry("520x420")
            ctk.CTkLabel(win, text="Results", font=("Arial", 16, "bold")).pack(pady=10)
            tv = ttk.Treeview(win, columns=("Candidate", "Party", "Votes"), show="headings", height=12)
            tv.heading("Candidate", text="Candidate")
            tv.heading("Party", text="Party")
            tv.heading("Votes", text="Votes")
            tv.pack(fill="both", expand=True, padx=12, pady=12)
            for _, cand_name, party, vote_count in results:
                tv.insert("", "end", values=(cand_name, party, vote_count))
        except Exception as e:
            messagebox.showerror("Error", f"Unable to load results: {e}")

    def finalize_selected_election(self):
        rec = self._get_selected_election_record()
        if not rec:
            messagebox.showerror("Error", "Select election and district first.")
            return
        election_id = rec[0]
        # mark archived
        try:
            self._bc.finalize_election(election_id)
                
            winner = self._bc.get_winner(election_id)
                
            messagebox.showinfo(
                "Election Finalized",
                f"Winner: {winner[0]}\nParty: {winner[1]}\nVotes: {winner[2]}"
            )
            self.db.update_election_status(election_id, "archived")
            self.auto_update_status()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to finalize election: {str(e)}")
            self.db.update_election_status(election_id, "archived")



