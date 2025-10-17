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
