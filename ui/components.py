import customtkinter as ctk

STATUS_COLORS = {
    "Solved":   {"bar": "#1D9E75", "pill_bg": "#0A2E22", "pill_fg": "#5DCAA5"},
    "Struggled":{"bar": "#BA7517", "pill_bg": "#2E1E04", "pill_fg": "#EF9F27"},
    "Gave up":  {"bar": "#E24B4A", "pill_bg": "#3D1515", "pill_fg": "#F09595"},
    "Learning": {"bar": "#534AB7", "pill_bg": "#2A2660", "pill_fg": "#AFA9EC"},
}

DIFF_COLORS = {
    "8kyu": "#888888", "7kyu": "#888888",
    "6kyu": "#EF9F27", "5kyu": "#EF9F27",
    "4kyu": "#5DCAA5", "3kyu+": "#AFA9EC",
}

def build_entry_row(parent, entry: dict):
    colors = STATUS_COLORS.get(entry["status"], STATUS_COLORS["Learning"])
    diff_color = DIFF_COLORS.get(entry["difficulty"], "gray50")

    row = ctk.CTkFrame(parent, corner_radius=8, fg_color="gray17")
    row.pack(fill="x", pady=(0, 6))

    accent = ctk.CTkFrame(row, width=3, corner_radius=0, fg_color=colors["bar"])
    accent.pack(side="left", fill="y")
    accent.pack_propagate(False)

    content = ctk.CTkFrame(row, fg_color="transparent")
    content.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    top = ctk.CTkFrame(content, fg_color="transparent")
    top.pack(fill="x", anchor="w")

    ctk.CTkLabel(
        top, text=entry["kata_name"],
        font=ctk.CTkFont(size=14, weight="bold"),
    ).pack(side="left", padx=(0, 8))

    ctk.CTkLabel(
        top, text=f" {entry['difficulty']} ",
        font=ctk.CTkFont(size=11),
        fg_color="gray25", text_color=diff_color,
        corner_radius=4,
    ).pack(side="left", padx=(0, 6))

    ctk.CTkLabel(
        top, text=f"  {entry['status']}  ",
        font=ctk.CTkFont(size=11),
        fg_color=colors["pill_bg"], text_color=colors["pill_fg"],
        corner_radius=99,
    ).pack(side="left", padx=(0, 6))


    ctk.CTkLabel(
        top, text=entry["timestamp"][11:16],
        font=ctk.CTkFont(size=11), text_color="gray50",
    ).pack(side="right")

    menu_frame=ctk.CTkFrame(top, fg_color="gray25", corner_radius=6)
    dots_btn=ctk.CTkButton(
        top, text="•••",width=28, height=22, fg_color="transparent",
        hover_color="gray30",text_color="gray50", font=ctk.CTkFont(size=12),
        corner_radius=4, command=lambda:toggle_menu(row, menu_frame,entry)
    )
    dots_btn.pack(side="right")

    if entry.get("notes"):
        ctk.CTkLabel(
            content, text=entry["notes"],
            font=ctk.CTkFont(size=13), text_color="gray70",
            wraplength=520, justify="left",
        ).pack(anchor="w", pady=(4, 0))

    def toggle_menu(row, menu_frame, entry):
        if menu_frame.winfo_ismapped():
            menu_frame.pack_forget()
            return
        
        for widget in menu_frame.winfo_children():
            widget.destroy()

        options = [
            ("📋  Copy kata name"),
            ("🗑  Delete entry"),
        ]

        for label, command in options:
            ctk.CTkButton(
                menu_frame,
                text=label,
                anchor="w",
                fg_color="transparent",
                hover_color="gray30",
                text_color="gray70",
                height=30,
                corner_radius=4,
                command=command
            ).pack(fill="x", padx=4, pady=2)

        menu_frame.pack(fill="x", padx=10, pady=(0, 8))

    def menu_frame_close(row):
        for widget in row.winfo_children():
            if isinstance(widget, ctk.CTkFrame) and widget.cget("fg_color")=="gray25":
                widget.pack_forget()