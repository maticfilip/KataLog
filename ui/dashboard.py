import customtkinter as ctk
from core.kata_log import get_streak, get_stats
from datetime import date

class DashboardPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent",**kwargs)

        intro_frame=ctk.CTkFrame(self, fg_color="transparent")
        intro_frame.pack(fill="x", pady=(0,12))
        intro_frame.grid_columnconfigure((0,1,2), weight=1)

        ctk.CTkLabel(
            intro_frame,
            text="KataLog",
            font=ctk.CTkFont(size=15, weight="bold"),
        ).pack(padx=16, anchor="w")
        ctk.CTkLabel(
            intro_frame,
            text="Unofficial helper app for your CodeWars experience",
            font=ctk.CTkFont(size=12),
        ).pack(padx=16, anchor="w")

        stats_frame=ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(0,12))
        stats_frame.grid_columnconfigure((0,1,2),weight=1)

        stats=[
            ("12","Journal entries this week"),
            ("4/5", "Habits done today"),
            ("14","Day streak")
        ]
        for col, (val, label) in enumerate(stats):
            card=ctk.CTkFrame(stats_frame)
            card.grid(row=0, column=col, padx=(0,8) if col < 2 else 0, sticky="ew")
            ctk.CTkLabel(card, text=val, font=ctk.CTkFont(size=26, weight="bold")).pack(
                anchor="w", padx=14, pady=(12,0)
            )
            ctk.CTkLabel(
                card, text=label, font=ctk.CTkFont(size=12), text_color="gray60"
            ).pack(anchor="w",padx=14,pady=(0,12))


        log_card=ctk.CTkFrame(self)
        log_card.pack(fill="x", pady=(0,12))

        ctk.CTkLabel(
            log_card, text="QUICK LOG", font=ctk.CTkFont(size=11), text_color="gray60"
        ).pack(anchor="w",padx=14, pady=(12,6))

        self.log_input=ctk.CTkTextbox(log_card, height=80, corner_radius=6)
        self.log_input.pack(fill="x",padx=14, pady=(0,8))
        self.log_input.insert("1.0","What are you working on?")

        btn_frame=ctk.CTkFrame(log_card, fg_color="transparent")
        btn_frame.pack(anchor="w", padx=14, pady=(0,12))
        ctk.CTkButton(btn_frame, text="Log entry", width=100, command=self.log_entry).pack(
            side="left", padx=(0,8)
        )
        ctk.CTkButton(
            btn_frame,
            text="Rubber duck",
            width=130, 
            fg_color="transparent",
            border_width=1,
            text_color=("gray10","gray90")
        ).pack(side="left")

        #-----------------#

        recent_card=ctk.CTkFrame(self)
        recent_card.pack(fill="x")

        ctk.CTkLabel(
            recent_card,
            text="RECENT JOURNAL ENTRIES",
            font=ctk.CTkFont(size=11),
            text_color="gray60"
        ).pack(anchor="w", padx=14, pady=(12,6))

        entries=[
            ("2:35 PM", "Test test test Test test test Test test test ","bug fix"),
            ("2:35 PM", "Test test test Test test test Test test test ","bug fix"),
        ]

        for time, text,tag in entries:
            entry_frame=ctk.CTkFrame(recent_card, corner_radius=6)
            entry_frame.pack(fill="x", padx=14, pady=(0,8))

            ctk.CTkLabel(
                entry_frame, text=time, font=ctk.CTkFont(size=11), text_color="gray60"
            ).pack(anchor="w", padx=10, pady=(8, 0))
            ctk.CTkLabel(
                entry_frame, text=text, wraplength=560, justify="left", font=ctk.CTkFont(size=13)
            ).pack(anchor="w", padx=10, pady=(2, 4))
            ctk.CTkLabel(
                entry_frame,
                text=f"  {tag}  ",
                font=ctk.CTkFont(size=11),
                fg_color=("#DDDAFC", "#3D3780"),
                text_color=("#3D3780", "#DDDAFC"),
            ).pack(anchor="w", padx=10, pady=(0, 8))

        #-----------------#


        streak_card=ctk.CTkFrame(self)
        streak_card.pack(fill="x", pady=(12,0))

        ctk.CTkLabel(streak_card, text="DAILY STREAK", font=ctk.CTkFont(size=11), text_color="gray60").pack(anchor="w",padx=14, pady=(12,8))

        streak_row=ctk.CTkFrame(streak_card, fg_color="transparent")
        streak_row.pack(anchor="w", padx=14, pady=(0,12))

        days=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        streak=get_streak()

        today_weekday=date.today().weekday()
        day_labels=[]
        for i in range(7):
            offset=i-6
            idx=(today_weekday+offset)%7
            day_labels.append(days[idx])

        for i, (did, label) in enumerate(zip(streak, day_labels)):
            col=ctk.CTkFrame(streak_row, fg_color="transparent")
            col.pack(side="left", padx=(0,12))

            color="#534AB7" if did else "gray30"
            dot=ctk.CTkFrame(col,width=28,height=28, corner_radius=6, fg_color=color)
            dot.pack()
            dot.pack_propagate(False)

            if did:
                ctk.CTkLabel(
                    dot, text="✓",
                    font=ctk.CTkFont(size=13, weight="bold"),
                    text_color="white"
                ).place(relx=0.5, rely=0.5, anchor="center")
            ctk.CTkLabel(
                col, text=label,
                font=ctk.CTkFont(size=10), text_color="gray50"
            ).pack(pady=(4, 0))




        #-----------------#

        

    def log_entry(self):
        text=self.log_input.get("1.0","end").strip()
        if text:
            print(f"[LOG] {text}")

    

