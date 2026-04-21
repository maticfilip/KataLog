import customtkinter as ctk
import json
import os
from datetime import date, datetime
from ui.components import build_entry_row, STATUS_COLORS, DIFF_COLORS
from core.kata_log import add_entry, get_entries, search_entries, group_by_day, DIFFICULTIES, STATUSES

class KataLogPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.selected_status = STATUSES[0]
        self.selected_difficulty = DIFFICULTIES[0]

        self.build_search()
        self.build_write_card()
        self.build_feed_area()
        self.build_feed()


    def build_search(self):
        search_frame=ctk.CTkFrame(self, fg_color="gray17", corner_radius=8)
        search_frame.pack(fill="x", pady=(0,10))

        self.search_var=ctk.StringVar()
        self.search_var.trace_add("write", self.on_search)

        ctk.CTkEntry(
            search_frame,
            placeholder_text="Search kata...",
            textvariable=self.search_var,
            border_width=0,
            fg_color="transparent",
            height=36,
        ).pack(fill="x", padx=8)

    def on_search(self, *args):
        query = self.search_var.get().strip()
        entries = search_entries(query) if query else get_entries()
        self.build_feed(entries)


    def build_write_card(self):
            card = ctk.CTkFrame(self, corner_radius=10)
            card.pack(fill="x", pady=(0, 12))

            ctk.CTkLabel(
                card, text="LOG A KATA",
                font=ctk.CTkFont(size=11), text_color="gray60"
            ).pack(anchor="w", padx=14, pady=(12, 8))

            # kata name input
            self.kata_name_input = ctk.CTkEntry(
                card, placeholder_text="Kata name", height=34, corner_radius=6
            )
            self.kata_name_input.pack(fill="x", padx=14, pady=(0, 8))

            # selectors row
            selectors = ctk.CTkFrame(card, fg_color="transparent")
            selectors.pack(fill="x", padx=14, pady=(0, 8))

            # difficulty selector
            ctk.CTkLabel(
                selectors, text="Difficulty", font=ctk.CTkFont(size=11), text_color="gray60"
            ).pack(side="left", padx=(0, 6))

            self.difficulty_buttons = {}
            for diff in DIFFICULTIES:
                btn = ctk.CTkButton(
                    selectors, text=diff, width=52, height=26,
                    corner_radius=99, border_width=1,
                    fg_color="transparent", text_color="gray60",
                    border_color="gray30",
                    command=lambda d=diff: self._select_difficulty(d),
                )
                btn.pack(side="left", padx=(0, 4))
                self.difficulty_buttons[diff] = btn

            self._select_difficulty(DIFFICULTIES[0])

            # status selector
            status_row = ctk.CTkFrame(card, fg_color="transparent")
            status_row.pack(fill="x", padx=14, pady=(0, 8))

            ctk.CTkLabel(
                status_row, text="Status", font=ctk.CTkFont(size=11), text_color="gray60"
            ).pack(side="left", padx=(0, 6))

            self.status_buttons = {}
            for status in STATUSES:
                colors = STATUS_COLORS.get(status, STATUS_COLORS["Learning"])
                btn = ctk.CTkButton(
                    status_row, text=status, width=80, height=26,
                    corner_radius=99, border_width=1,
                    fg_color="transparent", text_color="gray60",
                    border_color="gray30",
                    command=lambda s=status: self._select_status(s),
                )
                btn.pack(side="left", padx=(0, 4))
                self.status_buttons[status] = btn

            self._select_status(STATUSES[0])

            # notes box
            self.notes_input = ctk.CTkTextbox(card, height=70, corner_radius=6)
            self.notes_input.pack(fill="x", padx=14, pady=(0, 8))
            self.notes_input.insert("1.0", "What did you learn or struggle with?")

            # log button
            btn_row = ctk.CTkFrame(card, fg_color="transparent")
            btn_row.pack(fill="x", padx=14, pady=(0, 12))
            ctk.CTkButton(
                btn_row, text="Log kata", width=100, command=self._save_entry
            ).pack(side="right")
    def _select_difficulty(self, diff: str):
        self.selected_difficulty = diff
        for d, btn in self.difficulty_buttons.items():
            if d == diff:
                color = DIFF_COLORS.get(d, "gray50")
                btn.configure(fg_color="gray20", text_color=color, border_color=color)
            else:
                btn.configure(fg_color="transparent", text_color="gray60", border_color="gray30")

    def _select_status(self, status: str):
        self.selected_status = status
        colors = STATUS_COLORS.get(status, STATUS_COLORS["Learning"])
        for s, btn in self.status_buttons.items():
            if s == status:
                btn.configure(
                    fg_color=colors["pill_bg"],
                    text_color=colors["pill_fg"],
                    border_color=colors["bar"]
                )
            else:
                btn.configure(fg_color="transparent", text_color="gray60", border_color="gray30")

    def _save_entry(self):
        kata_name = self.kata_name_input.get().strip()
        notes = self.notes_input.get("1.0", "end").strip()

        if not kata_name:
            self.kata_name_input.configure(placeholder_text_color="red")
            return

        if notes == "What did you learn or struggle with?":
            notes = ""

        add_entry(
            kata_name=kata_name,
            difficulty=self.selected_difficulty,
            status=self.selected_status,
            notes=notes
        )

        # reset inputs
        self.kata_name_input.delete(0, "end")
        self.notes_input.delete("1.0", "end")
        self.notes_input.insert("1.0", "What did you learn or struggle with?")
        self._select_difficulty(DIFFICULTIES[0])
        self._select_status(STATUSES[0])

        self.build_feed()

    def build_feed_area(self):
        self.feed_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.feed_frame.pack(fill="both", expand=True)

    def build_feed(self, entries: list = None):
        for widget in self.feed_frame.winfo_children():
            widget.destroy()

        if entries is None:
            entries = get_entries()

        if not entries:
            ctk.CTkLabel(
                self.feed_frame,
                text="No kata logged yet — complete one and log it above.",
                text_color="gray50",
                font=ctk.CTkFont(size=13),
            ).pack(pady=20)
            return

        groups = group_by_day(entries)
        for day, day_entries in groups.items():
            self.build_day_group(day, day_entries)
        

    def build_day_group(self, day: str, entries: list):
        day_date = datetime.strptime(day, "%Y-%m-%d").date()
        delta = (date.today() - day_date).days

        if delta == 0:
            label = f"Today — {day_date.strftime('%B %d')}"
        elif delta == 1:
            label = f"Yesterday — {day_date.strftime('%B %d')}"
        else:
            label = day_date.strftime("%A, %B %d")

        ctk.CTkLabel(
            self.feed_frame, text=label,
            font=ctk.CTkFont(size=11), text_color="gray50"
        ).pack(anchor="w", pady=(10, 6))

        for entry in entries:
            build_entry_row(self.feed_frame, entry)

    