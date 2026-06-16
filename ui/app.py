import customtkinter as ctk
from datetime import datetime

from ui.kata_log import KataLogPage
from ui.dashboard import DashboardPage
from ui.weekly_review import WeeklyReviewPage
from ui.profile import ProfilePage
from ui.settings import SettingsPage
from ui.theory import TheoryPage

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

class LandingPage(ctk.CTkFrame):
    def __init__(self, master,  on_done, **kwargs):
        super().__init__(master, fg_color="#0F0F0F", corner_radius=0, **kwargs)
        self.on_done=on_done
        self.build()

    def build(self):
        # self.grid_rowconfigure(0, weight=1)
        # self.grid_rowconfigure(2, weight=1)
        # self.grid_columnconfigure(0, weight=1)

        self.pack_propagate(False)

        center = ctk.CTkFrame(self, fg_color="transparent")
        center.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            center,
            text="KataLog",
            font=ctk.CTkFont(size=52, weight="bold"),
            text_color="#EEEDFE"
        ).pack(pady=(0, 8))

        ctk.CTkFrame(
            center,
            width=60, height=3,
            corner_radius=99,
            fg_color="#534AB7"
        ).pack(pady=(0, 28))

        ctk.CTkLabel(
            center,
            text="Your personal Codewars companion.",
            font=ctk.CTkFont(size=16),
            text_color="gray60"
        ).pack(pady=(0, 6))

        ctk.CTkLabel(
            center,
            text="Log what you learn from each kata, track your daily streak,\nget AI-powered feedback on your solutions — all running locally.",
            font=ctk.CTkFont(size=13),
            text_color="gray40",
            justify="center"
        ).pack(pady=(0, 48))

        ctk.CTkButton(
            center,
            text="Get started →",
            width=180, height=44,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#534AB7",
            hover_color="#3C3489",
            corner_radius=10,
            command=self._enter
        ).pack()

        ctk.CTkLabel(
            center,
            text="v0.1.0  ·  built with Python & CustomTkinter",
            font=ctk.CTkFont(size=11),
            text_color="gray30"
        ).pack(pady=(32, 0))

    def _enter(self):
        self._fade_out()

    def _fade_out(self, alpha: float = 1.0):
        if alpha <= 0.0:
            self.destroy()
            self.on_done()
            return
        self.master.attributes("-alpha", alpha)
        self.after(16, lambda: self._fade_out(round(alpha - 0.06, 2)))

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("960x620")
        self.minsize(800,500)
        self.title("KataLog")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.show_landing()

    def show_landing(self):
        self.landing=LandingPage(self, on_done=self.launch_app)
        self.landing.place(x=0, y=0, relwidth=1, relheight=1)

    def launch_app(self):
        self.attributes("-alpha",1.0)

        self.grid_columnconfigure(0, weight=0)
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
            ("settings","Settings"),
            ("theory","Theory")
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
            "theory":   TheoryPage(self.content_area),
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
            "theory":   "Theory",
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
    


