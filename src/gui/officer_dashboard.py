"""import tkinter as tk
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
            messagebox.showerror("Error", f"Failed to submit vote: {str(e)}")"""

import io, os, hashlib
import customtkinter as ctk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk

# Optional QR (show message if not installed)
try:
    import qrcode
    QR_AVAILABLE = True
except Exception:
    QR_AVAILABLE = False

from src.utils.database import Database
from src.utils.blockchain import BlockchainManager
# Adjust import if your biometric module lives elsewhere:

from src.utils.biometric_secugen import SecuGenScanner
import base64
class OfficerDashboard(ctk.CTkFrame):
    """
    Officer dashboard:
    - Tab 1: Voter Verification & Secure Voting (CTkToplevel)
    - Tab 2: Live Results with turnout progress + refresh + chain status
    """
    def __init__(self, root, username_or_role, on_logout):
        super().__init__(root)
        self.root = root
        self.on_logout = on_logout

        self.db = Database()
        self.bc = BlockchainManager()
        self.sg = SecuGenScanner()

        # Resolve district from role or username
        self.officer_district = self.db.get_officer_district_from_role(username_or_role) or "Unknown"

        # Theme/window
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        self.root.title(f"Mata Raksha — Officer ({self.officer_district})")
        self.root.geometry("980x640")

        # Top bar
        top = ctk.CTkFrame(self.root, fg_color="#1a252f", height=50)
        top.pack(fill="x", side="top")
        ctk.CTkLabel(top, text=f"🛡️ Officer — {self.officer_district}",
                     font=("Arial", 18, "bold"), text_color="#ecf0f1").pack(side="left", padx=20, pady=10)

        # Chain status dot
        self.chain_dot = ctk.CTkLabel(top, text="●", font=("Arial", 18))
        self.chain_dot.pack(side="right", padx=(4, 12))
        self.chain_label = ctk.CTkLabel(top, text="Chain: checking...", text_color="#bdc3c7")
        self.chain_label.pack(side="right")

        # Logout
        ctk.CTkButton(top, text="Logout", fg_color="#e74c3c", hover_color="#c0392b",
                      width=90, height=30, corner_radius=15,
                      command=self.logout).pack(side="right", padx=12)

        # Tabs
        self.tabview = ctk.CTkTabview(self.root)
        self.tabview.pack(fill="both", expand=True, padx=16, pady=16)
        self.tab_voting = self.tabview.add("Voting & Verification")
        self.tab_results = self.tabview.add("Results / Status")

        # Build tabs
        self._build_voting_tab()
        self._build_results_tab()

        # Timers
        self._tick_chain_status()
        self._auto_refresh_results()

    # ===================== TAB 1: Voting & Verification ======================

    def _build_voting_tab(self):
        frame = ctk.CTkFrame(self.tab_voting)
        frame.pack(fill="both", expand=True, padx=16, pady=16)

        ctk.CTkLabel(frame, text="Voter Verification & Secure Voting",
                     font=("Arial", 17, "bold")).pack(pady=(8,12))
        district = self.officer_district
        print(district)
        if isinstance(district, list):
            district = district[0] if district else None
            print(district)
        # Active election (auto for officer's district)
        self.active_election = self.db.get_active_election_by_district(district)
        if not self.active_election:
            ctk.CTkLabel(frame, text="No ACTIVE election for your district.",
                         text_color="#c0392b", font=("Arial", 14, "bold")).pack()
            return

        eid, ename, sdate, edate, status = self.active_election
        ctk.CTkLabel(frame, text=f"Active: {ename}  ({self.officer_district})\n{sdate} → {edate}",
                     font=("Arial", 12)).pack()

        # Aadhaar / Voter ID
        pad = ctk.CTkFrame(frame)
        pad.pack(pady=12)
        self.voter_key = ctk.CTkEntry(pad, placeholder_text="Enter Aadhaar or Voter ID", width=320)
        self.voter_key.grid(row=0, column=0, padx=6)
        ctk.CTkButton(pad, text="Verify Voter", fg_color="#27ae60",
                      command=self._verify_voter).grid(row=0, column=1, padx=6)

        # Info labels
        self.info_voter = ctk.CTkLabel(frame, text="", font=("Arial", 12))
        self.info_voter.pack(pady=(6,2))
        self.info_status = ctk.CTkLabel(frame, text="", font=("Arial", 13, "bold"))
        self.info_status.pack()

        # Note
        ctk.CTkLabel(frame, text="(After verification, a separate secure window opens for the voter to choose a candidate.)",
                     text_color="#6b6b6b", font=("Arial", 11)).pack(pady=8)

    def _verify_voter(self):
        key = (self.voter_key.get() or "").strip()
        if not key:
            messagebox.showerror("Missing", "Enter Aadhaar or Voter ID.")
            return

        voter = self.db.get_voter_by_aadhaar_or_id(key)
        if not voter:
            messagebox.showerror("Not found", "No voter found for the input.")
            return

        # shape per helper: (id, voter_id, name, dob, district, aadhaar, fingerprint_hash, addr, pkey, has_voted)
        _id, voter_id, name, dob, aadhaar, district,  fp_hash, addr, pkey, _, _, = voter

        if district != self.officer_district:
            messagebox.showerror("District mismatch",
                                 f"Voter belongs to {district}, but you are assigned to {self.officer_district}.")
            return
        eid = self.active_election[0]
        has_voted= self.bc.has_voted(eid,addr )
        if has_voted:
            self.info_voter.configure(text=f"{name} ({voter_id}) — {district}")
            self.info_status.configure(text="⚠️ Already voted.", text_color="#e67e22")
            return

        # Fingerprint capture
        try:
            
            err, self.img_bytes = self.sg.capture_fingerprint()

            err, self.template = self.sg.create_template(self.img_bytes)

            tpl_stored=base64.b64decode(fp_hash)
            
        except Exception as e:
            messagebox.showerror("Fingerprint Error", str(e))
            return

        if not self.template:
            return
        matched = self.sg.match_templates(self.template, tpl_stored)
        self.info_voter.configure(text=f"{name} ({voter_id}) — {district}")

        if not matched :
            self.info_status.configure(text="❌ Verification Failed — fingerprint mismatch.", text_color="#e74c3c")
            return

        self.info_status.configure(text="✅ Verified. Opening secure voting window...", text_color="#27ae60")
        self._open_secure_voting_window(voter)

    def _open_secure_voting_window(self, voter_row):
        """
        Separate, voter-only selection screen.
        """
        eid = self.active_election[0]
        candidates = self.db.get_candidates_for_election_district(eid, self.officer_district)

        if not candidates:
            messagebox.showerror("No candidates", "No candidates configured for this election.")
            return

        win = ctk.CTkToplevel(self.root)
        win.title("Secure Voting")
        win.geometry("460x560")
        win.grab_set()  # lock focus here

        ctk.CTkLabel(win, text="Cast Your Vote", font=("Arial", 16, "bold")).pack(pady=(16,8))
        ctk.CTkLabel(win, text=f"{self.active_election[1]} — {self.officer_district}",
                     font=("Arial", 12)).pack()

        # Candidate combo
        # Header Frame
        header_frame = ctk.CTkFrame(win)
        header_frame.pack(pady=(10, 5), fill="x")

        ctk.CTkLabel(header_frame, text="Name", width=200, anchor="w").pack(side="left", padx=(10, 5))
        ctk.CTkLabel(header_frame, text="Party", width=150, anchor="w").pack(side="left", padx=5)
        ctk.CTkLabel(header_frame, text="Symbol", width=100, anchor="w").pack(side="left", padx=5)

        # Variable to store selected candidate
        self.selected_candidate = ctk.StringVar(value="")
        eid = self.active_election[0]
        print(self.bc.get_candidate_count(eid))
        # Candidate Rows with Radio Buttons
        c_id=0
        for c in candidates:
            c_id+=1
            # c[1] = name, c[2] = party, c[3] = symbol
            row = ctk.CTkFrame(win)
            row.pack(pady=3, fill="x")

            radio = ctk.CTkRadioButton(
                row,
                text="",                   # no text here
                variable=self.selected_candidate,
                value=str(c_id)            # candidate_id
            )
            radio.pack(side="left", padx=5)

            ctk.CTkLabel(row, text=c[1], width=200, anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(row, text=c[2], width=150, anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(row, text=c[3] or "", width=100, anchor="w").pack(side="left", padx=5)


        
        """nice = [f"{c[1]} — {c[2]} ({c[3] or ''})" for c in candidates]
        self.sec_combo = ctk.CTkComboBox(win, values=nice, width=360)
        self.sec_combo.pack(pady=(18,8))"""

        # Cast button
        ctk.CTkButton(win, text="Cast Vote", fg_color="#27ae60",
                      command=lambda: self._cast_vote(voter_row, candidates, win)).pack(pady=10)

        # QR preview
        self.qr_label = ctk.CTkLabel(win, text="")
        self.qr_label.pack(pady=8)

        # Info
        self.sec_status = ctk.CTkLabel(win, text="", font=("Arial", 12))
        self.sec_status.pack(pady=(6,12))

        # Download QR
        self.save_qr_btn = ctk.CTkButton(win, text="Download QR", state="disabled",
                                         command=lambda: self._save_qr_png(win))
        self.save_qr_btn.pack()

    def _cast_vote(self, voter_row, candidates, win):
        if not self.bc.is_connected():
            messagebox.showerror("Blockchain", "Not connected to Ganache/chain.")
            return
        sel = int(self.selected_candidate.get())
        print(sel)
        if not sel:
            messagebox.showerror("Select", "Select a candidate.")
            return

        # voter tuple (id, voter_id, name, dob, district, aadhaar, fp_hash, addr, pkey, has_voted)
        _id, voter_id, name, dob, aadhaar, district,  fp_hash, addr, pkey, _, _, = voter_row
        eid = self.active_election[0]

        try:
            tx_hash = self.bc.cast_vote(eid, sel, pkey)  # must return a hex string
        except Exception as e:
            messagebox.showerror("Blockchain Error", f"Failed to cast: {e}")
            return

        try:
            self.db.record_vote(voter_id, eid, sel, tx_hash)
        except Exception as e:
            messagebox.showwarning("DB Warning", f"Vote recorded on chain, but DB insert had an issue:\n{e}")

        self.sec_status.configure(text=f"✅ Vote cast! Tx: {tx_hash[:16]}...", text_color="#27ae60")

        # QR
        if not QR_AVAILABLE:
            self.qr_label.configure(text="(Install 'qrcode[pil]' to show QR)")
            return

        img = qrcode.make(f"MR-VOTE|e:{eid}|v:{voter_id}|tx:{tx_hash}")
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        pil_img = Image.open(buf)
        pil_img = pil_img.resize((210, 210))
        tk_img = ImageTk.PhotoImage(pil_img)
        self.qr_label.configure(image=tk_img, text="")
        self.qr_label.image = tk_img
        win._qr_png_bytes = buf.getvalue()
        self.save_qr_btn.configure(state="normal")

    def _save_qr_png(self, win):
        from tkinter import filedialog
        path = filedialog.asksaveasfilename(
            title="Save Vote QR",
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png")]
        )
        if not path:
            return
        if hasattr(win, "_qr_png_bytes"):
            with open(path, "wb") as f:
                f.write(win._qr_png_bytes)
            messagebox.showinfo("Saved", f"QR saved to {path}")

    # ===================== TAB 2: Results / Status ======================

    def _build_results_tab(self):
        frame = ctk.CTkFrame(self.tab_results)
        frame.pack(fill="both", expand=True, padx=16, pady=16)

        ctk.CTkLabel(frame, text="Live Status",
                     font=("Arial", 17, "bold")).pack(pady=(8,12))

        # Election selector (active/pending/completed in your district)
        self.res_election_combo = ctk.CTkComboBox(frame, width=360,
                                                  values=self._list_elections_in_district())
        self.res_election_combo.pack(pady=(6,8))
        ctk.CTkButton(frame, text="Refresh", command=self._refresh_results).pack(pady=6)

        # Chain status inline
        self.res_chain = ctk.CTkLabel(frame, text="")
        self.res_chain.pack()

        # Turnout bar
        bar_frame = ctk.CTkFrame(frame)
        bar_frame.pack(pady=(10,6), fill="x", padx=8)
        self.turnout_lbl = ctk.CTkLabel(bar_frame, text="Turnout: 0% (0 / 0)")
        self.turnout_lbl.pack(anchor="w", padx=8, pady=(6,2))
        self.turnout_bar = ctk.CTkProgressBar(bar_frame)
        self.turnout_bar.set(0.0)
        self.turnout_bar.pack(fill="x", padx=8, pady=(2,8))

        """# Results table
        self.res_table = ttk.Treeview(frame, columns=("Candidate", "Party", "Symbol", "Votes"),
                                      show="headings", height=10)
        for i, col in enumerate(("Candidate", "Party", "Symbol", "Votes")):
            self.res_table.heading(col, text=col)
            self.res_table.column(col, anchor="center", width=180 if i < 3 else 100)
        self.res_table.pack(fill="both", expand=True, pady=(8,6), padx=8)"""

        self._refresh_results()

    def _list_elections_in_district(self):
        rows = self.db.get_elections()
        vals = []
        for e in rows:
            # e: (id, election_name, district, start, end, contract_address, status, created_at)
            if e[2] == self.officer_district:
                vals.append(f"{e[1]} (ID:{e[0]}) [{e[6]}]")
        return vals or ["<No elections>"]

    def _selected_election_id(self):
        txt = (self.res_election_combo.get() or "")
        if "ID:" in txt:
            try:
                return int(txt.split("ID:")[1].split(")")[0])
            except Exception:
                return None
        return None

    def _refresh_results(self):
        eid = self._selected_election_id()
        if not eid:
            # pick active if possible
            if self.active_election:
                eid = self.active_election[0]
            else:
                return

        # Turnout
        total = self.db.count_voters_in_district(self.officer_district)
        voted = self.db.count_voted_in_election_district(eid, self.officer_district)
        pct = (voted / total) if total else 0.0
        self.turnout_lbl.configure(text=f"Turnout: {pct*100:.1f}%  ({voted} / {total})")
        self.turnout_bar.set(min(max(pct, 0.0), 1.0))

        # Chain ping
        if self.bc.is_connected():
            self.res_chain.configure(text="Chain: Connected", text_color="#27ae60")
        else:
            self.res_chain.configure(text="Chain: Disconnected", text_color="#e74c3c")

        # Table
        """for i in self.res_table.get_children():
            self.res_table.delete(i)

        rows = self.db.results_summary_by_election(eid)
        # rows: [(name, party, symbol, votes)]
        top_votes = rows[0][3] if rows else 0
        for r in rows:
            iid = self.res_table.insert("", "end", values=r)
            if r[3] == top_votes and top_votes > 0:
                # bold/green for winner
                self.res_table.item(iid, tags=("winner",))
        self.res_table.tag_configure("winner", background="#e8f8f5")"""

    # ===================== Timers / Status ======================

    def _tick_chain_status(self):
        if self.bc.is_connected():
            self.chain_dot.configure(text_color="#27ae60")
            self.chain_label.configure(text="Chain: Connected", text_color="#27ae60")
        else:
            self.chain_dot.configure(text_color="#e74c3c")
            self.chain_label.configure(text="Chain: Disconnected", text_color="#e74c3c")
        self.root.after(2000*60*100, self._tick_chain_status)

    def _auto_refresh_results(self):
        # refresh silently if results tab selected
        if self.tabview.get() == "Results / Status":
            self._refresh_results()
        self.root.after(1000*60, self._auto_refresh_results)

    def logout(self):
        self.destroy()
        self.on_logout()

