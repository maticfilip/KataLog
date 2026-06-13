import customtkinter as ctk
from core.codewars_api import fetch_profile, load_profile, fetch_all, get_completed_this_month,get_language_ranks
from core.kata_log import get_difficulty_breakdown

DIFF_COLORS = {
    "8 kyu": "#888780",
    "7 kyu": "#888780",
    "6 kyu": "#EF9F27",
    "5 kyu": "#EF9F27",
    "4 kyu": "#5DCAA5",
    "3 kyu+": "#AFA9EC",
}

LANG_COLORS = [
    "#3563D4", "#EF9F27", "#E24B4A",
    "#5DCAA5", "#AFA9EC", "#888780",
]
             


class ProfilePage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.build_profile_card()
        self.build_stats()
        self.build_charts()
        self.build_connect_card()


    def connect(self):
        username=self.username_input.get().strip()
        if not username:
            return
        
        self.set_connect_status("Connecting...","gray50")
        self.after(100,lambda:self.do_fetch(username))

    def do_fetch(self, username):
        result=fetch_all(username)

        if "error" in result:
            self.set_connect_status(f"Error: {result["error"]}", "#E24B4A")
            return
        self.set_connect_status("Connected!","#1D9E75")
        self.after(1000, self.refresh)

    def set_connect_status(self, message, color):
        if hasattr(self, "status_label"):
            self.status_label.configure(text=message, text_color=color)

    def refresh(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.build_profile_card()
        self.build_stats()
        self.build_charts()
        self.build_connect_card()

    # ── Connected profile header ──────────────────────────────────────────────

    def build_profile_card(self):
        profile = load_profile()

        username = profile.get("username", "Not connected") if profile else "Not connected"
        honor = f"{profile.get('honor', 0):,}" if profile else "—"
        rank = profile.get("ranks", {}).get("overall", {}).get("name", "—") if profile else "—"
        initials = username[:2].upper()

        card = ctk.CTkFrame(self, fg_color="gray17", corner_radius=10)
        card.pack(fill="x", pady=(0, 12))

        avatar = ctk.CTkFrame(card, width=48, height=48, corner_radius=24, fg_color="#3C3489")
        avatar.pack(side="left", padx=(14, 12), pady=14)
        avatar.pack_propagate(False)
        ctk.CTkLabel(
            avatar, text=initials,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#EEEDFE"
        ).place(relx=0.5, rely=0.5, anchor="center")

        info = ctk.CTkFrame(card, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True, pady=14)

        name_row = ctk.CTkFrame(info, fg_color="transparent")
        name_row.pack(anchor="w")

        ctk.CTkLabel(
            name_row, text=username,
            font=ctk.CTkFont(size=15, weight="bold")
        ).pack(side="left", padx=(0, 8))

        ctk.CTkLabel(
            name_row, text=f"  {rank}  ",
            font=ctk.CTkFont(size=11),
            fg_color="#2A2660", text_color="#AFA9EC",
            corner_radius=99
        ).pack(side="left", padx=(0, 6))

        ctk.CTkLabel(
            name_row, text=f"  {honor} honor  ",
            font=ctk.CTkFont(size=11),
            fg_color="#0A2E22", text_color="#5DCAA5",
            corner_radius=99
        ).pack(side="left")

        ctk.CTkLabel(
            info,
            text="Connected to Codewars" if profile else "Not connected",
            font=ctk.CTkFont(size=11), text_color="gray50"
        ).pack(anchor="w", pady=(4, 0))

        ctk.CTkButton(
            card, text="Sync",
            width=70, height=30,
            fg_color="transparent",
            border_width=1,
            text_color="gray60",
            border_color="gray30",
            corner_radius=8,
            command=lambda: self.do_fetch(username)
        ).pack(side="right", padx=14)


    def build_stats(self):
        profile = load_profile()

        completed = profile.get("codeChallenges", {}).get("totalCompleted", 0) if profile else 0
        authored = profile.get("codeChallenges", {}).get("totalAuthored", 0) if profile else 0
        leaderboard = profile.get("leaderboardPosition", "—") if profile else "—"
        this_month=get_completed_this_month() if profile else 0

        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(fill="x", pady=(0, 12))
        frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        stats = [
            (str(completed),     "Total completed"),
            (str(this_month),                "This month"),       # needs completed kata list later
            (str(authored),      "Kata authored"),
            (f"#{leaderboard}",  "Leaderboard"),
        ]

        for col, (val, label) in enumerate(stats):
            card = ctk.CTkFrame(frame)
            card.grid(row=0, column=col, padx=(0, 8) if col < 3 else 0, sticky="ew")
            ctk.CTkLabel(
                card, text=val,
                font=ctk.CTkFont(size=24, weight="bold")
            ).pack(anchor="w", padx=14, pady=(12, 0))
            ctk.CTkLabel(
                card, text=label,
                font=ctk.CTkFont(size=11), text_color="gray60"
            ).pack(anchor="w", padx=14, pady=(0, 12))


    def build_charts(self):
        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(fill="x", pady=(0, 12))
        row.grid_columnconfigure(0, weight=1)
        row.grid_columnconfigure(1, weight=1)

        self.build_difficulty_chart(row)
        self.build_language_list(row)

    def build_difficulty_chart(self, parent):
        card = ctk.CTkFrame(parent)
        card.grid(row=0, column=0, padx=(0, 6), sticky="nsew")

        ctk.CTkLabel(
            card, text="COMPLETED BY DIFFICULTY",
            font=ctk.CTkFont(size=11), text_color="gray60"
        ).pack(anchor="w", padx=14, pady=(12, 10))

        raw = get_difficulty_breakdown()

        kyu_order = ["8kyu", "7kyu", "6kyu", "5kyu", "4kyu", "3kyu", "2kyu", "1kyu"]
        data = {k: raw.get(k, 0) for k in kyu_order if k in raw}

        bars_frame = ctk.CTkFrame(card, fg_color="transparent")
        bars_frame.pack(fill="x", padx=14, pady=(0, 12))

        if not data:
            ctk.CTkLabel(
                bars_frame, text="No kata logged yet.",
                text_color="gray50", font=ctk.CTkFont(size=12)
            ).pack(anchor="w")
            return

        total = max(data.values())  # use max as 100% reference

        for kyu, count in data.items():
            row = ctk.CTkFrame(bars_frame, fg_color="transparent")
            row.pack(fill="x", pady=(0, 6))

            ctk.CTkLabel(
                row, text=kyu, width=50,
                font=ctk.CTkFont(size=11), text_color="gray60",
                anchor="w"
            ).pack(side="left")

            track = ctk.CTkFrame(row, height=8, corner_radius=99, fg_color="gray25")
            track.pack(side="left", fill="x", expand=True, padx=(6, 8))
            track.pack_propagate(False)

            fill_pct = count / total if total > 0 else 0
            color = DIFF_COLORS.get(kyu, "gray50")

            fill = ctk.CTkFrame(track, height=8, corner_radius=99, fg_color=color)
            fill.place(relx=0, rely=0, relwidth=fill_pct, relheight=1)

            ctk.CTkLabel(
                row, text=str(count), width=28,
                font=ctk.CTkFont(size=11), text_color="gray50",
                anchor="e"
            ).pack(side="left")


    def build_language_list(self, parent):
        card = ctk.CTkFrame(parent)
        card.grid(row=0, column=1, padx=(6, 0), sticky="nsew")

        ctk.CTkLabel(
            card, text="RANK BY LANGUAGE",
            font=ctk.CTkFont(size=11), text_color="gray60"
        ).pack(anchor="w", padx=14, pady=(12, 10))

        langs_frame = ctk.CTkFrame(card, fg_color="transparent")
        langs_frame.pack(fill="x", padx=14, pady=(0, 12))

        language_ranks = get_language_ranks()

        if not language_ranks:
            ctk.CTkLabel(
                langs_frame, text="No language data yet.",
                text_color="gray50", font=ctk.CTkFont(size=12)
            ).pack(anchor="w")
            return

        sorted_langs = sorted(
            language_ranks.items(),
            key=lambda x: x[1].get("rank", 0)
        )

        for i, (lang, rank_data) in enumerate(sorted_langs):
            row = ctk.CTkFrame(langs_frame, fg_color="transparent")
            row.pack(fill="x", pady=(0, 8))

            dot = ctk.CTkFrame(
                row, width=10, height=10,
                corner_radius=5,
                fg_color=LANG_COLORS[i % len(LANG_COLORS)]
            )
            dot.pack(side="left", padx=(0, 8))
            dot.pack_propagate(False)

            display_name = lang.replace("csharp", "C#").replace("cpp", "C++").capitalize()

            ctk.CTkLabel(
                row, text=display_name,
                font=ctk.CTkFont(size=13)
            ).pack(side="left")

            ctk.CTkLabel(
                row, text=rank_data.get("name", "—"),
                font=ctk.CTkFont(size=11), text_color="gray50"
            ).pack(side="right")


    def build_connect_card(self):
        card = ctk.CTkFrame(self, fg_color="gray17", corner_radius=10, border_width=1, border_color="gray30")
        card.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(
            card, text="Connect your Codewars account",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(pady=(16, 4))

        ctk.CTkLabel(
            card, text="Enter your Codewars username to sync your profile and stats",
            font=ctk.CTkFont(size=11), text_color="gray50"
        ).pack(pady=(0, 12))

        input_row = ctk.CTkFrame(card, fg_color="transparent")
        input_row.pack(pady=(0, 16))

        self.username_input = ctk.CTkEntry(
            input_row,
            placeholder_text="Your Codewars username",
            width=220, height=34
        )
        self.username_input.pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            input_row,
            text="Connect",
            width=90, height=34,
            fg_color="#534AB7",
            hover_color="#3C3489",
            command=self.connect
        ).pack(side="left")
