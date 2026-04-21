import customtkinter as ctk
from core.kata_log import get_streak, get_stats, calculate_weekly_entries, get_streak_number, check_today, get_entries
from datetime import date
from ui.components import build_entry_row, STATUS_COLORS, DIFF_COLORS


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

        entries_counter=calculate_weekly_entries()
        streak_counter=get_streak_number()
        did_today=check_today()

        stats=[
            (entries_counter,"Journal entries this week"),
            (streak_counter,"Day streak")
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

        today_card=ctk.CTkFrame(stats_frame)
        today_card.grid(row=0, column=2, sticky="ew")

        ctk.CTkLabel(
            today_card, 
            text="✓" if did_today else "✗",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="#1D9E75" if did_today else "#E24B4A"
        ).pack(anchor="w", padx=14, pady=(12,0))

        ctk.CTkLabel(
            today_card,
            text="Kata done today",
            font=ctk.CTkFont(size=12),
            text_color="gray60"
        ).pack(anchor="w", padx=14, pady=(0,12))

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

        recent_card=ctk.CTkFrame(self)
        recent_card.pack(fill="x", pady=(12,0))

        ctk.CTkLabel(
            recent_card, text="RECENT KATA", font=ctk.CTkFont(size=11), text_color="gray60"
        ).pack(anchor="w", padx=14, pady=(12,8))

        recent_container=ctk.CTkFrame(recent_card, fg_color="transparent")
        recent_container.pack(fill="x", padx=14, pady=(0,12))

        entries=get_entries()[:3]

        if not entries:
            ctk.CTkLabel(recent_container, text="No kata logged yet.", text_color="gray50",
                         font=ctk.CTkFont(size=13)).pack(anchor="w")
        else:
            for entry in entries:
                build_entry_row(recent_container, entry)

        #-----------------#


    def log_entry(self):
        text=self.log_input.get("1.0","end").strip()
        if text:
            print(f"[LOG] {text}")

    

