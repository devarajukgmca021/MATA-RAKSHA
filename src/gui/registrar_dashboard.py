"""import tkinter as tk
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


# src/gui/registrar_dashboard.py

import os
from datetime import datetime, date
import io

import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk

from PIL import Image, ImageDraw, ImageFont

# Project utils
from src.utils.database import Database
from src.utils.biometric_secugen import SecuGenScanner

try:
    from src.utils.blockchain import BlockchainManager
except Exception:
    BlockchainManager = None


KARNATAKA_DISTRICTS = [
    "Bagalkot", "Ballari", "Belagavi", "Bengaluru Rural", "Bengaluru Urban",
    "Bidar", "Chamarajanagar", "Chikkaballapur", "Chikkamagaluru", "Chitradurga",
    "Dakshina Kannada", "Davanagere", "Dharwad", "Gadag", "Hassan",
    "Haveri", "Kalaburagi", "Kodagu", "Kolar", "Koppal",
    "Mandya", "Mysuru", "Raichur", "Ramanagara", "Shivamogga",
    "Tumakuru", "Udupi", "Uttara Kannada", "Vijayapura", "Yadgir"
]


# ----------------------------- Helpers (local) -----------------------------

def _calc_age_yrs(dob_str: str) -> int:
    dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
    t = date.today()
    return t.year - dob.year - ((t.month, t.day) < (dob.month, dob.day))


def _ensure_dirs(path: str):
    os.makedirs(path, exist_ok=True)




def _generate_blockchain_creds() -> tuple[str, str]:
    
    #Prefer your project's BlockchainManager account creation if available.
    #Else, generate demo address/private key (NOT for production).
    # If you wrote an API like manager.create_account() returning (address, private_key)
    if BlockchainManager:
        try:
            mgr = BlockchainManager()
            # If your manager has an account creation helper, use it:
            if hasattr(mgr, "create_account"):
                addr, pk = mgr.create_account()
                if addr and pk:
                    return addr, pk
            # Fallback: use its default account if connected
            if hasattr(mgr, "w3") and mgr.w3 and mgr.w3.is_connected():
                acct = mgr.w3.eth.account.create()
                return acct.address, acct._private_key.hex()
        except Exception:
            pass

    # Minimal fallback (for dev only)
    import os, hashlib
    fake_priv = hashlib.sha256(os.urandom(32)).hexdigest()
    fake_addr = "0x" + hashlib.sha256(fake_priv.encode()).hexdigest()[:40]
    return fake_addr, fake_priv


    import qrcode
    from PIL import Image, ImageDraw, ImageFont

def _make_voter_id_png(out_dir: str, voter_id: str, name: str, aadhaar: str, district: str, dob: str) -> str:
    #Self-contained PNG voter ID (simple, printable) with QR Code.
    
    _ensure_dirs(out_dir)
    W, H = 720, 420
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)

    def font(sz):
        try:
            return ImageFont.load_default()
        except Exception:
            return ImageFont.load_default()

    # Header
    d.rectangle([(0, 0), (W, 72)], fill="#1a7f64")
    d.text((20, 22), "Mata Raksha – Voter ID", font=font(24), fill="white")

    # Body text
    y0, lh = 110, 38
    d.text((40, y0 + 0 * lh), f"Voter ID  : {voter_id}", font=font(20), fill="#111")
    d.text((40, y0 + 1 * lh), f"Name      : {name}", font=font(20), fill="#111")
    d.text((40, y0 + 2 * lh), f"Aadhaar   : XXXX-XXXX-{aadhaar[-4:]}", font=font(20), fill="#111")
    d.text((40, y0 + 3 * lh), f"District  : {district}", font=font(20), fill="#111")
    d.text((40, y0 + 4 * lh), f"DOB       : {dob}", font=font(20), fill="#111")
    d.text((40, y0 + 5 * lh), f"Issued On : {datetime.now().strftime('%Y-%m-%d')}", font=font(20), fill="#111")

    d.text((20, H - 32), "Note: Demo card for project use only.", font=font(16), fill="#666")

    # --- QR Code ---
    qr_data = f"VoterID:{voter_id}\nName:{name}\nAadhaar:{aadhaar[-4:]}\nDistrict:{district}\nDOB:{dob}"
    qr_img = qrcode.make(qr_data)
    qr_img = qr_img.resize((120, 120))
    img.paste(qr_img, (W - 150, H - 160))  # bottom-right corner

    out_path = os.path.join(out_dir, f"{voter_id}.png")
    img.save(out_path, "PNG")
    return out_path


def _compose_id_cards_pdf_for_district(rows, out_pdf_path: str):
    
    #Build a multi-page PDF: one voter ID card per page (with QR code).
    
    _ensure_dirs(os.path.dirname(out_pdf_path) or ".")
    pages = []

    for voter_id, name, dob, district, aadhaar, registered_at in rows:
        W, H = 720, 420
        img = Image.new("RGB", (W, H), "white")
        d = ImageDraw.Draw(img)

        def font(sz):
            return ImageFont.load_default()

        d.rectangle([(0, 0), (W, 72)], fill="#1a7f64")
        d.text((20, 22), "Mata Raksha – Voter ID", font=font(24), fill="white")

        y0, lh = 110, 38
        d.text((40, y0 + 0 * lh), f"Voter ID  : {voter_id}", font=font(20), fill="#111")
        d.text((40, y0 + 1 * lh), f"Name      : {name}", font=font(20), fill="#111")
        d.text((40, y0 + 2 * lh), f"Aadhaar   : XXXX-XXXX-{aadhaar[-4:]}", font=font(20), fill="#111")
        d.text((40, y0 + 3 * lh), f"District  : {district}", font=font(20), fill="#111")
        d.text((40, y0 + 4 * lh), f"DOB       : {dob}", font=font(20), fill="#111")
        d.text((40, y0 + 5 * lh), f"Issued On : {datetime.now().strftime('%Y-%m-%d')}", font=font(20), fill="#111")

        # QR Code
        qr_data = f"VoterID:{voter_id}\nName:{name}\nAadhaar:{aadhaar[-4:]}\nDistrict:{district}\nDOB:{dob}"
        qr_img = qrcode.make(qr_data)
        qr_img = qr_img.resize((120, 120))
        img.paste(qr_img, (W - 150, H - 160))

        d.text((20, H - 32), "Note: Demo card for project use only.", font=font(16), fill="#666")

        pages.append(img.convert("RGB"))

    if not pages:
        raise ValueError("No voters to export.")
    pages[0].save(out_pdf_path, save_all=True, append_images=pages[1:])


# ----------------------------- UI Class -----------------------------

class RegistrarDashboard(ctk.CTkFrame):
    def __init__(self, root, username, on_logout):
        super().__init__(root)
        self.root = root
        self.username = username
        self.on_logout = on_logout
        self.db = Database()

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.root.title("Mata Raksha – Registrar")
        self.root.geometry("1000x680")

        self.pack(fill="both", expand=True)

        # Top bar
        top = ctk.CTkFrame(self, fg_color="#1a252f", height=52)
        top.pack(fill="x", side="top")
        ctk.CTkLabel(top, text=f"Registrar: {self.username}",
                     font=("Arial", 16, "bold"), text_color="#ecf0f1").pack(side="left", padx=16, pady=10)
        ctk.CTkButton(top, text="Logout", fg_color="#e74c3c", hover_color="#c0392b",
                      width=90, command=self.logout).pack(side="right", padx=16, pady=10)

        # Tabs
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True, padx=16, pady=16)
        self.tab_register = self.tabs.add("Register Voter")
        self.tab_manage = self.tabs.add("Manage Voters")
        self.tab_downloads = self.tabs.add("Reports & Downloads")

        self._build_register_tab()
        self._build_manage_tab()
        self._build_downloads_tab()

        # Poll for tab changes if you want to auto-refresh views
        self._active_tab = None
        self.after(700, self._check_tab_change)
        self.sg = SecuGenScanner()     # Create a biometric interface for this window

    # ------------------------ Tab 1: Register ------------------------

    def _build_register_tab(self):
        form = ctk.CTkFrame(self.tab_register)
        form.pack(padx=18, pady=18, fill="x")

        self.r_name = ctk.CTkEntry(form, placeholder_text="Full Name", width=320)
        self.r_name.grid(row=0, column=0, padx=8, pady=8, sticky="w")

        self.r_dob = ctk.CTkEntry(form, placeholder_text="DOB (YYYY-MM-DD)", width=200)
        self.r_dob.grid(row=0, column=1, padx=8, pady=8, sticky="w")

        self.r_aadhaar = ctk.CTkEntry(form, placeholder_text="Aadhaar (12 digits)", width=220)
        self.r_aadhaar.grid(row=1, column=0, padx=8, pady=8, sticky="w")

        self.r_district = ctk.CTkComboBox(form, values=KARNATAKA_DISTRICTS, width=240)
        self.r_district.set(KARNATAKA_DISTRICTS[0])
        self.r_district.grid(row=1, column=1, padx=8, pady=8, sticky="w")

        # Fingerprint controls
        fp_box = ctk.CTkFrame(self.tab_register)
        fp_box.pack(padx=18, pady=(0, 8), fill="x")
        ctk.CTkLabel(fp_box, text="Fingerprint", font=("Arial", 12, "bold")).pack(anchor="w", padx=6, pady=(10, 6))

        inner = ctk.CTkFrame(fp_box)
        inner.pack(fill="x", padx=6, pady=6)

        self.r_fp_bytes = None
        ctk.CTkButton(inner, text="Capture / Choose Fingerprint", command=self._r_capture_fp).pack(side="left", padx=6)
        ctk.CTkButton(inner, text="Test Fingerprint", fg_color="#2980b9", command=self._r_test_fp).pack(side="left", padx=6)

        # Register button
        ctk.CTkButton(self.tab_register, text="Register Voter", fg_color="#27ae60",
                      width=200, command=self._register_voter).pack(pady=12)

    def _r_capture_fp(self):
        raw = self.sg.capture_fingerprint()
        if not raw:
            messagebox.showerror("Error", "Fingerprint capture failed")
            return

    def _r_test_fp(self):
        if not self.raw:
            messagebox.showerror("Fingerprint", "Capture or load a fingerprint first.")
            return
        if self.sg.get_quality(self.raw) < 40:
            messagebox.showerror("Error", "Poor fingerprint quality. Try again.")
            return

    def _register_voter(self):
        name = (self.r_name.get() or "").strip()
        dob = (self.r_dob.get() or "").strip()
        aadhaar = (self.r_aadhaar.get() or "").strip()
        district = self.r_district.get().strip()

        template = self.sg.create_template(self.raw)
        fp_hash = self.sg.template_hash(template)

        if not all([name, dob, aadhaar, district, template]):
            messagebox.showerror("Error", "All fields and fingerprint are required.")
            return

        if not (aadhaar.isdigit() and len(aadhaar) == 12):
            messagebox.showerror("Error", "Aadhaar must be exactly 12 digits.")
            return

        try:
            age = _calc_age_yrs(dob)
        except Exception:
            messagebox.showerror("Error", "DOB must be in YYYY-MM-DD format.")
            return
        if age < 18:
            messagebox.showerror("Error", "Voter must be at least 18 years old.")
            return

        # Blockchain credentials
        address, private_key = _generate_blockchain_creds()

        # Store in DB (prefers register_voter_full with Aadhaar support)
        try:
            if hasattr(self.db, "register_voter"):
                voter_id = self.db.register_voter(
                    name=name, dob=dob, district=district, aadhaar=aadhaar,
                    fp_template=template, fingerprint_hash=fp_hash, blockchain_address=address, private_key=private_key
                )
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
            return
        except Exception as e:
            messagebox.showerror("Error", f"Failed to register voter: {e}")
            return

        # Create PNG ID and show a simple popup
        out_png = _make_voter_id_png("exports/idcards", voter_id, name, aadhaar, district, dob)
        messagebox.showinfo(
            "Voter Registered",
            f"Voter ID: {voter_id}\n\nID card saved at:\n{os.path.abspath(out_png)}"
        )

        # Clear form
        for w in (self.r_name, self.r_dob, self.r_aadhaar):
            w.delete(0, "end")
        self.r_district.set(KARNATAKA_DISTRICTS[0])
        self.r_fp_bytes = None

    # ------------------------ Tab 2: Manage ------------------------

    def _build_manage_tab(self):
        bar = ctk.CTkFrame(self.tab_manage)
        bar.pack(fill="x", padx=16, pady=10)

        self.m_key = ctk.CTkEntry(bar, placeholder_text="Enter Aadhaar or Voter ID", width=300)
        self.m_key.pack(side="left", padx=6)
        ctk.CTkButton(bar, text="Fetch", command=self._m_fetch).pack(side="left", padx=6)
        ctk.CTkButton(bar, text="Clear", command=self._m_clear).pack(side="left", padx=6)

        form = ctk.CTkFrame(self.tab_manage)
        form.pack(fill="x", padx=16, pady=10)

        self.m_voter_id = ctk.CTkEntry(form, placeholder_text="Voter ID (read-only)", width=180)
        self.m_voter_id.grid(row=0, column=0, padx=6, pady=6)
        self.m_name = ctk.CTkEntry(form, placeholder_text="Name", width=220)
        self.m_name.grid(row=0, column=1, padx=6, pady=6)
        self.m_dob = ctk.CTkEntry(form, placeholder_text="DOB (YYYY-MM-DD)", width=180)
        self.m_dob.grid(row=0, column=2, padx=6, pady=6)

        self.m_aadhaar = ctk.CTkEntry(form, placeholder_text="Aadhaar (12 digits)", width=220)
        self.m_aadhaar.grid(row=1, column=0, padx=6, pady=6)
        self.m_district = ctk.CTkComboBox(form, values=KARNATAKA_DISTRICTS, width=220)
        self.m_district.grid(row=1, column=1, padx=6, pady=6)

        # Fingerprint recapture
        fp = ctk.CTkFrame(self.tab_manage)
        fp.pack(fill="x", padx=16, pady=6)
        self.m_fp_bytes = None
        ctk.CTkButton(fp, text="Load New Fingerprint", command=self._m_load_fp).pack(side="left", padx=6)
        ctk.CTkButton(fp, text="Test", fg_color="#2980b9", command=self._m_test_fp).pack(side="left", padx=6)

        actions = ctk.CTkFrame(self.tab_manage)
        actions.pack(fill="x", padx=16, pady=8)
        ctk.CTkButton(actions, text="Update", fg_color="#2980b9", command=self._m_update).pack(side="left", padx=6)
        ctk.CTkButton(actions, text="Delete", fg_color="#e67e22", command=self._m_delete).pack(side="left", padx=6)

        # Optional quick view table
        self.m_table = ttk.Treeview(
            self.tab_manage,
            columns=("VoterID", "Name", "Aadhaar", "District", "DOB", "HasVoted"),
            show="headings",
            height=8
        )
        for c in ("VoterID", "Name", "Aadhaar", "District", "DOB", "HasVoted"):
            self.m_table.heading(c, text=c)
            self.m_table.column(c, anchor="center", width=150)
        self.m_table.pack(fill="both", expand=True, padx=16, pady=(6, 16))

    def _m_fetch(self):
        key = (self.m_key.get()).strip()
        if not key:
            messagebox.showerror("Error", "Enter Aadhaar or Voter ID.")
            return

        row = None
        if hasattr(self.db, "get_voter_by_aadhaar_or_id"):
            row = self.db.get_voter_by_aadhaar_or_id(key)
        else:
            messagebox.showerror("Not Supported", "Database helper get_voter_by_aadhaar_or_id is missing.")
            return

        if not row:
            messagebox.showerror("Not found", "No voter matches given Aadhaar/Voter ID.")
            return

        # row: id, voter_id, name, dob, district, aadhaar, fingerprint_hash, blockchain_address,
        #      private_key, photo_path, registered_at, has_voted,
        _, voter_id, name, dob, aadhaar, dist, _, _, _, _, _, _ = row

        self.m_voter_id.delete(0, "end"); self.m_voter_id.insert(0, voter_id)
        self.m_name.delete(0, "end");     self.m_name.insert(0, name)
        self.m_dob.delete(0, "end");      self.m_dob.insert(0, dob)
        self.m_aadhaar.delete(0, "end");  self.m_aadhaar.insert(0, aadhaar or "")
        self.m_district.set(dist)

        # Fill table snapshot
        for i in self.m_table.get_children():
            self.m_table.delete(i)
        self.m_table.insert("", "end", values=(voter_id, name, aadhaar, dist, dob))

    def _m_load_fp(self):
        self.m_raw = self.sg.capture_image()
        if self.m_raw:
            messagebox.showinfo("Fingerprint", "Loaded new fingerprint.")
        else:
            messagebox.showerror("Error", "Fingerprint capture failed")
            return

    def _m_test_fp(self):
        if not self.m_raw:
            messagebox.showerror("Fingerprint", "Load a fingerprint first.")
            return
        if self.sg.get_quality(self.m_raw) < 40:
            messagebox.showerror("Error", "Poor fingerprint quality. Try again.")
            return

    def _m_update(self):
        voter_id = (self.m_voter_id.get()).strip()
        name = (self.m_name.get()).strip()
        dob = (self.m_dob.get()).strip()
        aadhaar = (self.m_aadhaar.get()).strip()
        district = self.m_district.get().strip()

        m_template = self.sg.create_template(self.m_raw)
        m_fp_hash = self.sg.template_hash(m_template)
        
        if not all([voter_id, name, dob, aadhaar, district,m_template]):
            messagebox.showerror("Error", "All fields are required.")
            return
        if not (aadhaar.isdigit() and len(aadhaar) == 12):
            messagebox.showerror("Error", "Aadhaar must be 12 digits.")
            return

        # Age check optional on update too
        try:
            if _calc_age_yrs(dob) < 18:
                messagebox.showerror("Error", "Voter must be at least 18 years old.")
                return
        except Exception:
            messagebox.showerror("Error", "DOB must be YYYY-MM-DD.")
            return

        try:
            if hasattr(self.db, "update_voter"):
                self.db.update_voter(voter_id, name, dob, aadhaar, district, m_template, m_fp_hash)
            else:
                messagebox.showerror("Not Supported", "Database helper update_voter_full is missing.")
                return
        except ValueError as ve:
            messagebox.showerror("Error", str(ve)); return
        except Exception as e:
            messagebox.showerror("Error", f"DB error: {e}"); return

        messagebox.showinfo("Updated", "Voter updated successfully.")
        self.m_raw = None
        self._m_fetch()

    def _m_delete(self):
        voter_id = (self.m_voter_id.get()).strip()
        if not voter_id:
            messagebox.showerror("Error", "Fetch a voter first.")
            return
        if not messagebox.askyesno("Confirm", f"Delete voter {voter_id}? This cannot be undone."):
            return
        try:
            self.db.delete_voter(voter_id)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete voter:\n{e}")
            return
        messagebox.showinfo("Deleted", f"Voter {voter_id} removed.")
        self._m_clear()
        for i in self.m_table.get_children():
            self.m_table.delete(i)

    def _m_clear(self):
        for w in (self.m_key, self.m_voter_id, self.m_name, self.m_dob, self.m_aadhaar):
            w.delete(0, "end")
        self.m_district.set("")
        self.m_raw = None

    # -------------------- Tab 3: Downloads --------------------

    def _build_downloads_tab(self):
        wrap = ctk.CTkFrame(self.tab_downloads)
        wrap.pack(fill="x", padx=16, pady=16)

        ctk.CTkLabel(wrap, text="District-wise PDF (multi-page Voter IDs)", font=("Arial", 14, "bold")).grid(row=0, column=0, sticky="w", padx=6, pady=6)
        self.dl_district = ctk.CTkComboBox(wrap, values=KARNATAKA_DISTRICTS, width=260)
        self.dl_district.grid(row=1, column=0, padx=6, pady=6, sticky="w")
        ctk.CTkButton(wrap, text="Export PDF", command=self._export_pdf).grid(row=1, column=1, padx=8, pady=6)

        sep = ctk.CTkFrame(self.tab_downloads, height=2)
        sep.pack(fill="x", padx=16, pady=10)

        indiv = ctk.CTkFrame(self.tab_downloads)
        indiv.pack(fill="x", padx=16, pady=10)
        ctk.CTkLabel(indiv, text="Individual Voter ID (PNG)", font=("Arial", 14, "bold")).grid(row=0, column=0, sticky="w", padx=6, pady=6)

        self.dl_key = ctk.CTkEntry(indiv, placeholder_text="Enter Aadhaar or Voter ID", width=300)
        self.dl_key.grid(row=1, column=0, padx=6, pady=6, sticky="w")

        ctk.CTkButton(indiv, text="Generate / Save PNG", command=self._export_single_png).grid(row=1, column=1, padx=8, pady=6)

    def _export_pdf(self):
        dist = self.dl_district.get().strip()
        if not dist:
            messagebox.showerror("Error", "Select a district.")
            return

        rows = self.db.get_voters_by_district(dist)
        if not rows:
            messagebox.showinfo("No Data", "No voters found for this district.")
            return

        save_path = filedialog.asksaveasfilename(
            title="Save PDF",
            defaultextension=".pdf",
            filetypes=[("PDF", "*.pdf")],
            initialfile=f"voter_id_cards_{dist}.pdf"
        )
        if not save_path:
            return

        try:
            _compose_id_cards_pdf_for_district(rows, save_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export PDF:\n{e}")
            return

        messagebox.showinfo("Exported", f"Saved:\n{save_path}")

    def _export_single_png(self):
        key = (self.dl_key.get() or "").strip()
        if not key:
            messagebox.showerror("Error", "Enter Aadhaar or Voter ID.")
            return

        row = self.db.get_voter_by_aadhaar_or_id(key)
        if not row:
            messagebox.showerror("Not Found", "No voter found.")
            return

        # row schema per Database get_voter_by_aadhaar_or_id()
        _, voter_id, name, dob, aadhaar, district, _, _, _, _, _, _ = row
        out_png = _make_voter_id_png("exports/idcards", voter_id, name, aadhaar or "", district, dob)

        # Offer Save As
        dest = filedialog.asksaveasfilename(
            title="Save Voter ID (PNG)",
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png")],
            initialfile=f"{voter_id}.png"
        )
        if not dest:
            messagebox.showinfo("Saved", f"Generated at:\n{os.path.abspath(out_png)}")
            return
        try:
            from shutil import copyfile
            copyfile(out_png, dest)
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file:\n{e}")
            return
        messagebox.showinfo("Saved", f"Voter ID saved to:\n{dest}")

    # -------------------- Tab monitor (optional) --------------------

    def _check_tab_change(self):
        cur = self.tabs.get()
        if cur != self._active_tab:
            self._active_tab = cur
            # Hook: refresh data per tab if needed later
            # e.g., if cur == "Manage Voters": do something
        self.after(700, self._check_tab_change)

    # -------------------- Logout --------------------

    def logout(self):
        self.destroy()
        self.on_logout()"""
