import customtkinter as ctk
from datetime import datetime

from ui.kata_log import KataLogPage
from ui.dashboard import DashboardPage
from ui.weekly_review import WeeklyReviewPage
from ui.profile import ProfilePage
from ui.settings import SettingsPage

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

#.........sidebar............#

class NavButton(ctk.CTkFrame):
    def __init__(self, master, text, command, **kwargs):
        super().__init__(
            master,
            height=36,
            fg_color="transparent",
            **kwargs,
        )
        self.grid_propagate(False)
        self.command=command
        
        self.accent=ctk.CTkFrame(self, width=3, height=36, corner_radius=0)
        self.accent.pack(side="left",fill="y")

        self.btn=ctk.CTkButton(
            self,
            text=text,
            command=command,
            anchor="w",
            fg_color="transparent",
            text_color=("gray50","gray50"),
            hover_color=("gray85","gray25"),
            corner_radius=0,
            height=36
        )

        self.btn.pack(side="left",fill="both", expand=True)
        self.set_active(False)


    def set_active(self, active:bool):
        if active:
            self.accent.configure(fg_color="#534AB7")
            self.configure(fg_color="gray25")
            self.btn.configure(
                fg_color=("gray80","gray25"),
                text_color=("gray10","white"),
                font=ctk.CTkFont(weight="bold")
            )
        else:
            self.accent.configure(fg_color="transparent")
            self.configure(fg_color="transparent")
            self.btn.configure(
                fg_color="transparent",
                text_color=("gray60","gray60"),
                font=ctk.CTkFont(weight="normal")
            )

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("960x620")
        self.minsize(800,500)
        self.title("Codewars journal and assistant")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.build_sidebar()
        self.build_main()

        self.show_page("dashboard")


    def build_sidebar(self):
        self.sidebar=ctk.CTkFrame(self, width=180, corner_radius=0, fg_color=("gray88","gray16"))
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        ctk.CTkLabel(
            self.sidebar,
            text="KataLog",
            font=ctk.CTkFont(size=15, weight="bold"),
        ).pack(pady=(24,20), padx=16, anchor="w")

        self.nav_buttons:dict[str, NavButton]={}

        nav_items=[
            ("dashboard"," Dashboard"),
            ("journal", " Your Kata"),
            ("review", " Review"),
            ("profile", " Your Profile"),
            ("settings","Settings")
        ]
        
        for key, label in nav_items:
            btn=NavButton(
                self.sidebar,
                text=label,
                command=lambda k=key: self.show_page(k)
            )
            btn.pack(fill="x", padx=10, pady=2)
            self.nav_buttons[key]=btn


    def build_main(self):
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.topbar = ctk.CTkFrame(self.main_frame, height=52, corner_radius=0)
        self.topbar.grid(row=0, column=0, sticky="ew")
        self.topbar.grid_propagate(False)

        self.page_title_label = ctk.CTkLabel(
            self.topbar, text="Dashboard",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.page_title_label.pack(side="left", padx=20, pady=14)

        # refresh button — right side of topbar
        self.refresh_btn = ctk.CTkButton(
            self.topbar,
            text="↺  Refresh",
            width=90, height=28,
            fg_color="transparent",
            border_width=1,
            text_color="gray60",
            border_color="gray30",
            hover_color="gray25",
            font=ctk.CTkFont(size=12),
            command=self.refresh_current_page
        )
        self.refresh_btn.pack(side="right", padx=16)

        self.content_area = ctk.CTkScrollableFrame(
            self.main_frame, corner_radius=0, fg_color="transparent"
        )
        self.content_area.grid(row=1, column=0, sticky="nsew", padx=20, pady=16)
        self.content_area.grid_columnconfigure(0, weight=1)

        self.pages: dict[str, ctk.CTkFrame] = {
            "dashboard": DashboardPage(self.content_area),
            "journal":   KataLogPage(self.content_area, app=self),
            "review":    WeeklyReviewPage(self.content_area),
            "profile":   ProfilePage(self.content_area),
            "settings":  SettingsPage(self.content_area),
        }
        for page in self.pages.values():
            page.grid(row=0, column=0, sticky="nsew")


    def show_page(self, key: str):
        titles = {
            "dashboard": "Dashboard",
            "journal":   "Your Kata",
            "review":    "Weekly Review",
            "profile":   "Profile",
            "settings":  "Settings",
        }
        self.current_page = key    # track active page

        # hide refresh button on pages that don't need it
        if key in ("journal", "settings"):
            self.refresh_btn.pack_forget()
        else:
            self.refresh_btn.pack(side="right", padx=16)

        self.page_title_label.configure(text=titles.get(key, key.title()))
        for k, btn in self.nav_buttons.items():
            btn.set_active(k == key)
        self.pages[key].tkraise()

    def refresh_current_page(self):
        key = getattr(self, "current_page", "dashboard")
        page = self.pages.get(key)
        if page and hasattr(page, "refresh"):
            page.refresh()

    def refresh_dashboard(self):
        self.pages["dashboard"].refresh()
    


