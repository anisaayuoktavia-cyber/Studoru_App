import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as tb
import winsound
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Persistence
STATS_FILE = "studoru_stats.json"
SCHEDULE_FILE = "studoru_schedule.json"

def load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default
    return default

def save_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

class StudoruApp:
    def __init__(self):
        # Light aesthetic theme only
        self.style = tb.Style(theme="litera")
        self.root = self.style.master
        self.root.title("STUDORU")
        self.root.geometry("1280x880")
        self.root.minsize(1100, 780)

        # Coquette palette (two pinks)
        self.accent_color = "#ff8fb3"   # light pink
        self.primary_color = "#d63384"  # dark pink

        # Bilingual texts (EN/ID) with emoji additions
        self.texts = {
            "EN": {
                "language_label": "Language",
                "settings_title": "🎀 Settings",
                "unit": "Time unit",
                "study": "Study",
                "break": "Break",
                "target": "Daily target (minutes)",
                "ready": "🎀 Ready to start! 💖",
                "start": "▶ Start 🎀",
                "pause": "⏸️ Pause 🎀",
                "resume": "⏯️ Resume 🎀",
                "stop": "■ Stop 🎀",
                "reset": "🔄 Reset 🎀",
                "schedule_title": "🎀 Study schedule",
                "session_name": "Session name",
                "study_number": "Study (number)",
                "break_number": "Break (number)",
                "session_list": "Session list",
                "add_session": "➕ Add session 🎀",
                "use_session": "🎯 Use session 🎀",
                "delete_session": "🗑️ Delete session 🎀",
                "analytics_title": "📈 Daily study analytics 🎀",
                "target_title": "🎯 Daily target 🎀",
                "target_label_suffix": "minutes",
                "unit_ready": "🎀 Unit mode: {unit}. Ready! 💖",
                "session_added": "Session added 🎀",
                "session_saved_msg": "Session '{name}' saved!",
                "schedule_pick_first": "Please select a session from the list first.",
                "schedule_not_found": "Session not found.",
                "schedule_title_box": "Schedule 🎀",
                "schedule_deleted_msg": "Session '{name}' deleted!",
                "error_title": "Error",
                "error_durations": "Enter valid numbers for durations & target!",
                "error_session_durations": "Enter valid numbers for session durations!",
                "error_session_name": "Session name cannot be empty!",
                "focus_started": "🎀 Focus mode started! Keep going! 💖",
                "paused": "⏸️ Paused. Gentle breath 🎀",
                "resumed": "⏯️ Resumed. You’ve got this! 💖",
                "stopped": "■ Timer stopped 🎀",
                "reset_text": "🔄 Reset. Fresh start, shining star! 🎀",
                "break_time": "☕ Break time! Rest softly 🎀",
                "back_to_focus": "💻 Back to focus. Bloom again! 🎀",
                "msg_study_done_title": "Great job!",
                "msg_study_done_text": "Take a break!",
                "msg_break_done_title": "Break finished!",
                "msg_break_done_text": "Back to work!",
                "no_sessions_chart": "No sessions today yet 🎀",
                "chart_title": "Study duration per session (minutes) 🎀",
                "chart_xlabel": "Session #",
                "chart_ylabel": "Minutes",
                "motivation_after_study": "You did amazing — small steps create big wins! 💖",
                "motivation_after_break": "Focus gently — your future self will thank you! 💖",
                "session_applied": "🎀 Session applied. Ready to bloom! 💖",
                "emoji_marker": "🎀",
            },
            "ID": {
                "language_label": "Bahasa",
                "settings_title": "🎀 Pengaturan",
                "unit": "Unit waktu",
                "study": "Belajar",
                "break": "Istirahat",
                "target": "Target harian (menit)",
                "ready": "🎀 Siap mulai! 💖",
                "start": "▶ Mulai 🎀",
                "pause": "⏸️ Jeda 🎀",
                "resume": "⏯️ Lanjut 🎀",
                "stop": "■ Berhenti 🎀",
                "reset": "🔄 Reset 🎀",
                "schedule_title": "🎀 Jadwal belajar",
                "session_name": "Nama sesi",
                "study_number": "Belajar (angka)",
                "break_number": "Istirahat (angka)",
                "session_list": "Daftar sesi",
                "add_session": "➕ Tambah sesi 🎀",
                "use_session": "🎯 Pakai sesi 🎀",
                "delete_session": "🗑️ Hapus sesi 🎀",
                "analytics_title": "📈 Analisis belajar harian 🎀",
                "target_title": "🎯 Target harian 🎀",
                "target_label_suffix": "menit",
                "unit_ready": "🎀 Mode unit: {unit}. Siap! 💖",
                "session_added": "Sesi ditambahkan 🎀",
                "session_saved_msg": "Sesi '{name}' disimpan!",
                "schedule_pick_first": "Pilih sesi dari daftar terlebih dahulu.",
                "schedule_not_found": "Sesi tidak ditemukan.",
                "schedule_title_box": "Jadwal 🎀",
                "schedule_deleted_msg": "Sesi '{name}' dihapus!",
                "error_title": "Error",
                "error_durations": "Masukkan angka valid untuk durasi & target!",
                "error_session_durations": "Masukkan angka valid untuk durasi sesi!",
                "error_session_name": "Nama sesi tidak boleh kosong!",
                "focus_started": "🎀 Mode fokus dimulai! Tetap semangat! 💖",
                "paused": "⏸️ Dijeda. Tarik napas lembut 🎀",
                "resumed": "⏯️ Dilanjutkan. Kamu pasti bisa! 💖",
                "stopped": "■ Timer berhenti 🎀",
                "reset_text": "🔄 Reset. Awal baru yang berkilau! 🎀",
                "break_time": "☕ Waktu istirahat! Rehat lembut 🎀",
                "back_to_focus": "💻 Kembali fokus. Mekar lagi! 🎀",
                "msg_study_done_title": "Kerja bagus!",
                "msg_study_done_text": "Istirahat dulu!",
                "msg_break_done_title": "Istirahat selesai!",
                "msg_break_done_text": "Kembali belajar!",
                "no_sessions_chart": "Belum ada sesi hari ini 🎀",
                "chart_title": "Durasi belajar per sesi (menit) 🎀",
                "chart_xlabel": "Sesi ke-",
                "chart_ylabel": "Menit",
                "motivation_after_study": "Kamu hebat — langkah kecil menciptakan kemenangan besar! 💖",
                "motivation_after_break": "Fokus lembut — dirimu di masa depan akan berterima kasih! 💖",
                "session_applied": "🎀 Sesi diterapkan. Siap mekar! 💖",
                "emoji_marker": "🎀",
            }
        }
        self.language = "EN"
        T = self.texts[self.language]

        # Top bar: title + language selector
        topbar = tb.Frame(self.root)
        topbar.pack(fill="x", padx=12, pady=8)
        self.title_label = tb.Label(topbar, text="STUDORU 🎀", font=("Comic Sans MS", 36, "bold"),
                                    foreground=self.primary_color)
        self.title_label.pack(side="left")
        lang_box = tb.Frame(topbar)
        lang_box.pack(side="right")
        self.language_label = tb.Label(lang_box, text=T["language_label"])
        self.language_label.pack(side="left", padx=6)
        self.combo_lang = tb.Combobox(lang_box, width=12, values=["EN", "ID"], state="readonly")
        self.combo_lang.set(self.language)
        self.combo_lang.pack(side="left")
        self.combo_lang.bind("<<ComboboxSelected>>", self.on_language_change)

        # Main layout
        container = tb.Frame(self.root)
        container.pack(padx=14, pady=10, fill="both", expand=True)
        container.columnconfigure(0, weight=3)
        container.columnconfigure(1, weight=2)

        left = tb.Frame(container)
        left.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        right = tb.Frame(container)
        right.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Emoji-only headers
        self.settings_header = tb.Label(left, text=T["settings_title"], font=("Comic Sans MS", 16, "bold"),
                                        foreground=self.primary_color)
        self.settings_header.pack(anchor="w", pady=(2, 4))

        # Settings fields
        settings = tb.Frame(left)
        settings.pack(fill="x", pady=4)
        self.label_unit = tb.Label(settings, text=T["unit"])
        self.label_unit.grid(row=0, column=0, padx=6, pady=6, sticky="e")
        self.combo_global_unit = tb.Combobox(settings, width=10, values=["minutes", "seconds"], state="readonly")
        self.combo_global_unit.set("minutes")
        self.combo_global_unit.grid(row=0, column=1, padx=4, pady=6)
        self.combo_global_unit.bind("<<ComboboxSelected>>", self.on_unit_change)

        self.label_study = tb.Label(settings, text=T["study"])
        self.label_study.grid(row=0, column=2, padx=6, pady=6, sticky="e")
        self.entry_work = tb.Entry(settings, width=10)
        self.entry_work.insert(0, "25")
        self.entry_work.grid(row=0, column=3, padx=4, pady=6)

        self.label_break = tb.Label(settings, text=T["break"])
        self.label_break.grid(row=0, column=4, padx=6, pady=6, sticky="e")
        self.entry_break = tb.Entry(settings, width=10)
        self.entry_break.insert(0, "5")
        self.entry_break.grid(row=0, column=5, padx=4, pady=6)

        self.label_target = tb.Label(settings, text=T["target"])
        self.label_target.grid(row=0, column=6, padx=6, pady=6, sticky="e")
        self.entry_target = tb.Entry(settings, width=10)
        self.entry_target.insert(0, "120")
        self.entry_target.grid(row=0, column=7, padx=4, pady=6)

        # Timer
        self.timer_label = tb.Label(left, text="25:00", font=("Comic Sans MS", 64, "bold"),
                                    foreground=self.primary_color)
        self.timer_label.pack(pady=8)

        self.progress = tb.Progressbar(left, orient="horizontal", length=960, mode="determinate",
                                       bootstyle="danger-striped")
        self.progress.pack(pady=10)

        self.status_label = tb.Label(left, text=T["ready"], font=("Comic Sans MS", 18),
                                     foreground=self.accent_color)
        self.status_label.pack(pady=6)

        # Controls
        buttons = tb.Frame(left)
        buttons.pack(pady=12)
        self.start_btn  = tb.Button(buttons, text=T["start"],  bootstyle="success",   command=self.start_timer)
        self.pause_btn  = tb.Button(buttons, text=T["pause"],  bootstyle="secondary", command=self.pause_timer,  state=tk.DISABLED)
        self.resume_btn = tb.Button(buttons, text=T["resume"], bootstyle="info",      command=self.resume_timer, state=tk.DISABLED)
        self.stop_btn   = tb.Button(buttons, text=T["stop"],   bootstyle="danger",    command=self.stop_timer,   state=tk.DISABLED)
        self.reset_btn  = tb.Button(buttons, text=T["reset"],  bootstyle="warning",   command=self.reset_timer)
        for i, btn in enumerate([self.start_btn, self.pause_btn, self.resume_btn, self.stop_btn, self.reset_btn]):
            btn.grid(row=0, column=i, padx=8)

        # Schedule header
        self.schedule_header = tb.Label(left, text=T["schedule_title"], font=("Comic Sans MS", 16, "bold"),
                                        foreground=self.primary_color)
        self.schedule_header.pack(anchor="w", pady=(8, 4))

        # Study schedule fields
        schedule_box = tb.Frame(left)
        schedule_box.pack(fill="x", pady=4)

        self.label_session_name = tb.Label(schedule_box, text=T["session_name"])
        self.label_session_name.grid(row=0, column=0, padx=6, pady=4, sticky="w")
        self.entry_session_name = tb.Entry(schedule_box, width=28)
        self.entry_session_name.grid(row=0, column=1, padx=6, pady=4, sticky="w")

        self.label_session_work = tb.Label(schedule_box, text=T["study_number"])
        self.label_session_work.grid(row=1, column=0, padx=6, pady=4, sticky="w")
        self.entry_session_work = tb.Entry(schedule_box, width=12)
        self.entry_session_work.insert(0, "50")
        self.entry_session_work.grid(row=1, column=1, padx=6, pady=4, sticky="w")

        self.label_session_break = tb.Label(schedule_box, text=T["break_number"])
        self.label_session_break.grid(row=2, column=0, padx=6, pady=4, sticky="w")
        self.entry_session_break = tb.Entry(schedule_box, width=12)
        self.entry_session_break.insert(0, "10")
        self.entry_session_break.grid(row=2, column=1, padx=6, pady=4, sticky="w")

        self.add_session_btn    = tb.Button(schedule_box, text=T["add_session"],   bootstyle="success",  command=self.add_schedule_item)
        self.apply_session_btn  = tb.Button(schedule_box, text=T["use_session"],   bootstyle="info",     command=self.apply_selected_session)
        self.delete_session_btn = tb.Button(schedule_box, text=T["delete_session"],bootstyle="danger",   command=self.delete_selected_session)
        self.add_session_btn.grid(row=0, column=2, rowspan=3, padx=10, pady=4)

        self.label_session_list = tb.Label(schedule_box, text=T["session_list"])
        self.label_session_list.grid(row=3, column=0, padx=6, pady=4, sticky="w")
        self.schedule_combo = tb.Combobox(schedule_box, width=48, state="readonly")
        self.schedule_combo.grid(row=3, column=1, padx=6, pady=4, sticky="w")
        self.apply_session_btn.grid(row=3, column=2, padx=6, pady=4)
        self.delete_session_btn.grid(row=3, column=3, padx=6, pady=4)

        # Analytics header
        self.analytics_header = tb.Label(right, text=T["analytics_title"], font=("Comic Sans MS", 16, "bold"),
                                         foreground=self.primary_color)
        self.analytics_header.pack(anchor="w", pady=(2, 4))

        # Analytics (line chart)
        analytics_box = tb.Frame(right)
        analytics_box.pack(pady=6, padx=6, fill="both", expand=True)

        self.fig = plt.figure(figsize=(7.2, 4.2), dpi=110, constrained_layout=True)
        self.ax = self.fig.add_subplot(111)
        self.chart_canvas = FigureCanvasTkAgg(self.fig, master=analytics_box)
        self.chart_canvas.get_tk_widget().grid(row=0, column=0, padx=8, pady=8, sticky="nsew")
        analytics_box.rowconfigure(0, weight=1)
        analytics_box.columnconfigure(0, weight=1)

        # Target header
        self.target_header = tb.Label(right, text=T["target_title"], font=("Comic Sans MS", 16, "bold"),
                                      foreground=self.primary_color)
        self.target_header.pack(anchor="w", pady=(8, 4))

        target_box = tb.Frame(right)
        target_box.pack(pady=6, padx=6, fill="x")
        self.target_progress = tb.Progressbar(target_box, orient="horizontal", length=420, mode="determinate",
                                              bootstyle="warning-striped")
        self.target_progress.grid(row=0, column=0, padx=8, pady=8)
        self.target_label = tb.Label(target_box, text=f"0 / 120 {T['target_label_suffix']}",
                                     font=("Comic Sans MS", 13), foreground=self.primary_color)
        self.target_label.grid(row=1, column=0, padx=8, pady=2, sticky="w")

        # State & persistence
        self.is_running = False
        self.is_work_time = True
        self.work_remaining = 25 * 60
        self.break_remaining = 5 * 60
        self.session_active_seconds = 0

        self.stats = load_json(STATS_FILE, {})
        self.today_key = datetime.now().strftime("%Y-%m-%d")
        if self.today_key not in self.stats:
            self.stats[self.today_key] = {"total_focus_sec": 0, "sessions": 0, "longest_sec": 0, "details": []}

        self.schedule = load_json(SCHEDULE_FILE, [])
        self.refresh_schedule_combo()

        self.progress["maximum"] = self.work_remaining
        self.progress["value"] = self.work_remaining
        self.update_timer_label()

        # Chart styling and initial draw (with layout fixes + emoji markers)
        self.apply_chart_style()
        self.refresh_line_chart()

    # Language switch
    def on_language_change(self, _event=None):
        self.language = self.combo_lang.get()
        self.apply_language()

    def apply_language(self):
        T = self.texts[self.language]
        # Top bar
        self.language_label.config(text=T["language_label"])
        # Headers
        self.settings_header.config(text=T["settings_title"])
        self.schedule_header.config(text=T["schedule_title"])
        self.analytics_header.config(text=T["analytics_title"])
        self.target_header.config(text=T["target_title"])
        # Settings fields
        self.label_unit.config(text=T["unit"])
        self.label_study.config(text=T["study"])
        self.label_break.config(text=T["break"])
        self.label_target.config(text=T["target"])
        # Status and buttons
        self.status_label.config(text=T["ready"])
        self.start_btn.config(text=T["start"])
        self.pause_btn.config(text=T["pause"])
        self.resume_btn.config(text=T["resume"])
        self.stop_btn.config(text=T["stop"])
        self.reset_btn.config(text=T["reset"])
        # Schedule labels
        self.label_session_name.config(text=T["session_name"])
        self.label_session_work.config(text=T["study_number"])
        self.label_session_break.config(text=T["break_number"])
        self.label_session_list.config(text=T["session_list"])
        self.add_session_btn.config(text=T["add_session"])
        self.apply_session_btn.config(text=T["use_session"])
        self.delete_session_btn.config(text=T["delete_session"])
        # Target label
        total_minutes_today = self.stats[self.today_key]["total_focus_sec"] // 60
        try:
            target_minutes = int(self.entry_target.get())
        except ValueError:
            target_minutes = 120
        self.target_label.config(text=f"{total_minutes_today} / {target_minutes} {T['target_label_suffix']}")
        # Chart localization
        self.apply_chart_style()
        self.refresh_line_chart()

    # Unit change info
    def on_unit_change(self, _event=None):
        T = self.texts[self.language]
        unit = self.combo_global_unit.get()
        self.status_label.config(text=T["unit_ready"].format(unit=unit))

    # Helpers
    def beep(self, freq=1200, ms=400):
        try:
            winsound.Beep(freq, ms)
        except Exception:
            pass

    def to_seconds(self, value_str):
        val = int(value_str)
        unit = self.combo_global_unit.get()
        return val if unit == "seconds" else val * 60

    def fmt_mmss(self, seconds):
        m = seconds // 60
        s = seconds % 60
        return f"{m:02d}:{s:02d}"

    def update_timer_label(self):
        current = self.work_remaining if self.is_work_time else self.break_remaining
        self.timer_label.config(text=self.fmt_mmss(current))

    # Schedule
    def refresh_schedule_combo(self):
        items = [f'{item["name"]} (Study {item["work"]}, Break {item["break"]})' for item in self.schedule]
        self.schedule_combo["values"] = items
        if items:
            self.schedule_combo.current(0)

    def add_schedule_item(self):
        T = self.texts[self.language]
        name = self.entry_session_name.get().strip()
        try:
            work_v = int(self.entry_session_work.get())
            break_v = int(self.entry_session_break.get())
        except ValueError:
            messagebox.showerror(T["error_title"], T["error_session_durations"])
            return
        if not name:
            messagebox.showerror(T["error_title"], T["error_session_name"])
            return
        self.schedule.append({"name": name, "work": work_v, "break": break_v})
        save_json(SCHEDULE_FILE, self.schedule)
        self.refresh_schedule_combo()
        messagebox.showinfo(T["session_added"], T["session_saved_msg"].format(name=name))

    def apply_selected_session(self):
        T = self.texts[self.language]
        sel = self.schedule_combo.get()
        if not sel:
            messagebox.showwarning(T["schedule_title"], T["schedule_pick_first"])
            return
        name_key = sel.split(" (")[0]
        item = next((x for x in self.schedule if x["name"] == name_key), None)
        if not item:
            messagebox.showwarning(T["schedule_title"], T["schedule_not_found"])
            return
        self.entry_work.delete(0, tk.END)
        self.entry_work.insert(0, str(item["work"]))
        self.entry_break.delete(0, tk.END)
        self.entry_break.insert(0, str(item["break"]))
        try:
            self.work_remaining = self.to_seconds(self.entry_work.get())
        except ValueError:
            self.work_remaining = 25 * 60
        self.is_work_time = True
        self.progress["maximum"] = self.work_remaining
        self.progress["value"] = self.work_remaining
        self.update_timer_label()
        self.status_label.config(text=T["session_applied"])

    def delete_selected_session(self):
        T = self.texts[self.language]
        sel = self.schedule_combo.get()
        if not sel:
            messagebox.showwarning(T["schedule_title"], T["schedule_pick_first"])
            return
        name_key = sel.split(" (")[0]
        idx = next((i for i, x in enumerate(self.schedule) if x["name"] == name_key), None)
        if idx is None:
            messagebox.showwarning(T["schedule_title"], T["schedule_not_found"])
            return
        removed = self.schedule.pop(idx)
        save_json(SCHEDULE_FILE, self.schedule)
        self.refresh_schedule_combo()
        messagebox.showinfo(T["schedule_title"], T["schedule_deleted_msg"].format(name=removed["name"]))

    # Controls
    def start_timer(self):
        T = self.texts[self.language]
        try:
            work_seconds   = self.to_seconds(self.entry_work.get())
            break_seconds  = self.to_seconds(self.entry_break.get())
            target_minutes = int(self.entry_target.get())
        except ValueError:
            messagebox.showerror(T["error_title"], T["error_durations"])
            return

        # Initialize from configured values
        self.work_remaining = max(1, work_seconds)
        self.break_remaining = max(1, break_seconds)
        self.is_work_time = True
        self.session_active_seconds = 0

        # Progress setup
        self.progress["maximum"] = self.work_remaining
        self.progress["value"] = self.work_remaining
        self.update_timer_label()

        # Target bar
        self.target_progress["maximum"] = max(1, target_minutes)
        self.update_target_label()

        # Start loop
        self.is_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.pause_btn.config(state=tk.NORMAL)
        self.resume_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_label.config(text=T["focus_started"])
        self.tick()

    def pause_timer(self):
        T = self.texts[self.language]
        if self.is_running:
            self.is_running = False
            self.pause_btn.config(state=tk.DISABLED)
            self.resume_btn.config(state=tk.NORMAL)
            self.status_label.config(text=T["paused"])

    def resume_timer(self):
        T = self.texts[self.language]
        if not self.is_running:
            self.is_running = True
            self.pause_btn.config(state=tk.NORMAL)
            self.resume_btn.config(state=tk.DISABLED)
            self.status_label.config(text=T["resumed"])
            self.tick()

    def stop_timer(self):
        T = self.texts[self.language]
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
        self.resume_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_label.config(text=T["stopped"])

    def reset_timer(self):
        T = self.texts[self.language]
        self.is_running = False
        self.is_work_time = True
        try:
            self.work_remaining = self.to_seconds(self.entry_work.get())
        except ValueError:
            self.work_remaining = 25 * 60
        self.progress["maximum"] = self.work_remaining
        self.progress["value"] = self.work_remaining
        self.update_timer_label()
        self.start_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
        self.resume_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_label.config(text=T["reset_text"])

    # Timer loop with robust phase transition (fixes 00:01 stuck) and messageboxes
    def tick(self):
        T = self.texts[self.language]
        if not self.is_running:
            return

        if self.is_work_time:
            # Decrement and clamp
            self.work_remaining = max(0, self.work_remaining - 1)
            # Sync progress bar to configured max
            try:
                cfg_work = max(1, self.to_seconds(self.entry_work.get()))
            except ValueError:
                cfg_work = self.progress["maximum"]
            self.progress["maximum"] = cfg_work
            self.progress["value"] = self.work_remaining
            self.session_active_seconds += 1

            # Transition when time <= 0 (prevents 00:01 stuck)
            if self.work_remaining <= 0:
                self.beep()
                # Record the completed study session
                self.record_focus_session(self.session_active_seconds)
                self.session_active_seconds = 0

                # Prepare break phase from current config
                try:
                    self.break_remaining = max(1, self.to_seconds(self.entry_break.get()))
                except ValueError:
                    self.break_remaining = 5 * 60
                self.is_work_time = False

                # Update progress for break phase
                self.progress["maximum"] = self.break_remaining
                self.progress["value"] = self.break_remaining

                # Notify and motivate
                messagebox.showinfo(T["msg_study_done_title"], T["msg_study_done_text"])
                self.status_label.config(text=T["break_time"])
                self.append_motivation(T["motivation_after_study"])
        else:
            # Break phase
            self.break_remaining = max(0, self.break_remaining - 1)
            try:
                cfg_break = max(1, self.to_seconds(self.entry_break.get()))
            except ValueError:
                cfg_break = self.progress["maximum"]
            self.progress["maximum"] = cfg_break
            self.progress["value"] = self.break_remaining

            if self.break_remaining <= 0:
                self.beep()
                # Prepare next work phase
                try:
                    self.work_remaining = max(1, self.to_seconds(self.entry_work.get()))
                except ValueError:
                    self.work_remaining = 25 * 60
                self.is_work_time = True

                self.progress["maximum"] = self.work_remaining
                self.progress["value"] = self.work_remaining

                messagebox.showinfo(T["msg_break_done_title"], T["msg_break_done_text"])
                self.status_label.config(text=T["back_to_focus"])
                self.append_motivation(T["motivation_after_break"])

        # Always update label (prevents display sticking at 00:01)
        self.update_timer_label()
        # Keep loop alive
        self.root.after(1000, self.tick)

    def append_motivation(self, text):
        try:
            current = self.status_label.cget('text')
            self.status_label.config(text=f"{current}  |  {text}")
        except Exception:
            pass

    # Analytics & target (line chart) with layout fixes + emoji title and empty-state
    def record_focus_session(self, seconds):
        now = datetime.now().strftime("%H:%M")
        today = self.stats[self.today_key]
        today["total_focus_sec"] += seconds
        today["sessions"] += 1
        today["longest_sec"] = max(today["longest_sec"], seconds)
        today["details"].append({
            "name": f"Session {today['sessions']}",
            "duration_min": seconds // 60,
            "time": now
        })
        save_json(STATS_FILE, self.stats)
        self.refresh_line_chart()
        self.update_target_label()

    def apply_chart_style(self):
        T = self.texts[self.language]
        self.ax.clear()
        # Light chart background
        self.fig.patch.set_facecolor("#ffffff")
        self.ax.set_facecolor("#ffffff")
        # Title spacing fix + emoji already in text
        self.ax.set_title(T["chart_title"], color=self.primary_color,
                          pad=14, fontsize=12, fontweight="bold")
        self.ax.set_xlabel(T["chart_xlabel"], color="#000000", labelpad=10)
        self.ax.set_ylabel(T["chart_ylabel"], color="#000000", labelpad=10)
        self.ax.grid(True, alpha=0.25, color="#000000")
        for spine in self.ax.spines.values():
            spine.set_color("#000000")
        self.ax.tick_params(colors="#000000", labelsize=9)
        # Prevent clipping of bottom x-labels and give top margin for title
        self.fig.subplots_adjust(bottom=0.24, left=0.10, right=0.98, top=0.90)

    def refresh_line_chart(self):
        T = self.texts[self.language]
        today = self.stats[self.today_key]
        y = [d["duration_min"] for d in today.get("details", [])]
        x = list(range(1, len(y) + 1))

        self.apply_chart_style()

        if x and y:
            # Trend line
            self.ax.plot(x, y, color=self.accent_color, linestyle="--", linewidth=1.2)
            # Ribbon emoji markers at points
            for xi, yi in zip(x, y):
                self.ax.text(xi, yi, T["emoji_marker"], fontsize=14, ha="center", va="bottom",
                             color=self.primary_color)
        else:
            # Centered empty-state message (with emoji already in text)
            self.ax.text(0.5, 0.5, T["no_sessions_chart"], color=self.primary_color,
                         ha="center", va="center", transform=self.ax.transAxes, fontsize=11)
        try:
            self.fig.tight_layout()
        except Exception:
            pass
        self.chart_canvas.draw()

    def update_target_label(self):
        T = self.texts[self.language]
        try:
            target_minutes = max(1, int(self.entry_target.get()))
        except ValueError:
            target_minutes = 120
        total_minutes_today = self.stats[self.today_key]["total_focus_sec"] // 60
        self.target_progress["maximum"] = target_minutes
        self.target_progress["value"] = min(target_minutes, total_minutes_today)
        self.target_label.config(text=f"{total_minutes_today} / {target_minutes} {T['target_label_suffix']}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    StudoruApp().run()