import customtkinter as ctk
from datetime import date, timedelta, datetime
from core.kata_log import get_entries
from ui.components import STATUS_COLORS, DIFF_COLORS

class WeeklyReviewPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self._build_stats()
        self._build_kata_list()
        self._build_review_card()

    # ── Stats ─────────────────────────────────────────────────────────────────

    def _build_stats(self):
        entries = self._get_this_week()

        statuses = [e["status"] for e in entries]
        solved   = statuses.count("Solved")
        struggled = statuses.count("Struggled")
        gave_up  = statuses.count("Gave up")

        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(fill="x", pady=(0, 12))
        frame.grid_columnconfigure((0, 1, 2), weight=1)

        stats = [
            (str(len(entries)), "Kata this week"),
            (str(solved),       "Solved"),
            (str(struggled + gave_up), "Struggled or gave up"),
        ]

        for col, (val, label) in enumerate(stats):
            card = ctk.CTkFrame(frame)
            card.grid(row=0, column=col, padx=(0, 8) if col < 2 else 0, sticky="ew")
            ctk.CTkLabel(
                card, text=val,
                font=ctk.CTkFont(size=26, weight="bold")
            ).pack(anchor="w", padx=14, pady=(12, 0))
            ctk.CTkLabel(
                card, text=label,
                font=ctk.CTkFont(size=11), text_color="gray60"
            ).pack(anchor="w", padx=14, pady=(0, 12))

    # ── Kata list ─────────────────────────────────────────────────────────────

    def _build_kata_list(self):
        entries = self._get_this_week()

        card = ctk.CTkFrame(self)
        card.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(
            card, text="KATA LOGGED THIS WEEK",
            font=ctk.CTkFont(size=11), text_color="gray60"
        ).pack(anchor="w", padx=14, pady=(12, 8))

        if not entries:
            ctk.CTkLabel(
                card,
                text="No kata logged this week yet.",
                text_color="gray50", font=ctk.CTkFont(size=13)
            ).pack(anchor="w", padx=14, pady=(0, 12))
            return

        container = ctk.CTkFrame(card, fg_color="transparent")
        container.pack(fill="x", padx=14, pady=(0, 12))

        for entry in entries:
            colors = STATUS_COLORS.get(entry["status"], STATUS_COLORS["Learning"])
            diff_color = DIFF_COLORS.get(entry["difficulty"], "gray50")

            row = ctk.CTkFrame(container, fg_color="gray17", corner_radius=0)
            row.pack(fill="x", pady=(0, 4))

            # left accent bar
            accent = ctk.CTkFrame(row, width=3, corner_radius=0, fg_color=colors["bar"])
            accent.pack(side="left", fill="y")
            accent.pack_propagate(False)

            ctk.CTkLabel(
                row, text=entry["kata_name"],
                font=ctk.CTkFont(size=13), anchor="w"
            ).pack(side="left", padx=(10, 8), pady=8)

            ctk.CTkLabel(
                row, text=f"  {entry['status']}  ",
                font=ctk.CTkFont(size=11),
                fg_color=colors["pill_bg"], text_color=colors["pill_fg"],
                corner_radius=99
            ).pack(side="right", padx=(0, 10))

            ctk.CTkLabel(
                row, text=entry["difficulty"],
                font=ctk.CTkFont(size=11), text_color=diff_color
            ).pack(side="right", padx=(0, 8))

    # ── AI review card ────────────────────────────────────────────────────────

    def _build_review_card(self):
        card = ctk.CTkFrame(self)
        card.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(
            card, text="AI WEEKLY REVIEW",
            font=ctk.CTkFont(size=11), text_color="gray60"
        ).pack(anchor="w", padx=14, pady=(12, 8))

        self.output_box = ctk.CTkTextbox(
            card, height=200, corner_radius=6,
            fg_color="gray17", text_color="gray70",
            state="normal", font=ctk.CTkFont(size=13)
        )
        self.output_box.pack(fill="x", padx=14, pady=(0, 8))
        self.output_box.insert("1.0", "Your AI review will appear here.\nClick generate to summarise your week.")
        self.output_box.configure(state="disabled")

        ctk.CTkButton(
            card,
            text="Generate weekly review",
            height=36,
            fg_color="#534AB7",
            hover_color="#3C3489",
            command=self._generate
        ).pack(fill="x", padx=14, pady=(0, 14))

    def _generate(self):
        # wire to LLM later
        self.output_box.configure(state="normal")
        self.output_box.delete("1.0", "end")
        self.output_box.insert("1.0", "[ LLM output will appear here ]")
        self.output_box.configure(state="disabled")

    # ── Helper ────────────────────────────────────────────────────────────────

    def _get_this_week(self) -> list:
        entries = get_entries()
        start_of_week = date.today() - timedelta(days=date.today().weekday())
        return [
            e for e in entries
            if datetime.strptime(e["timestamp"][:10], "%Y-%m-%d").date() >= start_of_week
        ]