# src/gui/registrar_dashboard.py

import os
from datetime import datetime, date
import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
import qrcode

# Database
from src.utils.database import Database

# Simulated fingerprint scanner
from src.utils.biometric_secugen import SecuGenScanner
from src.ai.ai_fingerprint import ai_predict_fingerprint
# Blockchain (optional)
try:
    from src.utils.blockchain import BlockchainManager
except ImportError:
    BlockchainManager = None
import base64

# --------------------------- DISTRICTS --------------------------
KARNATAKA_DISTRICTS = [
    "Bagalkot", "Ballari", "Belagavi", "Bengaluru Rural", "Bengaluru Urban",
    "Bidar", "Chamarajanagar", "Chikkaballapur", "Chikkamagaluru", "Chitradurga",
    "Dakshina Kannada", "Davanagere", "Dharwad", "Gadag", "Hassan",
    "Haveri", "Kalaburagi", "Kodagu", "Kolar", "Koppal",
    "Mandya", "Mysuru", "Raichur", "Ramanagara", "Shivamogga",
    "Tumakuru", "Udupi", "Uttara Kannada", "Vijayapura", "Yadgir"
]


# --------------------------- UTILITIES --------------------------

def _calc_age(dob_str: str) -> int:
    dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
    t = date.today()
    return t.year - dob.year - ((t.month, t.day) < (dob.month, dob.day))


