import customtkinter as ctk
from datetime import datetime
from core.theory import (
    get_topics, get_topics_by_category,
    get_category_counts, delete_topic,
    search_topics, CATEGORIES
)
from ui.components import confirm_delete

CATEGORY_COLORS = {
    "Algorithms":         {"bg": "#2A2660", "fg": "#AFA9EC"},
    "Data Structures":    {"bg": "#0A2E22", "fg": "#5DCAA5"},
    "String Manipulation":{"bg": "#2E1E04", "fg": "#EF9F27"},
    "Mathematics":        {"bg": "#3D1515", "fg": "#F09595"},
    "Language Features":  {"bg": "#0A1F3D", "fg": "#85B7EB"},
    "Other":              {"bg": "#222222", "fg": "#888888"},
}


class TheoryPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.selected_category = None  # None means "All"
        self.expanded_cards = set()    # track which cards are expanded

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
        query = self.search_var.get().strip()
        if query:
            topics = search_topics(query)
        else:
            topics = self._get_current_topics()
        self._rebuild_feed(topics)

    # ── Body (sidebar + feed) ─────────────────────────────────────────────────

    def _build_body(self):
        self.body_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.body_frame.pack(fill="both", expand=True)
        self.body_frame.grid_columnconfigure(1, weight=1)
        self.body_frame.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_feed_area()
        self._rebuild_feed(get_topics())

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

        self._build_cat_btn("All topics", total, None)

        for cat in CATEGORIES:
            self._build_cat_btn(cat, counts.get(cat, 0), cat)

    def _build_cat_btn(self, label: str, count: int, category):
        is_active = self.selected_category == category

        row = ctk.CTkFrame(
            self.sidebar,
            fg_color="#2A2660" if is_active else "transparent",
            corner_radius=6
        )
        row.pack(fill="x", pady=2)

        ctk.CTkLabel(
            row, text=label,
            font=ctk.CTkFont(size=13, weight="bold" if is_active else "normal"),
            text_color="#AFA9EC" if is_active else "gray60",
            anchor="w"
        ).pack(side="left", padx=10, pady=8)

        ctk.CTkLabel(
            row,
            text=str(count),
            font=ctk.CTkFont(size=11),
            fg_color="#534AB7" if is_active else "gray25",
            text_color="#EEEDFE" if is_active else "gray50",
            corner_radius=99,
            width=24
        ).pack(side="right", padx=8)

        row.bind("<Button-1>", lambda e, c=category: self._select_category(c))
        for child in row.winfo_children():
            child.bind("<Button-1>", lambda e, c=category: self._select_category(c))

    def _select_category(self, category):
        self.selected_category = category
        self._rebuild_sidebar()
        self._rebuild_feed(self._get_current_topics())

    def _get_current_topics(self) -> list:
        if self.selected_category is None:
            return get_topics()
        return get_topics_by_category(self.selected_category)

    # ── Feed ──────────────────────────────────────────────────────────────────

    def _build_feed_area(self):
        self.feed_frame = ctk.CTkFrame(
            self.body_frame, fg_color="transparent"
        )
        self.feed_frame.grid(row=0, column=1, sticky="nsew")

    def _rebuild_feed(self, topics: list):
        for widget in self.feed_frame.winfo_children():
            widget.destroy()

        if not topics:
            ctk.CTkLabel(
                self.feed_frame,
                text="No topics saved yet.\nGet an AI explanation from any kata entry to start building your library.",
                text_color="gray50",
                font=ctk.CTkFont(size=13),
                justify="center"
            ).pack(pady=40)
            return

        for topic in topics:
            self._build_topic_card(topic)

    def _build_topic_card(self, topic: dict):
        colors = CATEGORY_COLORS.get(topic["category"], CATEGORY_COLORS["Other"])
        is_expanded = topic["id"] in self.expanded_cards

        card = ctk.CTkFrame(self.feed_frame, corner_radius=10, fg_color="gray17")
        card.pack(fill="x", pady=(0, 8))

        # ── header ────────────────────────────────────────────────────────────
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=14, pady=(12, 8))

        ctk.CTkLabel(
            header,
            text=topic["topic"],
            font=ctk.CTkFont(size=14, weight="bold"),
        ).pack(side="left", padx=(0, 8))

        ctk.CTkLabel(
            header,
            text=f"  {topic['category']}  ",
            font=ctk.CTkFont(size=11),
            fg_color=colors["bg"],
            text_color=colors["fg"],
            corner_radius=99,
        ).pack(side="left")

        # delete button
        ctk.CTkButton(
            header,
            text="✕",
            width=24, height=24,
            fg_color="transparent",
            hover_color="gray25",
            text_color="gray50",
            font=ctk.CTkFont(size=11),
            command=lambda t=topic: self._delete_topic(t)
        ).pack(side="right")

        # timestamp
        day_date = datetime.strptime(topic["timestamp"][:10], "%Y-%m-%d").date()
        from datetime import date
        delta = (date.today() - day_date).days
        if delta == 0:
            time_str = "Today"
        elif delta == 1:
            time_str = "Yesterday"
        else:
            time_str = f"{delta} days ago"

        ctk.CTkLabel(
            header,
            text=time_str,
            font=ctk.CTkFont(size=11),
            text_color="gray50"
        ).pack(side="right", padx=(0, 8))

        # ── explanation ───────────────────────────────────────────────────────
        explanation = topic.get("explanation", "")
        preview = explanation[:180] + "..." if len(explanation) > 180 and not is_expanded else explanation

        explanation_label = ctk.CTkLabel(
            card,
            text=preview,
            font=ctk.CTkFont(size=13),
            text_color="gray70",
            wraplength=460,
            justify="left",
            anchor="w"
        )
        explanation_label.pack(anchor="w", padx=14, pady=(0, 8))

        # ── footer ────────────────────────────────────────────────────────────
        footer = ctk.CTkFrame(card, fg_color="gray14", corner_radius=0)
        footer.pack(fill="x")

        if topic.get("related_kata"):
            ctk.CTkLabel(
                footer,
                text=f"from kata:  {topic['related_kata']}",
                font=ctk.CTkFont(size=11),
                text_color="#534AB7"
            ).pack(side="left", padx=12, pady=8)

        if len(explanation) > 180:
            btn_text = "Show less ↑" if is_expanded else "Read more ↓"
            ctk.CTkButton(
                footer,
                text=btn_text,
                width=100, height=26,
                fg_color="transparent",
                text_color="#534AB7",
                hover_color="gray20",
                font=ctk.CTkFont(size=11),
                command=lambda t=topic: self._toggle_expand(t)
            ).pack(side="right", padx=8, pady=6)

    def _toggle_expand(self, topic: dict):
        if topic["id"] in self.expanded_cards:
            self.expanded_cards.remove(topic["id"])
        else:
            self.expanded_cards.add(topic["id"])
        self._rebuild_feed(self._get_current_topics())

    def _delete_topic(self, topic: dict):
        root = self.winfo_toplevel()
        confirm_delete(
            root,
            topic["topic"],
            on_confirm=lambda: [delete_topic(topic["id"]), self.refresh()]
        )

    # ── Refresh ───────────────────────────────────────────────────────────────

    def refresh(self):
        self._rebuild_sidebar()
        self._rebuild_feed(self._get_current_topics())