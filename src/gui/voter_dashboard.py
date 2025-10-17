import tkinter as tk
from tkinter import ttk, messagebox
from src.utils.database import Database
from src.utils.blockchain import BlockchainManager

class VoterDashboard:
    def __init__(self, root, username, on_logout):
        self.root = root
        self.username = username
        self.on_logout = on_logout
        self.db = Database()
        self.blockchain = BlockchainManager()
        
        self.root.title("Mata Raksha - Voter Portal")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        self.create_widgets()
    
    def create_widgets(self):
        header_frame = tk.Frame(self.root, bg='#34495e', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="VOTER PORTAL",
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
        
        elections_tab = tk.Frame(notebook, bg='#ecf0f1')
        results_tab = tk.Frame(notebook, bg='#ecf0f1')
        
        notebook.add(elections_tab, text='View Elections')
        notebook.add(results_tab, text='View Results')
        
        self.create_elections_tab(elections_tab)
        self.create_results_tab(results_tab)
    
    def create_elections_tab(self, parent):
        control_frame = tk.Frame(parent, bg='#ecf0f1')
        control_frame.pack(pady=20, padx=30, fill='x')
        
        tk.Label(control_frame, text="Select Election:", font=('Arial', 12), bg='#ecf0f1').pack(side='left', padx=10)
        self.election_var = tk.StringVar()
        self.election_combo = ttk.Combobox(control_frame, textvariable=self.election_var, font=('Arial', 12), width=35, state='readonly')
        self.election_combo.pack(side='left', padx=10)
        
        view_btn = tk.Button(
            control_frame,
            text="View Candidates",
            font=('Arial', 11),
            bg='#3498db',
            fg='white',
            command=self.view_candidates,
            cursor='hand2',
            padx=15,
            pady=5
        )
        view_btn.pack(side='left', padx=10)
        
        self.candidates_text = tk.Text(parent, font=('Arial', 11), height=20, bg='white')
        self.candidates_text.pack(fill='both', expand=True, padx=30, pady=10)
        
        self.load_elections()
    
    def create_results_tab(self, parent):
        control_frame = tk.Frame(parent, bg='#ecf0f1')
        control_frame.pack(pady=20, padx=30, fill='x')
        
        tk.Label(control_frame, text="Select Election:", font=('Arial', 12), bg='#ecf0f1').pack(side='left', padx=10)
        self.results_election_var = tk.StringVar()
        self.results_election_combo = ttk.Combobox(control_frame, textvariable=self.results_election_var, font=('Arial', 12), width=35, state='readonly')
        self.results_election_combo.pack(side='left', padx=10)
        
        view_btn = tk.Button(
            control_frame,
            text="View Results",
            font=('Arial', 11),
            bg='#27ae60',
            fg='white',
            command=self.view_results,
            cursor='hand2',
            padx=15,
            pady=5
        )
        view_btn.pack(side='left', padx=10)
        
        self.results_text = tk.Text(parent, font=('Arial', 11), height=20, bg='white')
        self.results_text.pack(fill='both', expand=True, padx=30, pady=10)
        
        self.load_elections_for_results()
    
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
    
    def view_candidates(self):
        election_text = self.election_var.get()
        
        if not election_text:
            messagebox.showerror("Error", "Please select an election")
            return
        
        try:
            election_id = int(election_text.split('ID:')[1].split(')')[0])
            
            candidates = self.db.get_candidates_by_election(election_id)
            
            self.candidates_text.delete(1.0, tk.END)
            self.candidates_text.insert(tk.END, f"CANDIDATES - {election_text}\n")
            self.candidates_text.insert(tk.END, "=" * 60 + "\n\n")
            
            if not candidates:
                self.candidates_text.insert(tk.END, "No candidates found for this election\n")
            else:
                for idx, candidate in enumerate(candidates, 1):
                    self.candidates_text.insert(tk.END, f"{idx}. Candidate: {candidate[2]}\n")
                    self.candidates_text.insert(tk.END, f"   Party: {candidate[3]}\n")
                    self.candidates_text.insert(tk.END, f"   Symbol: {candidate[4] or 'N/A'}\n")
                    self.candidates_text.insert(tk.END, "-" * 60 + "\n")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to view candidates: {str(e)}")
    
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
                
                sorted_results = sorted(results, key=lambda x: x['votes'], reverse=True)
                
                for idx, result in enumerate(sorted_results, 1):
                    self.results_text.insert(tk.END, f"{idx}. Candidate: {result['name']}\n")
                    self.results_text.insert(tk.END, f"   Party: {result['party']}\n")
                    self.results_text.insert(tk.END, f"   Votes: {result['votes']}\n")
                    self.results_text.insert(tk.END, "-" * 60 + "\n")
            else:
                messagebox.showerror("Error", "No blockchain results available for this election")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to view results: {str(e)}")