def _ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def _generate_blockchain():
    """Generates blockchain address + private key."""
    if BlockchainManager:
        try:
            mgr = BlockchainManager()
            if hasattr(mgr, "create_voter_account"):
                print("yes")
                return mgr.create_voter_account()
        except:
            print("yes2")
            pass

    # fallback
    import hashlib, os
    pk = hashlib.sha256(os.urandom(32)).hexdigest()
    address = "0x" + hashlib.sha256(pk.encode()).hexdigest()[:40]
    print("no")
    return address, pk


# -------------------- PNG VOTER ID WITH QR ----------------------

def _make_voter_id_png(out_dir, voter_id, name, aadhaar, district, dob):
    _ensure_dir(out_dir)
    W, H = 720, 420
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    d.rectangle([(0, 0), (W, 70)], fill="#1a7f64")
    d.text((20, 22), "Mata Raksha – Voter ID", fill="white", font=font)

    y = 110
    line = 38

    d.text((40, y + 0 * line), f"Voter ID: {voter_id}", font=font, fill="black")
    d.text((40, y + 1 * line), f"Name    : {name}", font=font, fill="black")
    d.text((40, y + 2 * line), f"Aadhaar : XXXX-XXXX-{aadhaar[-4:]}", font=font, fill="black")
    d.text((40, y + 3 * line), f"District: {district}", font=font, fill="black")
    d.text((40, y + 4 * line), f"DOB     : {dob}", font=font, fill="black")

    qr_data = f"{voter_id}|{name}|{aadhaar[-4:]}|{district}|{dob}"
    qr_img = qrcode.make(qr_data).resize((130, 130))
    img.paste(qr_img, (W - 160, H - 180))

    out = os.path.join(out_dir, f"{voter_id}.png")
    img.save(out)
    return out


