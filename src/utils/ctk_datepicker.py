import customtkinter as ctk
from tkinter import Toplevel
from datetime import date, datetime
import calendar

class CTkDatePicker:
    def __init__(self, parent, entry, mode="election"):
        self.parent = parent
        self.entry = entry
        self.mode = mode.lower().strip()
        self.popup = None
        self.today = date.today()

        self.entry.bind("<Button-1>", self.open_picker)

    # ------------------------------------------------------------
    # OPEN POPUP (FADE + SLIDE ENGINE INCLUDED)
    # ------------------------------------------------------------
    def open_picker(self, event=None):
        if self.popup and self.popup.winfo_exists():
            return

        # Create popup
        self.popup = Toplevel(self.parent)
        self.popup.overrideredirect(True)
        self.popup.attributes("-topmost", True)
        self.popup.attributes("-alpha", 0)

        # --- DARK POPUP BACKGROUND ---
        self.popup.configure(bg="#1A1A1A")

        # Position popup under entry
        x = self.entry.winfo_rootx()
        y = self.entry.winfo_rooty() + self.entry.winfo_height() + 2
        self.popup.geometry(f"{330}x{300}+{x}+{y}")

        # Dark container
        self.container = ctk.CTkFrame(
            self.popup,
            corner_radius=20,
            fg_color="#E9E3E3"
        )
        self.container.place(relwidth=1, relheight=1, relx=0.5, rely=0.5, anchor="center")

        # Initial values
        now = datetime.now()
        self.year = now.year
        self.month = now.month

        # Show DAY view
        self.show_day_view(initial=True)

        # Fade-in animation
        self.fade_in()

        # Close when clicking outside
        self.root = self.parent._root()
        self.root.bind("<Button-1>", self.detect_outside_click)


    # ------------------------------------------------------------
    # OUTSIDE CLICK HANDLER
    # ------------------------------------------------------------
    def detect_outside_click(self, event):
        if not self.popup or not self.popup.winfo_exists():
            return

        px, py = self.popup.winfo_rootx(), self.popup.winfo_rooty()
        pw, ph = self.popup.winfo_width(), self.popup.winfo_height()
        mx, my = event.x_root, event.y_root

        if px <= mx <= px + pw and py <= my <= py + ph:
            return

        self.close_popup()

    # ------------------------------------------------------------
    # CLOSE POPUP
    # ------------------------------------------------------------
    def close_popup(self, event=None):
        if self.popup and self.popup.winfo_exists():
            self.popup.destroy()
        if hasattr(self, "root"):
            self.root.unbind("<Button-1>")

    # ------------------------------------------------------------
    # FADE IN
    # ------------------------------------------------------------
    def fade_in(self):
        for i in range(0, 11):
            try:
                self.popup.attributes("-alpha", i/10)
                self.popup.update()
                self.popup.after(10)
            except:
                break

    # ------------------------------------------------------------
    # HEADER (YEAR BUTTON + MONTH BUTTON)
    # ------------------------------------------------------------
    def render_header(self, parent, show_month=True):
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(pady=10)

        # YEAR BUTTON
        self.year_btn = ctk.CTkButton(
            header, text=f"{self.year} ▼",
            width=120, fg_color="#1f6aa5",
            font=("Arial", 14, "bold"),
            command=self.show_year_view
        )
        self.year_btn.pack(side="left", padx=6)

        # MONTH BUTTON
        if show_month:
            month_name = calendar.month_name[self.month]
            self.month_btn = ctk.CTkButton(
                header, text=f"{month_name} ▼",
                width=120, fg_color="#1f6aa5",
                font=("Arial", 14, "bold"),
                command=self.show_month_view
            )
            self.month_btn.pack(side="left", padx=6)

    # ------------------------------------------------------------
    # YEAR VIEW (scrollable)
    # ------------------------------------------------------------
    def show_year_view(self):
        for w in self.container.winfo_children():
            w.destroy()

        frame = ctk.CTkScrollableFrame(self.container)
        frame.pack(fill="both", expand=True)

        if self.mode == "election":
            start_year = self.today.year
            end_year = self.today.year + 2
        else:  # DOB mode
            start_year = self.today.year - 120
            end_year = self.today.year

        for y in range(end_year, start_year - 1, -1):
            disabled = False
            if self.mode == "election" and y < self.today.year: disabled = True
            if self.mode == "dob" and y > self.today.year: disabled = True

            btn = ctk.CTkButton(
                frame,
                text=str(y),
                width=240,
                state="disabled" if disabled else "normal",
                fg_color="#1f6aa5",
                command=lambda yr=y: self.select_year(yr)
            )
            btn.pack(pady=3)

    def select_year(self, yr):
        self.year = yr
        self.show_month_view(slide_left=True)

    # ------------------------------------------------------------
    # MONTH VIEW
    # ------------------------------------------------------------
    def show_month_view(self, slide_left=False):
        for w in self.container.winfo_children():
            w.destroy()

        self.render_header(self.container, show_month=False)

        months = [
            "January","February","March","April","May","June",
            "July","August","September","October","November","December"
        ]

        grid = ctk.CTkFrame(self.container)
        grid.pack(pady=10)

        for i, m in enumerate(months):
            r, c = divmod(i, 3)
            btn = ctk.CTkButton(
                grid, text=m, width=90, fg_color="#1f6aa5",
                command=lambda idx=i+1: self.select_month(idx)
            )
            btn.grid(row=r, column=c, padx=6, pady=6)

    def select_month(self, m):
        self.month = m
        self.show_day_view(slide_left=True)

    # ------------------------------------------------------------
    # DAY VIEW
    # ------------------------------------------------------------
    def show_day_view(self, initial=False, slide_left=False):
        for w in self.container.winfo_children():
            w.destroy()

        self.render_header(self.container, show_month=True)

        days_frame = ctk.CTkFrame(self.container,corner_radius=20,
            fg_color="#AAAAAA"
        )
        days_frame.pack(pady=10)

        week_days = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]

        for i, d in enumerate(week_days):
            ctk.CTkLabel(days_frame, text=d).grid(row=0, column=i, padx=4)

        cal = calendar.monthcalendar(self.year, self.month)

        for r, week in enumerate(cal, start=1):
            for c, day in enumerate(week):
                if day == 0:
                    continue

                ddate = date(self.year, self.month, day)

                disabled = False
                if self.mode == "election" and ddate < self.today:
                    disabled = True
                if self.mode == "dob" and ddate > self.today:
                    disabled = True

                ctk.CTkButton(
                    days_frame,
                    text=str(day),
                    width=40,
                    state="disabled" if disabled else "normal",
                    fg_color="#cccccc",
                    text_color="#000000",
                    command=lambda d=day: self.select_date(d)
                ).grid(row=r, column=c, padx=3, pady=3)

    # ------------------------------------------------------------
    # FINAL SELECT
    # ------------------------------------------------------------
    def select_date(self, d):
        selected = f"{self.year:04d}-{self.month:02d}-{d:02d}"
        self.entry.delete(0, "end")
        self.entry.insert(0, selected)
        self.close_popup()
