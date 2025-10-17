import tkinter as tk
from tkinter import ttk, messagebox
from src.utils.database import Database
from src.utils.biometric import BiometricSimulator
from src.utils.blockchain import BlockchainManager

class OfficerDashboard:
    def __init__(self, root, username, on_logout):
        self.root = root
        self.username = username
        self.on_logout = on_logout
        self.db = Database()
        self.biometric = BiometricSimulator()
        self.blockchain = BlockchainManager()
        
        self.current_voter = None
        self.current_election = None
        
        self.root.title("Mata Raksha - Election Officer Dashboard")
        self.root.geometry("800x700")
        self.root.configure(bg='#2c3e50')
        
        self.create_widgets()
    
    def create_widgets(self):
        header_frame = tk.Frame(self.root, bg='#34495e', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="ELECTION OFFICER DASHBOARD",
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
        
        verify_frame = tk.Frame(self.root, bg='#ecf0f1', padx=30, pady=20)
        verify_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(verify_frame, text="Step 1: Verify Voter", font=('Arial', 14, 'bold'), bg='#ecf0f1').pack(pady=10)
        
        verify_controls = tk.Frame(verify_frame, bg='#ecf0f1')
        verify_controls.pack(pady=10)
        
        tk.Label(verify_controls, text="Voter ID:", font=('Arial', 12), bg='#ecf0f1').pack(side='left', padx=5)
        self.voter_id_entry = tk.Entry(verify_controls, font=('Arial', 12), width=25)
        self.voter_id_entry.pack(side='left', padx=5)
        
        verify_btn = tk.Button(
            verify_controls,
            text="Verify Fingerprint",
            font=('Arial', 11),
            bg='#3498db',
            fg='white',
            command=self.verify_voter,
            cursor='hand2',
            padx=15,
            pady=8
        )
        verify_btn.pack(side='left', padx=10)
        
        self.voter_info_label = tk.Label(
            verify_frame,
            text="No voter verified",
            font=('Arial', 11),
            bg='#ecf0f1',
            fg='#95a5a6'
        )
        self.voter_info_label.pack(pady=10)
        
        vote_frame = tk.Frame(self.root, bg='#ecf0f1', padx=30, pady=20)
        vote_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        tk.Label(vote_frame, text="Step 2: Cast Vote", font=('Arial', 14, 'bold'), bg='#ecf0f1').pack(pady=10)
        
        election_controls = tk.Frame(vote_frame, bg='#ecf0f1')
        election_controls.pack(pady=10)
        
        tk.Label(election_controls, text="Select Election:", font=('Arial', 12), bg='#ecf0f1').pack(side='left', padx=5)
        self.election_var = tk.StringVar()
        self.election_combo = ttk.Combobox(election_controls, textvariable=self.election_var, font=('Arial', 11), width=35, state='readonly')
        self.election_combo.pack(side='left', padx=5)
        self.election_combo.bind('<<ComboboxSelected>>', self.load_candidates)
        
        self.load_elections()
        
        candidates_container = tk.Frame(vote_frame, bg='#ecf0f1')
        candidates_container.pack(fill='both', expand=True, pady=10)
        
        tk.Label(candidates_container, text="Candidates:", font=('Arial', 12, 'bold'), bg='#ecf0f1').pack(anchor='w')
        
        self.candidates_frame = tk.Frame(candidates_container, bg='white', relief='solid', borderwidth=1)
        self.candidates_frame.pack(fill='both', expand=True, pady=5)
        
        self.candidate_var = tk.IntVar(value=0)
        
        vote_btn = tk.Button(
            vote_frame,
            text="Submit Vote to Blockchain",
            font=('Arial', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            command=self.submit_vote,
            cursor='hand2',
            padx=30,
            pady=12
        )
        vote_btn.pack(pady=15)
    
    def verify_voter(self):
        voter_id = self.voter_id_entry.get().strip()
        
        if not voter_id:
            messagebox.showerror("Error", "Please enter Voter ID")
            return
        
        voter = self.db.get_voter_by_id(voter_id)
        
        if not voter:
            messagebox.showerror("Error", "Voter not found")
            return
        
        simulated_scan = self.biometric.simulate_fingerprint_scan()
        
        if messagebox.askyesno("Fingerprint Verification", "Place finger on scanner for verification"):
            stored_fingerprint = voter[5]
            
            if self.biometric.verify_fingerprint(stored_fingerprint, stored_fingerprint):
                self.current_voter = voter
                
                self.voter_info_label.config(
                    text=f"✓ Verified: {voter[2]} | District: {voter[4]} | ID: {voter[1]}",
                    fg='#27ae60'
                )
                
                messagebox.showinfo("Success", f"Voter verified successfully!\nName: {voter[2]}\nDistrict: {voter[4]}")
            else:
                messagebox.showerror("Error", "Fingerprint verification failed")
    
    def load_elections(self):
        elections = self.db.get_elections()
        election_list = [f"{e[1]} - {e[2]} (ID:{e[0]})" for e in elections if e[6] == 'active']
        self.election_combo['values'] = election_list
        if election_list:
            self.election_combo.current(0)
            self.load_candidates()
    
    def load_candidates(self, event=None):
        for widget in self.candidates_frame.winfo_children():
            widget.destroy()
        
        election_text = self.election_var.get()
        
        if not election_text:
            return
        
        try:
            election_id = int(election_text.split('ID:')[1].split(')')[0])
            self.current_election = election_id
            
            candidates = self.db.get_candidates_by_election(election_id)
            
            if not candidates:
                tk.Label(
                    self.candidates_frame,
                    text="No candidates found",
                    font=('Arial', 11),
                    bg='white',
                    fg='#95a5a6'
                ).pack(pady=20)
                return
            
            for idx, candidate in enumerate(candidates):
                candidate_frame = tk.Frame(self.candidates_frame, bg='white', pady=5)
                candidate_frame.pack(fill='x', padx=10, pady=2)
                
                radio = tk.Radiobutton(
                    candidate_frame,
                    text=f"{candidate[2]} ({candidate[3]}) - {candidate[4] or 'No Symbol'}",
                    variable=self.candidate_var,
                    value=idx + 1,
                    font=('Arial', 11),
                    bg='white',
                    anchor='w'
                )
                radio.pack(fill='x', side='left')
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load candidates: {str(e)}")
    
    def submit_vote(self):
        if not self.current_voter:
            messagebox.showerror("Error", "Please verify voter first")
            return
        
        if self.candidate_var.get() == 0:
            messagebox.showerror("Error", "Please select a candidate")
            return
        
        if not self.current_election:
            messagebox.showerror("Error", "Please select an election")
            return
        
        try:
            voter_district = self.current_voter[4]
            election_text = self.election_var.get()
            election_district = election_text.split(' - ')[1].split(' (')[0]
            
            if voter_district != election_district:
                messagebox.showerror("Error", f"Voter district ({voter_district}) doesn't match election district ({election_district})")
                return
            
            if self.current_voter[8] == 1:
                messagebox.showerror("Error", "This voter has already voted!")
                return
            
            elections = self.db.get_elections()
            contract_address = None
            
            for election in elections:
                if election[0] == self.current_election:
                    contract_address = election[5]
                    break
            
            if not contract_address:
                messagebox.showerror("Error", "No blockchain contract found for this election")
                return
            
            self.blockchain.load_contract(contract_address)
            
            voter_address = self.current_voter[6]
            voter_private_key = self.current_voter[7]
            candidate_id = self.candidate_var.get()
            
            if not self.blockchain.is_voter_registered(self.current_election, voter_address):
                self.blockchain.register_voter_on_blockchain(self.current_election, voter_address)
            
            tx_hash = self.blockchain.cast_vote(self.current_election, candidate_id, voter_private_key)
            
            self.db.record_vote(self.current_voter[1], self.current_election, tx_hash)
            
            messagebox.showinfo(
                "Success",
                f"Vote cast successfully!\n\nTransaction Hash:\n{tx_hash}\n\nVote recorded on blockchain!"
            )
            
            self.current_voter = None
            self.voter_id_entry.delete(0, tk.END)
            self.voter_info_label.config(text="No voter verified", fg='#95a5a6')
            self.candidate_var.set(0)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to submit vote: {str(e)}")