# --------------------------- MAIN CLASS --------------------------

class RegistrarDashboard(ctk.CTkFrame):

    def __init__(self, root, username, on_logout):
        super().__init__(root)
        self.root = root
        self.username = username
        self.on_logout = on_logout

        self.db = Database()
        self.sg = SecuGenScanner()  # simulated scanner
        self.blockchain = BlockchainManager()
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        self.root.title("Registrar – Mata Raksha")
        self.root.geometry("1000x680")

        self.pack(fill="both", expand=True)

        self._build_top()
        self._build_tabs()

        self._current_tab = None
        self.after(400, self._watch_tabs)

    # ----------------------------- TOP BAR -----------------------------

    def _build_top(self):
        bar = ctk.CTkFrame(self, fg_color="#1a252f", height=50)
        bar.pack(fill="x")

        ctk.CTkLabel(bar, text=f"Registrar: {self.username}",
                     text_color="white", font=("Arial", 18, "bold")).pack(side="left", padx=20, pady=10)

        ctk.CTkButton(bar, text="Logout", fg_color="#e74c3c",
                      command=self.logout).pack(side="right", padx=20, pady=10)

    # ----------------------------- TABS -----------------------------

    def _build_tabs(self):
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True, padx=20, pady=20)

        self.tab_reg = self.tabs.add("Register Voter")
        self.tab_manage = self.tabs.add("Manage Voters")
        self.tab_download = self.tabs.add("Reports & Downloads")

        self._build_register_tab()
        self._build_manage_tab()
        self._build_downloads_tab()

    # ===================== TAB 1 – REGISTER ========================

    def _build_register_tab(self):
        f = ctk.CTkFrame(self.tab_reg)
        f.pack(fill="x", padx=20, pady=20)

        self.r_name = ctk.CTkEntry(f, placeholder_text="Full Name")
        self.r_dob = ctk.CTkEntry(f, placeholder_text="DOB (YYYY-MM-DD)")
        self.r_aadhaar = ctk.CTkEntry(f, placeholder_text="Aadhaar (12 digits)")
        self.r_district = ctk.CTkComboBox(f, values=KARNATAKA_DISTRICTS)

        self.r_district.set(KARNATAKA_DISTRICTS[0])

        self.r_name.grid(row=0, column=0, padx=8, pady=8)
        self.r_dob.grid(row=0, column=1, padx=8, pady=8)
        self.r_aadhaar.grid(row=1, column=0, padx=8, pady=8)
        self.r_district.grid(row=1, column=1, padx=8, pady=8)

        fpbox = ctk.CTkFrame(self.tab_reg)
        fpbox.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(fpbox, text="Fingerprint").pack(anchor="w", pady=5)

        self.r_fp_raw = None

        ctk.CTkButton(fpbox, text="Capture Fingerprint", command=self._capture_fp).pack(side="left", padx=6)
        ctk.CTkButton(fpbox, text="Test Quality", fg_color="#2980b9",
                      command=self._test_fp).pack(side="left", padx=6)

        ctk.CTkButton(self.tab_reg, text="Register Voter", fg_color="#2ecc71",
                      command=self._register_voter).pack(pady=14)

    def _capture_fp(self):
        err, self.img_bytes = self.sg.capture_fingerprint()
        if err != 0 or self.img_bytes is None:
            messagebox.showerror("Error", "Fingerprint capture failed")
            return

        err, self.template = self.sg.create_template(self.img_bytes)
        if err != 0 or self.template is None:
            messagebox.showerror("Error", "Template creation failed")
            return

        # HASH the template
        self.raw = base64.b64encode(self.template).decode()

        messagebox.showinfo("Success", "Fingerprint loaded.")



    def _test_fp(self):
        if not self.img_bytes:
            messagebox.showerror("Fingerprint", "Capture or load a fingerprint first.")
            return
        ai = ai_predict_fingerprint(self.img_bytes)

        messagebox.showinfo(
            "AI Fingerprint Result",
            f"Verdict: {ai['verdict']}\nConfidence: {ai['confidence']}%"
        )
        if ai['verdict']=="FAIL":
            self.raw=None
            
    def _register_voter(self):
        name_ = self.r_name.get().strip()
        dob = self.r_dob.get().strip()
        aadhaar = self.r_aadhaar.get().strip()
        district = self.r_district.get().strip()

        if not all([name_, dob, aadhaar, district, self.raw]):
            messagebox.showerror("Error", "All fields + fingerprint required.")
            return

        if not (aadhaar.isdigit() and len(aadhaar) == 12):
            messagebox.showerror("Error", "Aadhaar must be 12 digits.")
            return

        try:
            if _calc_age(dob) < 18:
                messagebox.showerror("Error", "Voter must be 18+.")
                return
        except:
            messagebox.showerror("Error", "DOB format must be YYYY-MM-DD")
            return
        exists = self.db.get_voter_by_fingerprint()
        for voter_id, name, hash_ in exists:
            tpl_stored=base64.b64decode(hash_)
            matched = self.sg.match_templates(self.template, tpl_stored)
            if matched:
                messagebox.showerror(
                    "Duplicate Fingerprint",
                    f"This fingerprint already belongs to:\n\n"
                    f"Voter ID: {voter_id}\n"
                    f"Name: {name}\n\n"
                    f"Registration stopped."
                )
                self.raw = None
                for w in (self.r_name, self.r_dob, self.r_aadhaar):
                    w.delete(0, "end")
                self.r_district.set(KARNATAKA_DISTRICTS[0])
                return

        #address, privkey = _generate_blockchain()
        address, privkey = self.blockchain.create_voter_account()
        self.blockchain.fund_voter_account(address, 0.1)
        print(address, privkey)
        try:
            voter_id = self.db.register_voter(
                name=name_,
                dob=dob,
                district=district,
                aadhaar=aadhaar,
                fingerprint_hash=self.raw,
                blockchain_address=address,
                private_key=privkey
            )
        except Exception as e:
            messagebox.showerror("DB Error", str(e))
            return

        card = _make_voter_id_png("exports/idcards", voter_id, name_, aadhaar, district, dob)

        messagebox.showinfo("Success",
                            f"Voter Registered!\n\nVoter ID: {voter_id}\nSaved at:\n{card}")

        self.raw = None
        for w in (self.r_name, self.r_dob, self.r_aadhaar):
            w.delete(0, "end")
        self.r_district.set(KARNATAKA_DISTRICTS[0])

    # ==================== TAB 2 – MANAGE ==========================

    def _build_manage_tab(self):
        bar = ctk.CTkFrame(self.tab_manage)
        bar.pack(padx=16, pady=16, fill="x")

        self.m_key = ctk.CTkEntry(bar, placeholder_text="Enter Aadhaar or Voter ID")
        self.m_key.pack(side="left", padx=8)

        ctk.CTkButton(bar, text="Fetch", command=self._m_fetch).pack(side="left", padx=8)

        form = ctk.CTkFrame(self.tab_manage)
        form.pack(fill="x", padx=16, pady=10)

        self.m_voter_id = ctk.CTkEntry(form, placeholder_text="Voter ID", width=150)
        self.m_name = ctk.CTkEntry(form, placeholder_text="Name", width=200)
        self.m_dob = ctk.CTkEntry(form, placeholder_text="DOB", width=150)
        self.m_aadhaar = ctk.CTkEntry(form, placeholder_text="Aadhaar", width=200)
        self.m_district = ctk.CTkComboBox(form, values=KARNATAKA_DISTRICTS)

        self.m_voter_id.grid(row=0, column=0, padx=6, pady=6)
        self.m_name.grid(row=0, column=1, padx=6, pady=6)
        self.m_dob.grid(row=0, column=2, padx=6, pady=6)

        self.m_aadhaar.grid(row=1, column=0, padx=6, pady=6)
        self.m_district.grid(row=1, column=1, padx=6, pady=6)

        fpbox = ctk.CTkFrame(self.tab_manage)
        fpbox.pack(fill="x", padx=16, pady=10)

        self.m_fp_raw = None

        ctk.CTkButton(fpbox, text="Load Fingerprint",
                      command=self._m_load_fp).pack(side="left", padx=6)

        ctk.CTkButton(fpbox, text="Test", fg_color="#3498db",
                      command=self._m_test_fp).pack(side="left", padx=6)

        act = ctk.CTkFrame(self.tab_manage)
        act.pack(fill="x", padx=16, pady=10)

        ctk.CTkButton(act, text="Update", fg_color="#2980b9",
                      command=self._m_update).pack(side="left", padx=6)
        ctk.CTkButton(act, text="Delete", fg_color="#e67e22",
                      command=self._m_delete).pack(side="left", padx=6)

    # -------- Manage functions --------

    def _m_fetch(self):
        key = self.m_key.get().strip()
        if not key:
            messagebox.showerror("Error", "Enter Aadhaar or Voter ID.")
            return

        row = self.db.get_voter_by_aadhaar_or_id(key)
        if not row:
            messagebox.showerror("Not Found", "No voter found.")
            return

        _,vid, name, dob, aadhaar, district,*_= row

        self.m_voter_id.delete(0, "end")
        self.m_name.delete(0, "end")
        self.m_dob.delete(0, "end")
        self.m_aadhaar.delete(0, "end")

        self.m_voter_id.insert(0, vid)
        self.m_name.insert(0, name)
        self.m_dob.insert(0, dob)
        self.m_aadhaar.insert(0, aadhaar)
        self.m_district.set(district)

    def _m_load_fp(self):
        err, self.img_bytes_m = self.sg.capture_fingerprint()
        if err != 0 or self.img_bytes_m is None:
            messagebox.showerror("Error", "Fingerprint capture failed")
            return

        err, self.template_m = self.sg.create_template(self.img_bytes_m)
        if err != 0 or self.template_m is None:
            messagebox.showerror("Error", "Template creation failed")
            return

        # HASH the template
        self.raw_m = base64.b64encode(self.template_m).decode()

        messagebox.showinfo("Success", "Fingerprint loaded.")
    def _m_test_fp(self):
        if not self.img_bytes_m:
            messagebox.showerror("Fingerprint", "Capture or load a fingerprint first.")
            return
        ai = ai_predict_fingerprint(self.img_bytes_m)

        messagebox.showinfo(
            "AI Fingerprint Result",
            f"Verdict: {ai['verdict']}\nConfidence: {ai['confidence']}%"
        )
        if ai['verdict']=="FAIL":
            self.raw_m=None


    def _m_update(self):
        vid = self.m_voter_id.get().strip()
        name = self.m_name.get().strip()
        dob = self.m_dob.get().strip()
        aadhaar = self.m_aadhaar.get().strip()
        district = self.m_district.get().strip()

        if not all([name, dob, aadhaar, district, self.raw_m]):
            messagebox.showerror("Error", "All fields + fingerprint required.")
            return

        exists = self.db.fingerprint_exists_except(vid)
        for voter_id, name, hash_ in exists:
            tpl_stored=base64.b64decode(hash_)
            matched = self.sg.match_templates(self.template_m, tpl_stored)
            if matched:
                messagebox.showerror(
                    "Duplicate Fingerprint",
                    f"This fingerprint already belongs to:\n\n"
                    f"Voter ID: {voter_id}\n"
                    f"Name: {name}\n\n"
                    f"Registration stopped."
                )
                self.raw_m=None
                for w in (self.m_voter_id, self.m_name, self.m_dob, self.m_aadhaar):
                    w.delete(0, "end")
                self.m_district.set(KARNATAKA_DISTRICTS[0])
                return
        
        try:
            self.db.update_voter(vid, name, dob, aadhaar, district, self.raw_m)
            messagebox.showinfo("Updated", "Voter updated.")
        except Exception as e:
            messagebox.showerror("DB Error", str(e))
        self.raw_m=None
        for w in (self.m_voter_id, self.m_name, self.m_dob, self.m_aadhaar):
            w.delete(0, "end")
        self.m_district.set(KARNATAKA_DISTRICTS[0])
        return

    def _m_delete(self):
        vid = self.m_voter_id.get().strip()
        if not vid:
            return
        if not messagebox.askyesno("Confirm", f"Delete {vid}?"):
            return
        self.db.delete_voter(vid)
        messagebox.showinfo("Deleted", f"{vid} removed.")
        self._build_manage_tab()

    # ================= TAB 3 – DOWNLOADS =======================

    def _build_downloads_tab(self):
        frame = ctk.CTkFrame(self.tab_download)
        frame.pack(fill="x", padx=16, pady=16)

        ctk.CTkLabel(frame, text="District PDF Export").grid(row=0, column=0, pady=6)
        self.d_dist = ctk.CTkComboBox(frame, values=KARNATAKA_DISTRICTS)
        self.d_dist.grid(row=1, column=0, padx=6, pady=6)

        ctk.CTkButton(frame, text="Export PDF", command=self._export_pdf).grid(row=1, column=1, padx=10)

        frame2 = ctk.CTkFrame(self.tab_download)
        frame2.pack(fill="x", padx=16, pady=16)

        self.d_key = ctk.CTkEntry(frame2, placeholder_text="Aadhaar or Voter ID")
        self.d_key.grid(row=0, column=0, pady=10)

        ctk.CTkButton(frame2, text="Generate PNG",
                      command=self._export_png).grid(row=0, column=1, padx=10)

        """   def _export_pdf(self):
        dist = self.d_dist.get().strip()
        if not dist:
            return

        rows = self.db.get_voters_by_district(dist)
        if not rows:
            messagebox.showinfo("Empty", "No voters in district.")
            return

        dest = filedialog.asksaveasfilename(defaultextension=".pdf")
        if not dest:
            return

        pages = []
        for voter in rows:
            vid, name, dob, aadhaar, district= voter
            png = _make_voter_id_png("temp_cards", vid, name, aadhaar, district, dob)
            pages.append(Image.open(png).convert("RGB"))

        pages[0].save(dest, save_all=True, append_images=pages[1:])
        messagebox.showinfo("Done", f"Saved PDF:\n{dest}")"""

    def _export_pdf(self):
        dist = self.d_dist.get().strip()
        if not dist:
            return

        rows = self.db.get_voters_by_district(dist)
        if not rows:
            messagebox.showinfo("Empty", "No voters in district.")
            return

        # --- Get Downloads folder path ---
        downloads = str(Path.home() / "Downloads")
        filename = f"{dist}.pdf"
        dest = os.path.join(downloads, filename)

        pages = []
        for voter in rows:
            vid, name, dob, aadhaar, district = voter
            png = _make_voter_id_png("temp_cards", vid, name, aadhaar, district, dob)
            pages.append(Image.open(png).convert("RGB"))

        # Save PDF directly
        pages[0].save(dest, save_all=True, append_images=pages[1:])

        messagebox.showinfo("Done", f"Saved to Downloads:\n{dest}")

    def _export_png(self):
        key = self.d_key.get().strip()
        row = self.db.get_voter_by_aadhaar_or_id(key)
        if not row:
            messagebox.showerror("Not Found", "No voter.")
            return

        _, vid, name, dob, aadhaar, district, *_ = row
        png = _make_voter_id_png("exports/idcards", vid, name, aadhaar, district, dob)

        dest = filedialog.asksaveasfilename(defaultextension=".png")
        if not dest:
            return

        from shutil import copyfile
        copyfile(png, dest)
        messagebox.showinfo("Saved", dest)

    # ---------------- TAB WATCH ----------------
    def _watch_tabs(self):
        cur = self.tabs.get()
        if cur != self._current_tab:
            self._current_tab = cur
        self.after(400, self._watch_tabs)

    # ---------------- LOGOUT -------------------
    def logout(self):
        self.destroy()
        self.on_logout()

