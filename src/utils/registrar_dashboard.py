# src/gui/registrar_dashboard.py

import os
from datetime import datetime, date
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont

import qrcode

# Database
from src.utils.database import Database

# Simulated fingerprint
from src.utils.biometric import SimulatedFingerprint

# AI fingerprint model
from src.ai.ai_fingerprint import ai_predict_fingerprint


# ---------------------- DISTRICTS -----------------------------
KARNATAKA_DISTRICTS = [
    "Bagalkot", "Ballari", "Belagavi", "Bengaluru Rural", "Bengaluru Urban",
    "Bidar", "Chamarajanagar", "Chikkaballapur", "Chikkamagaluru", "Chitradurga",
    "Dakshina Kannada", "Davanagere", "Dharwad", "Gadag", "Hassan",
    "Haveri", "Kalaburagi", "Kodagu", "Kolar", "Koppal",
    "Mandya", "Mysuru", "Raichur", "Ramanagara", "Shivamogga",
    "Tumakuru", "Udupi", "Uttara Kannada", "Vijayapura", "Yadgir"
]


# ---------------------- HELPERS ------------------------------
def _calc_age(dob_str: str) -> int:
    dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
    t = date.today()
    return t.year - dob.year - ((t.month, t.day) < (dob.month, dob.day))


def _ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def _make_voter_id_png(out_dir, voter_id, name, aadhaar, district, dob):
    _ensure_dir(out_dir)

    W, H = 720, 420
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    # Header
    d.rectangle([(0, 0), (W, 70)], fill="#1a7f64")
    d.text((20, 22), "Mata Raksha – Voter ID", fill="white", font=font)

    y = 110
    line = 38

    d.text((40, y + 0*line), f"Voter ID: {voter_id}", font=font, fill="black")
    d.text((40, y + 1*line), f"Name    : {name}", font=font, fill="black")
    d.text((40, y + 2*line), f"Aadhaar : XXXX-XXXX-{aadhaar[-4:]}", font=font, fill="black")
    d.text((40, y + 3*line), f"District: {district}", font=font, fill="black")
    d.text((40, y + 4*line), f"DOB     : {dob}", font=font, fill="black")

    qr_data = f"{voter_id}|{name}|{aadhaar[-4:]}|{district}|{dob}"
    qr_img = qrcode.make(qr_data).resize((130, 130))
    img.paste(qr_img, (W - 160, H - 180))

    out = os.path.join(out_dir, f"{voter_id}.png")
    img.save(out)
    return out


