import customtkinter as ctk

STATUS_COLORS = {
    "Solved":   {"bar": "#1D9E75", "pill_bg": "#0A2E22", "pill_fg": "#5DCAA5"},
    "Struggled":{"bar": "#BA7517", "pill_bg": "#2E1E04", "pill_fg": "#EF9F27"},
    "Gave up":  {"bar": "#E24B4A", "pill_bg": "#3D1515", "pill_fg": "#F09595"},
    "Learning": {"bar": "#534AB7", "pill_bg": "#2A2660", "pill_fg": "#AFA9EC"},
}

DIFF_COLORS = {
    "8kyu": "#7A7A7A", "7kyu": "#B0B0B0",
    "6kyu": "#C97D00", "5kyu": "#F0A500",
    "4kyu": "#2A5F9E", "3kyu": "#3C7EBB",
    "2kyu":"#6A3FA0", "1kyu":"#865FC0"
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

    if entry.get("description"):
        ctk.CTkLabel(
            content, text="Description",
            font=ctk.CTkFont(size=11), text_color="gray50"
        ).pack(anchor="w", pady=(6, 2))
        ctk.CTkLabel(
            content, text=entry["description"],
            font=ctk.CTkFont(size=12), text_color="gray60",
            wraplength=520, justify="left",
        ).pack(anchor="w")

    if entry.get("notes"):
        ctk.CTkLabel(
            content, text=entry["notes"],
            font=ctk.CTkFont(size=13), text_color=diff_color,
            wraplength=520, justify="left",
        ).pack(anchor="w", pady=(4, 0))

    if entry.get("code"):
        ctk.CTkLabel(
            content, text="Solution",
            font=ctk.CTkFont(size=11), text_color="gray50"
        ).pack(anchor="w", pady=(6, 2))
        ctk.CTkTextbox(
            content, height=80, corner_radius=6,
            font=ctk.CTkFont(family="Courier", size=12),
            fg_color="gray12", text_color="#5DCAA5",
            state="normal"
        )._textbox.configure(wrap="none")
        code_box = ctk.CTkTextbox(
            content, height=80, corner_radius=6,
            font=ctk.CTkFont(family="Courier", size=12),
            fg_color="gray12", text_color="#5DCAA5",
        )
        code_box.pack(fill="x", pady=(0, 4))
        code_box.insert("1.0", entry["code"])
        code_box.configure(state="disabled")

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