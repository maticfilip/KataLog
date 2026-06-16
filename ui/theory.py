import customtkinter as ctk
from datetime import datetime, date
from core.theory import (
    get_topics, get_topics_by_category,
    get_category_counts, delete_topic,
    search_topics, CATEGORIES
)
from ui.components import confirm_delete

CATEGORY_COLORS = {
    "Algorithms":          {"bg": "#2A2660", "fg": "#AFA9EC"},
    "Data Structures":     {"bg": "#0A2E22", "fg": "#5DCAA5"},
    "String Manipulation": {"bg": "#2E1E04", "fg": "#EF9F27"},
    "Mathematics":         {"bg": "#3D1515", "fg": "#F09595"},
    "Language Features":   {"bg": "#0A1F3D", "fg": "#85B7EB"},
    "Other":               {"bg": "#222222", "fg": "#888888"},
}


class TheoryPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.selected_category = None
        self.expanded_cards = set()
        self._all_cards = []

        self._build_search()
        self._build_body()

    # ── Search ────────────────────────────────────────────────────────────────

    def _build_search(self):
        search_frame = ctk.CTkFrame(self, fg_color="gray17", corner_radius=8)
        search_frame.pack(fill="x", pady=(0, 10))

        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self._on_search)

        ctk.CTkEntry(
            search_frame,
            placeholder_text="Search topics...",
            textvariable=self.search_var,
            border_width=0,
            fg_color="transparent",
            height=36,
        ).pack(fill="x", padx=8)

    def _on_search(self, *args):
        self._apply_filter(self.search_var.get().strip())

    # ── Body ──────────────────────────────────────────────────────────────────

    def _build_body(self):
        self.body_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.body_frame.pack(fill="both", expand=True)
        self.body_frame.grid_columnconfigure(1, weight=1)
        self.body_frame.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_feed_area()
        self._build_all_cards()
        self._apply_filter()

    # ── Sidebar ───────────────────────────────────────────────────────────────

    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self.body_frame, width=160, fg_color="transparent"
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        self.sidebar.grid_propagate(False)
        self._rebuild_sidebar()

    def _rebuild_sidebar(self):
        for widget in self.sidebar.winfo_children():
            widget.destroy()

        counts = get_category_counts()
        total = sum(counts.values())

        self._cat_btn(self.sidebar, "All topics", total, None)

        ctk.CTkFrame(
            self.sidebar, height=1, fg_color="gray25"
        ).pack(fill="x", pady=8)

        for cat in CATEGORIES:
            self._cat_btn(self.sidebar, cat, counts.get(cat, 0), cat)

    def _cat_btn(self, parent, label: str, count: int, category):
        is_active = self.selected_category == category
        colors = CATEGORY_COLORS.get(category, {"bg": "gray25", "fg": "gray60"})

        row = ctk.CTkFrame(
            parent,
            fg_color=colors["bg"] if is_active else "transparent",
            corner_radius=6
        )
        row.pack(fill="x", pady=2)

        ctk.CTkLabel(
            row, text=label,
            font=ctk.CTkFont(size=12, weight="bold" if is_active else "normal"),
            text_color=colors["fg"] if is_active else "gray60",
            anchor="w"
        ).pack(side="left", padx=10, pady=7)

        ctk.CTkLabel(
            row, text=str(count),
            font=ctk.CTkFont(size=11),
            fg_color=colors["bg"] if is_active else "gray25",
            text_color=colors["fg"] if is_active else "gray50",
            corner_radius=99,
            width=24
        ).pack(side="right", padx=8)

        # bind click on row and all children
        for widget in [row] + list(row.winfo_children()):
            widget.bind("<Button-1>", lambda e, c=category: self._select_category(c))

    def _select_category(self, category):
        self.selected_category = category
        self._rebuild_sidebar()
        self._apply_filter(self.search_var.get().strip())

    # ── Feed ──────────────────────────────────────────────────────────────────

    def _build_feed_area(self):
        self.feed_frame = ctk.CTkFrame(
            self.body_frame, fg_color="transparent"
        )
        self.feed_frame.grid(row=0, column=1, sticky="nsew")

        self.empty_label = ctk.CTkLabel(
            self.feed_frame,
            text="No topics saved yet.\nGet an AI explanation from any kata entry\nto start building your library.",
            text_color="gray50",
            font=ctk.CTkFont(size=13),
            justify="center"
        )

    def _build_all_cards(self):
        for _, card in self._all_cards:
            card.destroy()
        self._all_cards = []

        for topic in get_topics():
            card = self._build_topic_card(topic)
            self._all_cards.append((topic, card))

    def _apply_filter(self, query: str = ""):
        self.empty_label.pack_forget()
        visible = 0

        for topic, card in self._all_cards:
            show = True

            if self.selected_category and topic["category"] != self.selected_category:
                show = False

            if query:
                match = (
                    query.lower() in topic["topic"].lower() or
                    query.lower() in topic["explanation"].lower()
                )
                if not match:
                    show = False

            if show:
                card.pack(fill="x", pady=(0, 8))
                visible += 1
            else:
                card.pack_forget()

        if visible == 0:
            self.empty_label.pack(pady=40)

    # ── Topic card ────────────────────────────────────────────────────────────

    def _build_topic_card(self, topic: dict) -> ctk.CTkFrame:
        colors = CATEGORY_COLORS.get(topic["category"], CATEGORY_COLORS["Other"])
        explanation = topic.get("explanation", "")
        is_long = len(explanation) > 180

        card = ctk.CTkFrame(self.feed_frame, corner_radius=10, fg_color="gray17")

        # left accent bar
        accent = ctk.CTkFrame(card, width=3, corner_radius=0, fg_color=colors["bg"])
        accent.pack(side="left", fill="y")
        accent.pack_propagate(False)

        # main content
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(side="left", fill="both", expand=True, padx=12, pady=10)

        # ── top row ───────────────────────────────────────────────────────────
        top = ctk.CTkFrame(inner, fg_color="transparent")
        top.pack(fill="x")

        ctk.CTkLabel(
            top, text=topic["topic"],
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        ).pack(side="left", padx=(0, 8))

        ctk.CTkLabel(
            top,
            text=f"  {topic['category']}  ",
            font=ctk.CTkFont(size=11),
            fg_color=colors["bg"],
            text_color=colors["fg"],
            corner_radius=99,
        ).pack(side="left")

        # timestamp
        day_date = datetime.strptime(topic["timestamp"][:10], "%Y-%m-%d").date()
        delta = (date.today() - day_date).days
        if delta == 0:
            time_str = "Today"
        elif delta == 1:
            time_str = "Yesterday"
        else:
            time_str = f"{delta} days ago"

        ctk.CTkLabel(
            top, text=time_str,
            font=ctk.CTkFont(size=11), text_color="gray50"
        ).pack(side="right", padx=(8, 0))

        # delete button
        ctk.CTkButton(
            top, text="✕",
            width=24, height=24,
            fg_color="transparent",
            hover_color="gray25",
            text_color="gray50",
            font=ctk.CTkFont(size=11),
            command=lambda t=topic: self._delete_topic(t)
        ).pack(side="right")

        # ── explanation ───────────────────────────────────────────────────────
        preview = explanation[:180] + "..." if is_long else explanation

        explanation_label = ctk.CTkLabel(
            inner,
            text=preview,
            font=ctk.CTkFont(size=13),
            text_color="gray70",
            wraplength=440,
            justify="left",
            anchor="w"
        )
        explanation_label.pack(anchor="w", pady=(6, 0))

        # ── footer ────────────────────────────────────────────────────────────
        footer = ctk.CTkFrame(inner, fg_color="transparent")
        footer.pack(fill="x", pady=(6, 0))

        if topic.get("related_kata"):
            ctk.CTkLabel(
                footer,
                text=f"↳  {topic['related_kata']}",
                font=ctk.CTkFont(size=11),
                text_color="#534AB7"
            ).pack(side="left")

        if is_long:
            expand_btn = ctk.CTkButton(
                footer,
                text="Read more ↓",
                width=90, height=22,
                fg_color="transparent",
                text_color="#534AB7",
                hover_color="gray20",
                font=ctk.CTkFont(size=11),
            )
            expand_btn.configure(
                command=lambda t=topic, lbl=explanation_label, btn=expand_btn, exp=explanation:
                    self._toggle_expand(t, lbl, btn, exp)
            )
            expand_btn.pack(side="right")

        return card

    # ── Expand / collapse ─────────────────────────────────────────────────────

    def _toggle_expand(self, topic, label, btn, full_text):
        if topic["id"] in self.expanded_cards:
            self.expanded_cards.remove(topic["id"])
            label.configure(text=full_text[:180] + "...")
            btn.configure(text="Read more ↓")
        else:
            self.expanded_cards.add(topic["id"])
            label.configure(text=full_text)
            btn.configure(text="Show less ↑")

    # ── Delete ────────────────────────────────────────────────────────────────

    def _delete_topic(self, topic: dict):
        root = self.winfo_toplevel()
        confirm_delete(
            root,
            topic["topic"],
            on_confirm=lambda: self._do_delete(topic)
        )

    def _do_delete(self, topic: dict):
        delete_topic(topic["id"])
        self._all_cards = [
            (t, c) for t, c in self._all_cards
            if t["id"] != topic["id"]
        ]
        for t, c in self._all_cards:
            if t["id"] == topic["id"]:
                c.destroy()
        self._rebuild_sidebar()
        self._apply_filter(self.search_var.get().strip())

    # ── Refresh ───────────────────────────────────────────────────────────────

    def refresh(self):
        self._build_all_cards()
        self._rebuild_sidebar()
        self._apply_filter(self.search_var.get().strip())