# ---------------------- MAIN CLASS ----------------------------
class RegistrarDashboard(ctk.CTkFrame):

    def __init__(self, root, username, on_logout):
        super().__init__(root)
        self.root = root
        self.username = username
        self.on_logout = on_logout

        self.db = Database()
        self.sg = SimulatedFingerprint()

        self.root.title("Registrar – Mata Raksha")
        self.root.geometry("1000x680")

        self.pack(fill="both", expand=True)

        self._build_top()
        self._build_tabs()

        self._current_tab = None
        self.after(400, self._watch_tabs)

    # ---------------------- TOP BAR ----------------------------
    def _build_top(self):
        bar = ctk.CTkFrame(self, fg_color="#1a252f", height=50)
        bar.pack(fill="x")

        ctk.CTkLabel(
            bar,
            text=f"Registrar: {self.username}",
            text_color="white",
            font=("Arial", 16, "bold")
        ).pack(side="left", padx=16)

        ctk.CTkButton(
            bar,
            text="Logout",
            fg_color="#e74c3c",
            command=self.logout
        ).pack(side="right", padx=16)

    # ---------------------- TABS ------------------------------
    def _build_tabs(self):
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True, padx=16, pady=16)

        self.tab_reg = self.tabs.add("Register Voter")
        self.tab_manage = self.tabs.add("Manage Voters")
        self.tab_download = self.tabs.add("Reports & Downloads")

        self._apply_bg(self.tab_reg)
        self._apply_bg(self.tab_manage)
        self._apply_bg(self.tab_download)

        self._build_register_tab()
        self._build_manage_tab()
        self._build_downloads_tab()

    # ---------------------- Background for Frames Only ----------------------
    def _apply_bg(self, frame):
        """Apply background image ONLY to tabs."""
        try:
            bg_path = "src/assets/bg_fingerprint.png"
            img = ctk.CTkImage(
                light_image=Image.open(bg_path),
                dark_image=Image.open(bg_path),
                size=(1000, 650)
            )
            label = ctk.CTkLabel(frame, image=img, text="")
            label.image = img
            label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print("[BG ERROR]", e)

    # ---------------------- REGISTER TAB ----------------------
    def _build_register_tab(self):
        f = ctk.CTkFrame(self.tab_reg, fg_color="#e8e8e8")
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

        # Fingerprint
        box = ctk.CTkFrame(self.tab_reg, fg_color="#e8e8e8")
        box.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(box, text="Fingerprint").pack(anchor="w", padx=10)

        self.raw = None

        ctk.CTkButton(box, text="Capture Fingerprint",
                      command=self._capture_fp).pack(side="left", padx=8)

        ctk.CTkButton(box, text="Test Quality",
                      fg_color="#2980b9",
                      command=self._test_fp).pack(side="left", padx=8)

        ctk.CTkButton(self.tab_reg, text="Register Voter",
                      fg_color="#2ecc71",
                      command=self._register_voter).pack(pady=15)

    def _capture_fp(self):
        self.raw = self.sg.capture_fingerprint()
        if self.raw:
            messagebox.showinfo("Success", "Fingerprint captured.")
        else:
            messagebox.showerror("Error", "Fingerprint failed.")

    def _test_fp(self):
        if not self.raw:
            messagebox.showerror("Error", "Capture fingerprint first.")
            return

        ai = ai_predict_fingerprint(self.raw)

        messagebox.showinfo(
            "AI Fingerprint Result",
            f"Verdict: {ai['verdict']}\nConfidence: {ai['confidence']}%"
        )

    def _register_voter(self):
        name = self.r_name.get().strip()
        dob = self.r_dob.get().strip()
        aad = self.r_aadhaar.get().strip()
        dist = self.r_district.get().strip()

        if not all([name, dob, aad, dist, self.raw]):
            messagebox.showerror("Error", "All fields + fingerprint required.")
            return

        if len(aad) != 12 or not aad.isdigit():
            messagebox.showerror("Error", "Aadhaar must be 12 digits.")
            return

        try:
            if _calc_age(dob) < 18:
                messagebox.showerror("Error", "Voter must be 18+.")
                return
        except:
            messagebox.showerror("Error", "DOB must be YYYY-MM-DD")
            return

        # ---------------- AI CHECK ----------------
        ai = ai_predict_fingerprint(self.raw)
        if ai["verdict"] == "FAIL":
            messagebox.showerror("AI Blocked", "Poor fingerprint. Try again.")
            return

        fp_hash = self.sg.template_hash(self.raw)

        exists = self.db.fingerprint_exists(fp_hash)
        if exists:
            vid, nm = exists
            messagebox.showerror(
                "Duplicate Fingerprint",
                f"Belongs to Voter ID: {vid}\nName: {nm}"
            )
            return

        voter_id = self.db.register_voter(
            name=name,
            dob=dob,
            district=dist,
            aadhaar=aad,
            fingerprint_hash=fp_hash,
        )

        card = _make_voter_id_png("exports/idcards", voter_id, name, aad, dist, dob)

        messagebox.showinfo("Success", f"Registered!\nVoter ID: {voter_id}")

    # ---------------------- MANAGE TAB -------------------------
    def _build_manage_tab(self):
        bar = ctk.CTkFrame(self.tab_manage, fg_color="#e8e8e8")
        bar.pack(fill="x", pady=20, padx=16)

        self.m_key = ctk.CTkEntry(bar, placeholder_text="Aadhaar or Voter ID")
        self.m_key.pack(side="left", padx=10)

        ctk.CTkButton(bar, text="Fetch", command=self._m_fetch).pack(side="left", padx=10)

        form = ctk.CTkFrame(self.tab_manage, fg_color="#e8e8e8")
        form.pack(fill="x", padx=16, pady=10)

        self.m_vid = None
        self.m_name = ctk.CTkEntry(form, placeholder_text="Name")
        self.m_dob = ctk.CTkEntry(form, placeholder_text="DOB")
        self.m_aadhaar = ctk.CTkEntry(form, placeholder_text="Aadhaar")
        self.m_dist = ctk.CTkComboBox(form, values=KARNATAKA_DISTRICTS)

        self.m_name.grid(row=0, column=0, padx=8, pady=8)
        self.m_dob.grid(row=0, column=1, padx=8, pady=8)
        self.m_aadhaar.grid(row=1, column=0, padx=8, pady=8)
        self.m_dist.grid(row=1, column=1, padx=8, pady=8)

        fpbox = ctk.CTkFrame(self.tab_manage, fg_color="#e8e8e8")
        fpbox.pack(fill="x", padx=16, pady=10)

        self.m_raw = None
        ctk.CTkButton(fpbox, text="Load Fingerprint", command=self._m_load_fp).pack(side="left", padx=10)
        ctk.CTkButton(fpbox, text="Test AI", fg_color="#2980b9", command=self._m_test_fp).pack(side="left", padx=10)

        act = ctk.CTkFrame(self.tab_manage, fg_color="#e8e8e8")
        act.pack(fill="x", padx=16, pady=10)

        ctk.CTkButton(act, text="Update", fg_color="#3498db", command=self._m_update).pack(side="left", padx=10)
        ctk.CTkButton(act, text="Delete", fg_color="#e74c3c", command=self._m_delete).pack(side="left", padx=10)

    def _m_fetch(self):
        key = self.m_key.get().strip()
        row = self.db.get_voter_by_aadhaar_or_id(key)

        if not row:
            messagebox.showerror("Not Found", "No voter found.")
            return

        _, vid, name, dob, aad, dist, *_ = row

        self.m_vid = vid
        self.m_name.delete(0, "end"); self.m_name.insert(0, name)
        self.m_dob.delete(0, "end"); self.m_dob.insert(0, dob)
        self.m_aadhaar.delete(0, "end"); self.m_aadhaar.insert(0, aad)
        self.m_dist.set(dist)

    def _m_load_fp(self):
        self.m_raw = self.sg.capture_fingerprint()
        if self.m_raw:
            messagebox.showinfo("OK", "Fingerprint loaded.")
        else:
            messagebox.showerror("Error", "Failed.")

    def _m_test_fp(self):
        if not self.m_raw:
            messagebox.showerror("Error", "Load fingerprint first.")
            return

        ai = ai_predict_fingerprint(self.m_raw)

        messagebox.showinfo(
            "AI Result",
            f"Verdict: {ai['verdict']}\nConfidence: {ai['confidence']}%"
        )

    def _m_update(self):
        if not self.m_vid:
            return

        if not all([self.m_name.get(), self.m_dob.get(), self.m_aadhaar.get(), self.m_dist.get(), self.m_raw]):
            messagebox.showerror("Error", "All fields + fingerprint required.")
            return

        ai = ai_predict_fingerprint(self.m_raw)
        if ai["verdict"] == "FAIL":
            messagebox.showerror("AI Blocked", "Fingerprint rejected by AI.")
            return

        fp_hash = self.sg.template_hash(self.m_raw)

        # Duplicate check
        duplicate = self.db.fingerprint_exists_except(fp_hash, self.m_vid)
        if duplicate:
            vid, nm = duplicate
            messagebox.showerror(
                "Duplicate",
                f"Fingerprint belongs to {nm}\nVoter ID: {vid}"
            )
            return

        self.db.update_voter(
            self.m_vid,
            self.m_name.get(),
            self.m_dob.get(),
            self.m_aadhaar.get(),
            self.m_dist.get(),
            fp_hash
        )

        messagebox.showinfo("Updated", "Voter updated successfully.")

    def _m_delete(self):
        if not self.m_vid:
            return
        if messagebox.askyesno("Confirm", "Delete voter?"):
            self.db.delete_voter(self.m_vid)
            messagebox.showinfo("Deleted", "Voter deleted.")

    # ---------------------- DOWNLOAD TAB -------------------------
    def _build_downloads_tab(self):
        f = ctk.CTkFrame(self.tab_download, fg_color="#e8e8e8")
        f.pack(pady=20, padx=20, fill="x")

        self.d_dist = ctk.CTkComboBox(f, values=KARNATAKA_DISTRICTS)
        self.d_dist.grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkButton(f, text="Export PDF", command=self._export_pdf).grid(row=0, column=1, padx=10)

        f2 = ctk.CTkFrame(self.tab_download, fg_color="#e8e8e8")
        f2.pack(pady=20, padx=20, fill="x")

        self.d_key = ctk.CTkEntry(f2, placeholder_text="Aadhaar or Voter ID")
        self.d_key.grid(row=0, column=0, pady=10)
        ctk.CTkButton(f2, text="Generate PNG", command=self._export_png).grid(row=0, column=1, padx=10)

    def _export_pdf(self):
        dist = self.d_dist.get()
        rows = self.db.get_voters_by_district(dist)

        if not rows:
            messagebox.showerror("Error", "No voters in district.")
            return

        dest = filedialog.asksaveasfilename(defaultextension=".pdf")
        if not dest:
            return

        from reportlab.pdfgen import canvas
        c = canvas.Canvas(dest)
        y = 800

        for row in rows:
            vid, name, dob, aad, d = row
            c.drawString(50, y, f"{vid} | {name} | {dob} | {aad} | {d}")
            y -= 20
            if y < 50:
                c.showPage()
                y = 800

        c.save()
        messagebox.showinfo("Done", "PDF saved.")

    def _export_png(self):
        key = self.d_key.get()
        row = self.db.get_voter_by_aadhaar_or_id(key)

        if not row:
            messagebox.showerror("Not Found", "No voter.")
            return

        _, vid, name, dob, aad, dist, *_ = row
        png = _make_voter_id_png("exports/idcards", vid, name, aad, dist, dob)

        dest = filedialog.asksaveasfilename(defaultextension=".png")
        if not dest:
            return

        from shutil import copyfile
        copyfile(png, dest)

    # ---------------- WATCH TABS -------------------------
    def _watch_tabs(self):
        cur = self.tabs.get()
        if cur != self._current_tab:
            self._current_tab = cur
        self.after(400, self._watch_tabs)

    # ---------------- LOGOUT -----------------------------
    def logout(self):
        self.destroy()
        self.on_logout()

