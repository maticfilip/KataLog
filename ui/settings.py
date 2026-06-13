import customtkinter as ctk
import os
from tkinter import filedialog
from core.codewars_api import load_profile, fetch_all, disconnect
from core.kata_log import export_json, export_csv, KATA_FILE


class SettingsPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self._build_account()
        self._build_appearance()
        self._build_data()
        self._build_about()


    def _build_account(self):
        card = ctk.CTkFrame(self)
        card.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(
            card, text="CODEWARS ACCOUNT",
            font=ctk.CTkFont(size=11), text_color="gray60"
        ).pack(anchor="w", padx=14, pady=(12, 10))

        profile = load_profile()
        username = profile.get("username") if profile else None

        status_row = ctk.CTkFrame(card, fg_color="transparent")
        status_row.pack(fill="x", padx=14, pady=(0, 8))

        if username:
            ctk.CTkLabel(
                status_row,
                text=username,
                font=ctk.CTkFont(size=13, weight="bold")
            ).pack(side="left", padx=(0, 8))

            ctk.CTkLabel(
                status_row,
                text="  Connected  ",
                font=ctk.CTkFont(size=11),
                fg_color="#0A2E22", text_color="#5DCAA5",
                corner_radius=99
            ).pack(side="left")

            ctk.CTkButton(
                status_row, text="Sync",
                width=70, height=28,
                fg_color="transparent", border_width=1,
                text_color="gray60", border_color="gray30",
                command=self._sync
            ).pack(side="right", padx=(8, 0))

            ctk.CTkButton(
                status_row, text="Disconnect",
                width=90, height=28,
                fg_color="transparent", border_width=1,
                text_color="#E24B4A", border_color="#A32D2D",
                command=self._disconnect
            ).pack(side="right")

        else:
            ctk.CTkLabel(
                status_row, text="Not connected",
                font=ctk.CTkFont(size=13), text_color="gray50"
            ).pack(side="left")

        ctk.CTkFrame(card, height=1, fg_color="gray25").pack(fill="x", padx=14, pady=(4, 8))

        input_row = ctk.CTkFrame(card, fg_color="transparent")
        input_row.pack(fill="x", padx=14, pady=(0, 12))

        self.username_input = ctk.CTkEntry(
            input_row,
            placeholder_text="Codewars username",
            height=32
        )
        self.username_input.pack(side="left", fill="x", expand=True, padx=(0, 8))

        ctk.CTkButton(
            input_row, text="Connect",
            width=90, height=32,
            fg_color="#534AB7", hover_color="#3C3489",
            command=self._connect
        ).pack(side="left")

        self.status_label = ctk.CTkLabel(
            card, text="", font=ctk.CTkFont(size=11)
        )
        self.status_label.pack(anchor="w", padx=14, pady=(0, 8))


    def _build_appearance(self):
        card = ctk.CTkFrame(self)
        card.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(
            card, text="APPEARANCE",
            font=ctk.CTkFont(size=11), text_color="gray60"
        ).pack(anchor="w", padx=14, pady=(12, 10))

        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(fill="x", padx=14, pady=(0, 12))

        ctk.CTkLabel(
            row, text="Theme",
            font=ctk.CTkFont(size=13)
        ).pack(side="left")

        btn_frame = ctk.CTkFrame(row, fg_color="transparent")
        btn_frame.pack(side="right")

        ctk.CTkButton(
            btn_frame, text="Light",
            width=80, height=28,
            fg_color="transparent", border_width=1,
            text_color="gray60", border_color="gray30",
        ).pack(side="left", padx=(0, 6))

        ctk.CTkButton(
            btn_frame, text="Dark",
            width=80, height=28,
            fg_color="#534AB7", hover_color="#3C3489",
        ).pack(side="left")


    def _build_data(self):
        card = ctk.CTkFrame(self)
        card.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(
            card, text="DATA",
            font=ctk.CTkFont(size=11), text_color="gray60"
        ).pack(anchor="w", padx=14, pady=(12, 10))

        export_row = ctk.CTkFrame(card, fg_color="transparent")
        export_row.pack(fill="x", padx=14, pady=(0, 10))

        ctk.CTkLabel(
            export_row, text="Export kata log",
            font=ctk.CTkFont(size=13)
        ).pack(side="left")

        ctk.CTkLabel(
            export_row, text="Download your entries as a file",
            font=ctk.CTkFont(size=11), text_color="gray50"
        ).pack(side="left", padx=(8, 0))

        btn_frame = ctk.CTkFrame(export_row, fg_color="transparent")
        btn_frame.pack(side="right")

        ctk.CTkButton(
            btn_frame, text="JSON",
            width=70, height=28,
            fg_color="transparent", border_width=1,
            text_color="gray60", border_color="gray30",
            command=self._export_json
        ).pack(side="left", padx=(0, 6))

        ctk.CTkButton(
            btn_frame, text="CSV",
            width=70, height=28,
            fg_color="transparent", border_width=1,
            text_color="gray60", border_color="gray30",
            command=self._export_csv
        ).pack(side="left")

        ctk.CTkFrame(card, height=1, fg_color="gray25").pack(fill="x", padx=14, pady=(4, 8))

        # clear kata log row
        self._build_danger_row(
            card,
            title="Clear kata log",
            subtitle="Permanently delete all logged kata entries",
            btn_text="Clear all",
            command=self._clear_kata_log
        )

        ctk.CTkFrame(card, height=1, fg_color="gray25").pack(fill="x", padx=14, pady=(0, 8))

        self._build_danger_row(
            card,
            title="Clear Codewars cache",
            subtitle="Delete locally saved profile and completed kata data",
            btn_text="Clear",
            command=self._clear_cw_cache
        )

    def _build_danger_row(self, parent, title, subtitle, btn_text, command):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=14, pady=(0, 10))

        text_col = ctk.CTkFrame(row, fg_color="transparent")
        text_col.pack(side="left")

        ctk.CTkLabel(
            text_col, text=title,
            font=ctk.CTkFont(size=13)
        ).pack(anchor="w")

        ctk.CTkLabel(
            text_col, text=subtitle,
            font=ctk.CTkFont(size=11), text_color="gray50"
        ).pack(anchor="w")

        ctk.CTkButton(
            row, text=btn_text,
            width=90, height=28,
            fg_color="transparent", border_width=1,
            text_color="#E24B4A", border_color="#A32D2D",
            hover_color="#3D1515",
            command=command
        ).pack(side="right")


    def _build_about(self):
        card = ctk.CTkFrame(self)
        card.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(
            card, text="ABOUT",
            font=ctk.CTkFont(size=11), text_color="gray60"
        ).pack(anchor="w", padx=14, pady=(12, 10))

        rows = [
            ("App name",       "KataLog"),
            ("Version",        "0.1.0"),
            ("Built with",     "Python · CustomTkinter · LangChain"),
            ("Codewars API",   "dev.codewars.com"),
        ]

        for label, value in rows:
            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=14, pady=(0, 8))

            ctk.CTkLabel(
                row, text=label,
                font=ctk.CTkFont(size=12), text_color="gray50"
            ).pack(side="left")

            ctk.CTkLabel(
                row, text=value,
                font=ctk.CTkFont(size=12)
            ).pack(side="right")

        ctk.CTkFrame(card, height=1, fg_color="transparent").pack(pady=(0, 4))


    def _connect(self):
        username = self.username_input.get().strip()
        if not username:
            return
        self.status_label.configure(text="Connecting...", text_color="gray50")
        self.after(100, lambda: self._do_fetch(username))

    def _do_fetch(self, username: str):
        result = fetch_all(username)
        if "error" in result:
            self.status_label.configure(
                text=f"Error: {result['error']}", text_color="#E24B4A"
            )
            return
        self.status_label.configure(text="Connected!", text_color="#1D9E75")
        self.after(1000, self._rebuild)

    def _sync(self):
        profile = load_profile()
        if not profile:
            return
        username = profile.get("username")
        self.status_label.configure(text="Syncing...", text_color="gray50")
        self.after(100, lambda: self._do_fetch(username))

    def _disconnect(self):
        from ui.components import confirm_delete
        root = self.winfo_toplevel()
        confirm_delete(
            root,
            "your Codewars account",
            on_confirm=lambda: [disconnect(), self._rebuild()]
        )

    def _export_json(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            initialfile="kata_log.json"
        )
        if path:
            export_json(path)
            self.status_label.configure(
                text=f"Exported to {os.path.basename(path)}", text_color="#1D9E75"
            )

    def _export_csv(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile="kata_log.csv"
        )
        if path:
            export_csv(path)
            self.status_label.configure(
                text=f"Exported to {os.path.basename(path)}", text_color="#1D9E75"
            )

    def _clear_kata_log(self):
        from ui.components import confirm_delete
        root = self.winfo_toplevel()
        confirm_delete(
            root,
            "all kata log entries",
            on_confirm=self._do_clear_kata_log
        )

    def _do_clear_kata_log(self):
        if os.path.exists(KATA_FILE):
            os.remove(KATA_FILE)
        self.status_label.configure(
            text="Kata log cleared.", text_color="#E24B4A"
        )

    def _clear_cw_cache(self):
        from ui.components import confirm_delete
        root = self.winfo_toplevel()
        confirm_delete(
            root,
            "Codewars profile and cache",
            on_confirm=self._do_clear_cw_cache
        )

    def _do_clear_cw_cache(self):
        disconnect()
        self.status_label.configure(
            text="Codewars cache cleared.", text_color="#E24B4A"
        )

    def _rebuild(self):
        for widget in self.winfo_children():
            widget.destroy()
        self._build_account()
        self._build_appearance()
        self._build_data()
        self._build_about()