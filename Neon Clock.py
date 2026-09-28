import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from zoneinfo import ZoneInfo, available_timezones
import math, random, colorsys, json, threading, time
from pathlib import Path

try:
    import geonamescache
    from timezonefinder import TimezoneFinder
    CITIES_AVAILABLE = True
except ImportError:
    CITIES_AVAILABLE = False

try:
    import pystray
    from PIL import Image, ImageDraw
    TRAY_AVAILABLE = True
except ImportError:
    TRAY_AVAILABLE = False

# ============ ЧАСОВЫЕ ПОЯСА ============
_EXCLUDE = {"UTC","GMT","GMT0","GMT+0","GMT-0","UCT","Zulu",
            "Universal","Etc/UTC","Etc/GMT","Etc/Greenwich"}
ALL_ZONES = sorted(z for z in available_timezones()
                   if z not in _EXCLUDE and "/" in z)

# ============ ТЕМЫ ============
THEMES = {
    "Малиновый неон":   {"bg":"#0a0012","accent":"#ff006e","glow":"#ff4d9d","secondary":"#8338ec"},
    "Киберпанк":        {"bg":"#0d0221","accent":"#00fff5","glow":"#ff00ff","secondary":"#fffb00"},
    "Зелёный изумруд":  {"bg":"#001210","accent":"#00ff88","glow":"#39ff14","secondary":"#00d9ff"},
    "Оранжевый закат":  {"bg":"#120000","accent":"#ff6b00","glow":"#ffcc00","secondary":"#ff0055"},
    "Фиолетовый космос":{"bg":"#050014","accent":"#a855f7","glow":"#ec4899","secondary":"#06b6d4"},
    "Ледяной синий":    {"bg":"#000814","accent":"#00d4ff","glow":"#7dd3fc","secondary":"#c084fc"},
    "Красный дракон":   {"bg":"#0a0000","accent":"#ff0000","glow":"#ff4444","secondary":"#ffaa00"},
    "Золотой":          {"bg":"#0a0800","accent":"#ffd700","glow":"#ffed4e","secondary":"#ff8c00"},
    "Матрица":          {"bg":"#000000","accent":"#00ff00","glow":"#00ff88","secondary":"#008800"},
    "Vaporwave":        {"bg":"#1a0033","accent":"#ff71ce","glow":"#01cdfe","secondary":"#05ffa1"},
    "Synthwave":        {"bg":"#150024","accent":"#ff2a6d","glow":"#05d9e8","secondary":"#d1f7ff"},
    "Tron":             {"bg":"#000000","accent":"#00d9ff","glow":"#ff6ec7","secondary":"#ffffff"},
    "Cyberpunk 2077":   {"bg":"#0a0a0a","accent":"#fcee0a","glow":"#00f0ff","secondary":"#ff003c"},
    "Радуга":           {"bg":"#0a0a1a","accent":"#ff00ff","glow":"#00ffff","secondary":"#ffff00"},
    "Розовое золото":   {"bg":"#150a0a","accent":"#ffb6c1","glow":"#ff69b4","secondary":"#ffd700"},
    "Мятный лёд":       {"bg":"#001a14","accent":"#7fffd4","glow":"#e0fff4","secondary":"#00ced1"},
    "Персиковый рай":   {"bg":"#1a0e0a","accent":"#ffaa88","glow":"#ffd4b3","secondary":"#ff6b6b"},
    "Манговый смузи":   {"bg":"#1a1200","accent":"#ffb300","glow":"#ffe066","secondary":"#ff6a00"},
    "Плазма":           {"bg":"#0d001a","accent":"#ff0080","glow":"#00ffea","secondary":"#ffe600"},
    "Лава":             {"bg":"#120000","accent":"#ff3300","glow":"#ffcc00","secondary":"#ff0066"},
    "Ядовитый":         {"bg":"#0a1000","accent":"#aaff00","glow":"#ccff33","secondary":"#00ff66"},
    "Электрик":         {"bg":"#00001a","accent":"#ffff00","glow":"#0099ff","secondary":"#ffffff"},
    "Кислота":          {"bg":"#001a0a","accent":"#ccff00","glow":"#ff00cc","secondary":"#00ffff"},
    "Полярное сияние":  {"bg":"#000a0a","accent":"#00ffaa","glow":"#aaffee","secondary":"#0088ff"},
    "Глубокий океан":   {"bg":"#00040d","accent":"#0066ff","glow":"#00ccff","secondary":"#00ffcc"},
    "Космический лёд":  {"bg":"#00020a","accent":"#88ddff","glow":"#ddeeff","secondary":"#9966ff"},
    "Лунный свет":      {"bg":"#0a0a12","accent":"#e0e0ff","glow":"#aaccff","secondary":"#8888aa"},
    "Закат в Токио":    {"bg":"#1a0a14","accent":"#ff5577","glow":"#ffaa88","secondary":"#ffdd66"},
    "Аметист":          {"bg":"#10001a","accent":"#bb66ff","glow":"#dd99ff","secondary":"#ff66cc"},
    "Розовый закат":    {"bg":"#1a0a1a","accent":"#ff66aa","glow":"#ff99cc","secondary":"#ffcc88"},
    "Тёплый неон":      {"bg":"#140a00","accent":"#ff8833","glow":"#ffcc66","secondary":"#ff4477"},
    "Платина":          {"bg":"#0a0a0d","accent":"#e8e8f0","glow":"#ffffff","secondary":"#8899aa"},
    "Изумруд":          {"bg":"#001410","accent":"#00cc66","glow":"#33ffaa","secondary":"#00ffdd"},
    "Рубин":            {"bg":"#140006","accent":"#e60026","glow":"#ff4466","secondary":"#ffaa00"},
    "Сапфир":           {"bg":"#00061a","accent":"#0066cc","glow":"#3399ff","secondary":"#99ddff"},
    "Космос":           {"bg":"#000010","accent":"#8844ff","glow":"#ff44aa","secondary":"#44ddff"},
    "Галактика":        {"bg":"#0a0018","accent":"#cc44ff","glow":"#4488ff","secondary":"#ffdd00"},
    "Туманность":       {"bg":"#0d0015","accent":"#ff33cc","glow":"#6633ff","secondary":"#00ffcc"},
    "Чёрная дыра":      {"bg":"#000000","accent":"#ffffff","glow":"#8844ff","secondary":"#ff0066"},
    "Naruto":           {"bg":"#1a0a00","accent":"#ff8800","glow":"#ffdd44","secondary":"#2266ff"},
    "Sailor Moon":      {"bg":"#1a001a","accent":"#ffee00","glow":"#ff66cc","secondary":"#66ccff"},
    "Demon Slayer":     {"bg":"#0a0015","accent":"#00ccff","glow":"#ff0066","secondary":"#ffcc00"},
    "Тропики":          {"bg":"#001410","accent":"#00ff88","glow":"#ffdd00","secondary":"#ff3366"},
    "Сакура":           {"bg":"#14080d","accent":"#ffb3cc","glow":"#ffd9e6","secondary":"#cc66aa"},
    "Лаванда":          {"bg":"#0f0a1a","accent":"#cc99ff","glow":"#e6ccff","secondary":"#ff99cc"},
    "Кактус":           {"bg":"#0a1408","accent":"#88dd44","glow":"#ccff88","secondary":"#ff8844"},
}

LANGS = {
    "ru":{"search":"Поиск:","theme":"Тема:","lang":"Язык:","fx":"Эффект:",
          "city_btn":"🌍 Города","zone_btn":"🕐 Пояса",
          "hint":"F11 — экран  |  Esc — выход  |  🎲 — тема  |  🌈 — радуга  |  ⏱ — таймер  |  🔔 — будильник  |  🌙 — астро  |  📝 — заметки  |  🖥 — трей",
          "no_results":"Ничего не найдено",
          "alarm_title":"🔔 Будильники","alarm_add":"Добавить","alarm_time":"Время (ЧЧ:ММ):",
          "alarm_list":"Список:","alarm_none":"Нет будильников","alarm_delete":"Удалить",
          "alarm_fire":"⏰ БУДИЛЬНИК! {city} — {time}",
          "astro_title":"🌙 Астрономия","astro_moon":"Фаза луны:",
          "astro_day":"День года:","astro_week":"Неделя года:","astro_left":"Дней до конца года:",
          "notes_title":"📝 Заметки","notes_save":"💾 Сохранить","notes_clear":"🗑 Очистить",
          "notes_saved":"Сохранено","notes_auto":"Автосохранение каждые 3 сек",
          "stopwatch_title":"⏱ Секундомер / Таймер","sw_start":"▶ Старт","sw_stop":"⏸ Пауза",
          "sw_reset":"⟲ Сброс","timer_set":"Минуты:","timer_start":"▶ Запустить",
          "timer_done":"⏰ Время вышло!","timer_cancel":"✕ Отмена","stopwatch_lap":"⏱ Круг: ",
          "tray_not_available":"Не установлен pystray"},
    "en":{"search":"Search:","theme":"Theme:","lang":"Language:","fx":"Effect:",
          "city_btn":"🌍 Cities","zone_btn":"🕐 Zones",
          "hint":"F11 — Fullscreen  |  Esc — Exit  |  🎲 — Theme  |  🌈 — Rainbow  |  ⏱ — Timer  |  🔔 — Alarm  |  🌙 — Astro  |  📝 — Notes  |  🖥 — Tray",
          "no_results":"Nothing found",
          "alarm_title":"🔔 Alarms","alarm_add":"Add","alarm_time":"Time (HH:MM):",
          "alarm_list":"List:","alarm_none":"No alarms","alarm_delete":"Delete",
          "alarm_fire":"⏰ ALARM! {city} — {time}",
          "astro_title":"🌙 Astronomy","astro_moon":"Moon phase:",
          "astro_day":"Day of year:","astro_week":"Week of year:","astro_left":"Days left:",
          "notes_title":"📝 Notes","notes_save":"💾 Save","notes_clear":"🗑 Clear",
          "notes_saved":"Saved","notes_auto":"Autosave every 3 sec",
          "stopwatch_title":"⏱ Stopwatch / Timer","sw_start":"▶ Start","sw_stop":"⏸ Pause",
          "sw_reset":"⟲ Reset","timer_set":"Minutes:","timer_start":"▶ Start",
          "timer_done":"⏰ Time's up!","timer_cancel":"✕ Cancel","stopwatch_lap":"⏱ Lap: ",
          "tray_not_available":"pystray not installed"},
    "de":{"search":"Suche:","theme":"Thema:","lang":"Sprache:","fx":"Effekt:",
          "city_btn":"🌍 Städte","zone_btn":"🕐 Zonen",
          "hint":"F11 — Vollbild  |  Esc — Beenden  |  🎲 — Thema  |  🌈 — Regenbogen  |  ⏱ — Timer  |  🔔 — Wecker  |  🌙 — Astro  |  📝 — Notizen  |  🖥 — Tray",
          "no_results":"Nichts gefunden",
          "alarm_title":"🔔 Wecker","alarm_add":"Hinzufügen","alarm_time":"Zeit (HH:MM):",
          "alarm_list":"Liste:","alarm_none":"Keine Wecker","alarm_delete":"Löschen",
          "alarm_fire":"⏰ WECKER! {city} — {time}",
          "astro_title":"🌙 Astronomie","astro_moon":"Mondphase:",
          "astro_day":"Tag des Jahres:","astro_week":"Woche:","astro_left":"Tage bis Jahresende:",
          "notes_title":"📝 Notizen","notes_save":"💾 Speichern","notes_clear":"🗑 Löschen",
          "notes_saved":"Gespeichert","notes_auto":"Autosave alle 3 Sek",
          "stopwatch_title":"⏱ Stoppuhr / Timer","sw_start":"▶ Start","sw_stop":"⏸ Pause",
          "sw_reset":"⟲ Reset","timer_set":"Minuten:","timer_start":"▶ Start",
          "timer_done":"⏰ Zeit abgelaufen!","timer_cancel":"✕ Abbruch","stopwatch_lap":"⏱ Runde: ",
          "tray_not_available":"pystray fehlt"},
    "es":{"search":"Buscar:","theme":"Tema:","lang":"Idioma:","fx":"Efecto:",
          "city_btn":"🌍 Ciudades","zone_btn":"🕐 Zonas",
          "hint":"F11 — Pantalla completa  |  Esc — Salir  |  🎲 — Tema  |  🌈 — Arcoíris  |  ⏱ — Temporizador  |  🔔 — Alarma  |  🌙 — Astro  |  📝 — Notas  |  🖥 — Bandeja",
          "no_results":"Nada encontrado",
          "alarm_title":"🔔 Alarmas","alarm_add":"Añadir","alarm_time":"Hora (HH:MM):",
          "alarm_list":"Lista:","alarm_none":"Sin alarmas","alarm_delete":"Eliminar",
          "alarm_fire":"⏰ ¡ALARMA! {city} — {time}",
          "astro_title":"🌙 Astronomía","astro_moon":"Fase lunar:",
          "astro_day":"Día del año:","astro_week":"Semana:","astro_left":"Días restantes:",
          "notes_title":"📝 Notas","notes_save":"💾 Guardar","notes_clear":"🗑 Limpiar",
          "notes_saved":"Guardado","notes_auto":"Autoguardado cada 3 seg",
          "stopwatch_title":"⏱ Cronómetro / Temporizador","sw_start":"▶ Iniciar","sw_stop":"⏸ Pausa",
          "sw_reset":"⟲ Reiniciar","timer_set":"Minutos:","timer_start":"▶ Iniciar",
          "timer_done":"⏰ ¡Tiempo agotado!","timer_cancel":"✕ Cancelar","stopwatch_lap":"⏱ Vuelta: ",
          "tray_not_available":"pystray no instalado"},
}

FX_LABELS = {"✨ Звёзды":"stars","❄️ Снег":"snow","🔥 Огонь":"fire",
             "🍂 Листья":"leaves","⭕ Выкл":"off"}

SETTINGS_PATH = Path.home() / ".neon_clock_settings.json"
NOTES_PATH    = Path.home() / ".neon_clock_notes.txt"


def random_neon_theme():
    hue = random.random()
    ar,ag,ab = colorsys.hls_to_rgb(hue, 0.55, 1.0)
    gh = (hue + random.uniform(0.15,0.35)) % 1.0
    gr,gg,gb = colorsys.hls_to_rgb(gh, 0.75, 1.0)
    sh = (hue + 0.5) % 1.0
    sr,sg,sb = colorsys.hls_to_rgb(sh, 0.65, 1.0)
    return {"bg":"#0a0010",
            "accent":f"#{int(ar*255):02x}{int(ag*255):02x}{int(ab*255):02x}",
            "glow":f"#{int(gr*255):02x}{int(gg*255):02x}{int(gb*255):02x}",
            "secondary":f"#{int(sr*255):02x}{int(sg*255):02x}{int(sb*255):02x}"}


def blend(c1, c2, k):
    k = max(0.0, min(1.0, k))
    r1,g1,b1 = int(c1[1:3],16),int(c1[3:5],16),int(c1[5:7],16)
    r2,g2,b2 = int(c2[1:3],16),int(c2[3:5],16),int(c2[5:7],16)
    return f"#{max(0,min(255,int(r1+(r2-r1)*k))):02x}" \
           f"{max(0,min(255,int(g1+(g2-g1)*k))):02x}" \
           f"{max(0,min(255,int(b1+(b2-b1)*k))):02x}"


# ============ АСТРО ============
class AstroService:
    KNOWN_NEW_MOON = datetime(2000, 1, 6, 18, 14)
    SYNODIC_MONTH = 29.530588853

    def moon_phase(self, now):
        days = (now - self.KNOWN_NEW_MOON).total_seconds() / 86400
        phase = (days % self.SYNODIC_MONTH) / self.SYNODIC_MONTH
        if phase < 0.03 or phase > 0.97: return "🌑", "Новолуние"
        if phase < 0.22: return "🌒", "Молодая луна"
        if phase < 0.28: return "🌓", "Первая четверть"
        if phase < 0.47: return "🌔", "Растущая луна"
        if phase < 0.53: return "🌕", "Полнолуние"
        if phase < 0.72: return "🌖", "Убывающая луна"
        if phase < 0.78: return "🌗", "Последняя четверть"
        return "🌘", "Старая луна"

    def get_info(self, zone):
        try:
            now = datetime.now(ZoneInfo(zone))
        except Exception:
            now = datetime.now()
        emoji, name = self.moon_phase(now.replace(tzinfo=None))
        doy = now.timetuple().tm_yday
        year = now.year
        leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
        total = 366 if leap else 365
        return {"moon_emoji": emoji, "moon_name": name,
                "day_of_year": doy, "total_days": total,
                "days_left": total - doy, "week": now.isocalendar()[1]}


# ============ ЗАСТАВКА ============
class SplashScreen:
    TITLE_PART1 = "N E O N"
    TITLE_PART2 = "C L O C K"
    SUBTITLE = "World Time  •  Neon Edition"
    STORY_LINES = [
        "В мире, где время течёт сквозь неоновые огни,",
        "родились часы, что видят каждый город",
        "планеты — от заката в Токио до рассвета в Нью-Йорке.",
        "",
        "46 тем  •  25 000 городов  •  Бесконечность эффектов.",
        "Одно мгновение — и ты в любой точке Земли.",
    ]
    CREATOR = "Created by   W e b 0 f"
    VERSION = "v1.0  •  2026"
    HINT = "▸  Нажми Enter или кликни мышкой, чтобы продолжить  ◂"
    BG = "#000000"; ACCENT = "#00fff5"; GLOW = "#ff00ff"
    SECOND = "#fffb00"; DIM = "#1a1a2a"
    MATRIX_CHARS = "01ЖФ#@$%&*+=<>¦:."
    READY_AT_MS = 7200

    def __init__(self, master, on_finish, duration_ms=8000):
        self.master = master; self.on_finish = on_finish
        self.start_time = time.time()
        self.waiting_for_input = False; self.closing = False
        self.close_start_time = 0

        self.win = tk.Toplevel(master)
        self.win.overrideredirect(True)
        self.win.attributes("-topmost", True)
        self.win.configure(bg=self.BG)
        self.W, self.H = 820, 560
        self.win.update_idletasks()
        sw = self.win.winfo_screenwidth(); sh = self.win.winfo_screenheight()
        x = (sw - self.W)//2; y = (sh - self.H)//2
        self.win.geometry(f"{self.W}x{self.H}+{x}+{y}")

        self.canvas = tk.Canvas(self.win, width=self.W, height=self.H,
                                bg=self.BG, highlightthickness=0, bd=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.matrix_cols = []
        cw = 14
        for xx in range(0, self.W, cw):
            self.matrix_cols.append({"x":xx+cw//2, "y":random.uniform(-self.H,0),
                "speed":random.uniform(4,10),
                "chars":[random.choice(self.MATRIX_CHARS) for _ in range(12)],
                "change_tick":0})

        self.canvas.create_rectangle(4,4,self.W-4,self.H-4, outline=self.ACCENT, width=2)
        self.canvas.create_rectangle(10,10,self.W-10,self.H-10, outline=self.GLOW, width=1)
        for cx,cy,dx,dy in [(4,4,1,1),(self.W-4,4,-1,1),(4,self.H-4,1,-1),(self.W-4,self.H-4,-1,-1)]:
            self.canvas.create_line(cx,cy,cx+30*dx,cy, fill=self.SECOND, width=3)
            self.canvas.create_line(cx,cy,cx,cy+30*dy, fill=self.SECOND, width=3)

        self.dot = self.canvas.create_oval(self.W/2-5,36,self.W/2+5,46,
                                           fill=self.ACCENT, outline="")
        self.ring1 = self.canvas.create_oval(0,0,0,0, outline=self.GLOW, width=2)
        self.ring2 = self.canvas.create_oval(0,0,0,0, outline=self.ACCENT, width=1)

        self.title_y = 130; self.title_letter_ids = []
        ls = 32; total = len(self.TITLE_PART1)
        sx = self.W/2 - (total-1)*ls/2
        for i,ch in enumerate(self.TITLE_PART1):
            tid = self.canvas.create_text(sx+i*ls, self.title_y, text="",
                fill=self.ACCENT, font=("Consolas",34,"bold"), anchor="center")
            self.title_letter_ids.append(tid)

        self.title2_id = self.canvas.create_text(self.W/2, self.title_y+55, text="",
            fill=self.GLOW, font=("Consolas",30,"bold"), anchor="center")
        self.subtitle_id = self.canvas.create_text(self.W/2, 205, text="",
            fill=self.SECOND, font=("Segoe UI",12), anchor="center")

        self.story_ids = []
        ys = 270
        for i in range(len(self.STORY_LINES)):
            tid = self.canvas.create_text(self.W/2, ys+i*24, text="",
                fill="#c0c0d0", font=("Segoe UI",11), anchor="center", justify="center")
            self.story_ids.append(tid)

        self.creator_id = self.canvas.create_text(self.W/2, self.H-140, text="",
            fill=self.SECOND, font=("Consolas",15,"bold"), anchor="center")
        self.hint_id = self.canvas.create_text(self.W/2, self.H-95, text="",
            fill=self.SECOND, font=("Consolas",12,"bold"), anchor="center")
        self.version_id = self.canvas.create_text(self.W/2, self.H-62, text="",
            fill=self.GLOW, font=("Segoe UI",10), anchor="center")

        self.canvas.create_rectangle(120,self.H-40,self.W-120,self.H-32,
                                     fill=self.DIM, outline="")
        self.pbar = self.canvas.create_rectangle(120,self.H-40,120,self.H-32,
                                                 fill=self.ACCENT, outline="")
        self.pbar_shine = self.canvas.create_rectangle(120,self.H-40,130,self.H-32,
                                                       fill="#ffffff", outline="")
        self.sweep_line = self.canvas.create_line(0,20,60,20, fill=self.ACCENT, width=2)
        self.sweep_x = 0

        self.flash_rect = self.canvas.create_rectangle(0,0,self.W,self.H,
                                                       fill=self.BG, outline="")
        self.canvas.tag_lower(self.flash_rect)
        self.canvas.itemconfig(self.flash_rect, state="hidden")

        self.win.bind("<Key>", self._on_user_input)
        self.win.bind("<Button-1>", self._on_user_input)
        self.win.bind("<Button-2>", self._on_user_input)
        self.win.bind("<Button-3>", self._on_user_input)
        self.canvas.bind("<Button-1>", self._on_user_input)
        self.canvas.bind("<Button-2>", self._on_user_input)
        self.canvas.bind("<Button-3>", self._on_user_input)
        try:
            self.win.focus_force(); self.canvas.focus_set()
        except Exception: pass

        self._animate()

    def _on_user_input(self, event=None):
        if not self.waiting_for_input or self.closing: return "break"
        self.closing = True; self.close_start_time = time.time()
        return "break"

    def _all_text_ids(self):
        return (self.title_letter_ids +
                [self.title2_id, self.subtitle_id, self.creator_id,
                 self.hint_id, self.version_id] + self.story_ids)

    def _animate(self):
        if self.closing:
            self._animate_closing(); return
        try:
            elapsed_ms = (time.time() - self.start_time) * 1000
            t = max(0.0, min(1.0, elapsed_ms / self.READY_AT_MS))
        except Exception:
            elapsed_ms, t = 0, 0

        if elapsed_ms < 1100:
            alpha = 1.0 if elapsed_ms > 200 else elapsed_ms / 200
        else:
            alpha = max(0, min(1, (2500 - elapsed_ms) / 1400))
        self._draw_matrix(alpha)

        pulse = (math.sin(elapsed_ms*0.006) + 1) / 2
        r = 4 + pulse*5; cx, cy = self.W/2, 41
        self.canvas.coords(self.dot, cx-r, cy-r, cx+r, cy+r)
        self.canvas.itemconfig(self.dot, fill=blend(self.ACCENT, self.GLOW, pulse))

        self.sweep_x = (self.sweep_x + 6) % (self.W + 60)
        self.canvas.coords(self.sweep_line, self.sweep_x-60, 20, self.sweep_x, 20)

        letter_start = 1000; letter_delay = 280
        for i, tid in enumerate(self.title_letter_ids):
            lt = letter_start + i*letter_delay
            if elapsed_ms > lt:
                p = min((elapsed_ms-lt)/250, 1.0)
                if p < 1:
                    color = blend(self.ACCENT, "#ffffff", math.sin(p*math.pi)*0.9)
                else:
                    pp = (math.sin(elapsed_ms*0.004+i)+1)/2
                    color = blend(self.ACCENT, self.GLOW, pp*0.4)
                self.canvas.itemconfig(tid, text=self.TITLE_PART1[i], fill=color)

        if elapsed_ms > 3000:
            p = min((elapsed_ms-3000)/700, 1.0)
            n = int(len(self.TITLE_PART2)*p)
            self.canvas.itemconfig(self.title2_id, text=self.TITLE_PART2[:n])

        if elapsed_ms > 4000:
            rt = max(0.0, min(1.0, (elapsed_ms-4000)/1000))
            r1 = 130 + rt*60; cx, cy = self.W/2, self.title_y+20
            self.canvas.coords(self.ring1, cx-r1, cy-r1, cx+r1, cy+r1)
            r2 = 90 + math.sin(elapsed_ms*0.005)*12
            self.canvas.coords(self.ring2, cx-r2, cy-r2, cx+r2, cy+r2)
            self.canvas.itemconfig(self.ring1, outline=blend(self.BG, self.GLOW, rt*0.7))
            self.canvas.itemconfig(self.ring2, outline=self.ACCENT)

        if elapsed_ms > 2500:
            p = min((elapsed_ms-2500)/500, 1.0)
            n = int(len(self.SUBTITLE)*p)
            self.canvas.itemconfig(self.subtitle_id, text=self.SUBTITLE[:n])

        for i, tid in enumerate(self.story_ids):
            ls = 5000 + i*220
            if elapsed_ms > ls:
                p = min((elapsed_ms-ls)/350, 1.0)
                n = int(len(self.STORY_LINES[i])*p)
                self.canvas.itemconfig(tid, text=self.STORY_LINES[i][:n])

        if elapsed_ms > 6500:
            p = min((elapsed_ms-6500)/600, 1.0)
            n = int(len(self.CREATOR)*p)
            self.canvas.itemconfig(self.creator_id, text=self.CREATOR[:n])
            pp = (math.sin(elapsed_ms*0.01)+1)/2
            self.canvas.itemconfig(self.creator_id,
                                   fill=blend(self.SECOND, "#ffffff", pp*0.5))

        if elapsed_ms > 7000:
            self.canvas.itemconfig(self.version_id, text=self.VERSION)

        total_w = self.W - 240
        bar_w = total_w * t
        self.canvas.coords(self.pbar, 120, self.H-40, 120+bar_w, self.H-32)
        self.canvas.itemconfig(self.pbar, fill=blend(self.ACCENT, self.GLOW, t))
        sh = 120 + bar_w - 8
        self.canvas.coords(self.pbar_shine, sh, self.H-40, sh+8, self.H-32)

        if elapsed_ms >= self.READY_AT_MS and not self.waiting_for_input:
            self.waiting_for_input = True
            self.canvas.coords(self.pbar, 120, self.H-40, 120+total_w, self.H-32)

        if self.waiting_for_input:
            pp = (math.sin(elapsed_ms*0.008)+1)/2
            self.canvas.itemconfig(self.hint_id, text=self.HINT,
                                   fill=blend(self.SECOND, "#ffffff", pp))

        self.win.after(30, self._animate)

    def _animate_closing(self):
        ct = (time.time() - self.close_start_time)*1000
        if ct < 200:
            f = ct / 200
            for tid in self._all_text_ids():
                try:
                    cur = self.canvas.itemcget(tid, "fill")
                    self.canvas.itemconfig(tid, fill=blend(cur, self.BG, f))
                except Exception: pass
            self.win.after(20, self._animate_closing); return
        if ct < 400:
            f = (ct-200)/200
            self.canvas.itemconfig(self.flash_rect, state="normal")
            self.canvas.itemconfig(self.flash_rect, fill=blend(self.BG, "#ffffff", f))
            self.canvas.tag_raise(self.flash_rect)
            self.win.after(20, self._animate_closing); return
        if ct < 700:
            f = (ct-400)/300
            self.canvas.itemconfig(self.flash_rect, fill=blend("#ffffff", self.BG, f))
            self.canvas.tag_raise(self.flash_rect)
            self.win.after(20, self._animate_closing); return
        try: self.win.destroy()
        except Exception: pass
        self.on_finish()

    def _draw_matrix(self, alpha):
        self.canvas.delete("matrix")
        if alpha <= 0.01: return
        for col in self.matrix_cols:
            col["y"] += col["speed"]; col["change_tick"] += 1
            if col["change_tick"] % 5 == 0:
                idx = random.randint(0, len(col["chars"])-1)
                col["chars"][idx] = random.choice(self.MATRIX_CHARS)
            if col["y"] > self.H + 100:
                col["y"] = random.uniform(-200, -50)
                col["speed"] = random.uniform(4, 10)
            for i, ch in enumerate(col["chars"]):
                y = col["y"] - i*16
                if y < -20 or y > self.H + 20: continue
                fr = 1.0 - (i/len(col["chars"]))
                br = fr*alpha
                if i == 0:
                    color = blend(self.BG, "#ffffff", br)
                else:
                    base = self.ACCENT if i % 3 else self.GLOW
                    color = blend(self.BG, base, br*0.7)
                self.canvas.create_text(col["x"], y, text=ch, fill=color,
                                        font=("Consolas", 11), tags="matrix")
        self.canvas.tag_lower("matrix")


# ============ БАЗА ГОРОДОВ ============
class CityDatabase:
    def __init__(self):
        gc = geonamescache.GeonamesCache()
        countries = gc.get_countries()
        self.cities = []
        for cid, c in gc.get_cities().items():
            cc = c["countrycode"]
            country = countries.get(cc,{}).get("name",cc)
            self.cities.append({"name":c["name"],"country":country,
                "lat":c["latitude"],"lon":c["longitude"],"pop":c["population"],
                "search":f"{c['name']} {country}".lower(),"tz":None})
        self.cities.sort(key=lambda x:-x["pop"])
        self._tf = None
    def _get_tf(self):
        if self._tf is None: self._tf = TimezoneFinder()
        return self._tf
    def search(self, query, limit=300):
        q = query.strip().lower()
        if not q: return self.cities[:limit]
        out = []
        for c in self.cities:
            if q in c["search"]:
                out.append(c)
                if len(out)>=limit: break
        return out
    def get_timezone(self, city):
        if city["tz"] is None:
            tz = self._get_tf().timezone_at(lat=city["lat"],lng=city["lon"])
            city["tz"] = tz or "UTC"
        return city["tz"]
    def find_by_zone(self, zone):
        for c in self.cities:
            if c["tz"] is None:
                try:
                    c["tz"] = self._get_tf().timezone_at(lat=c["lat"],lng=c["lon"]) or "UTC"
                except Exception: c["tz"] = "UTC"
            if c["tz"] == zone: return c
        return None


# ============ ЭФФЕКТЫ ФОНА (исправлено) ============
class BackgroundFX:
    STAR_COLORS = ["#ffffff","#ffeeaa","#aaddff","#ffddff","#ffffcc"]
    SNOW_COLORS = ["#ffffff","#e0f0ff","#cceeff","#ddeeff","#f0f8ff"]
    FIRE_COLORS = ["#ff2200","#ff6600","#ffaa00","#ffdd00","#ffff88"]
    LEAF_COLORS = ["#ff6600","#cc3300","#ff9933","#cc6600",
                   "#ffcc33","#996633","#99cc33","#993300"]

    # Разрешённые режимы (для защиты от битых сохранений)
    VALID_MODES = {"stars", "snow", "fire", "leaves", "off"}

    def __init__(self, canvas):
        self.canvas = canvas
        self.mode = "stars"
        self.w = 0; self.h = 0; self.tick = 0
        self.particles = []
        self.bg_color = "#000000"; self.grid_color = "#333333"

    def set_mode(self, mode):
        """Безопасно устанавливает режим, игнорируя неизвестные."""
        self.mode = mode if mode in self.VALID_MODES else "stars"

    def update_colors(self, theme):
        self.bg_color = theme["bg"]
        self.grid_color = blend(theme["bg"], theme["accent"], 0.22)

    def resize(self, w, h):
        if w < 50 or h < 50: return
        self.w, self.h = w, h
        self._reset_particles()
        # фон рисуем только один раз — через сам canvas bg, без bg_rect
        self.canvas.delete("grid")
        if self.mode != "off":
            step = 80
            for x in range(0, self.w, step):
                self.canvas.create_line(x, 0, x, self.h,
                                        fill=self.grid_color, width=1, tags="grid")
            for y in range(0, self.h, step):
                self.canvas.create_line(0, y, self.w, y,
                                        fill=self.grid_color, width=1, tags="grid")
        self.canvas.tag_lower("grid")

    def _reset_particles(self):
        self.particles = []
        w, h = self.w, self.h
        if self.mode == "stars":
            for _ in range(200):
                self.particles.append({"x":random.uniform(0,w),"y":random.uniform(0,h),
                    "r":random.uniform(1.5,4.0),"vy":random.uniform(0.1,0.5),
                    "phase":random.uniform(0,math.tau),
                    "color":random.choice(self.STAR_COLORS)})
        elif self.mode == "snow":
            for _ in range(150):
                self.particles.append(self._new_snow(random_y=True))
        elif self.mode == "fire":
            for _ in range(180):
                self.particles.append(self._new_fire(random_y=True))
        elif self.mode == "leaves":
            for _ in range(60):
                self.particles.append(self._new_leaf(random_y=True))

    def _new_fire(self, random_y=False):
        w, h = self.w, self.h
        return {"x":random.uniform(0,w),
                "y":h+random.uniform(0,h) if random_y else h+5,
                "r":random.uniform(2.0,5.0),"vy":random.uniform(-3.5,-1.5),
                "vx":random.uniform(-0.7,0.7),"life":1.0,
                "decay":random.uniform(0.004,0.012)}

    def _new_snow(self, random_y=False):
        w, h = self.w, self.h
        return {"x":random.uniform(0,w),
                "y":random.uniform(-h,h) if random_y else -10,
                "r":random.uniform(1.5,4.0),
                "vy":random.uniform(0.8,2.6),
                "vx":random.uniform(-0.3,0.3),
                "sway":random.uniform(0,math.tau),
                "sway_speed":random.uniform(0.015,0.05),
                "alpha":random.uniform(0.7,1.0),
                "color":random.choice(self.SNOW_COLORS)}

    def _new_leaf(self, random_y=False):
        w, h = self.w, self.h
        return {"x":random.uniform(0,w),
                "y":random.uniform(-h,h) if random_y else -20,
                "size":random.uniform(6,12),"vy":random.uniform(0.8,2.0),
                "vx":random.uniform(-0.8,0.8),"angle":random.uniform(0,math.tau),
                "spin":random.uniform(-0.08,0.08),"sway":random.uniform(0,math.tau),
                "sway_speed":random.uniform(0.03,0.08),
                "color":random.choice(self.LEAF_COLORS)}

    def draw(self):
        if self.mode == "off":
            self.canvas.delete("particle")
            return
        drawer = {"stars":self._draw_stars, "snow":self._draw_snow,
                  "fire":self._draw_fire, "leaves":self._draw_leaves}.get(self.mode)
        if drawer is None:
            return
        self.tick += 1
        self.canvas.delete("particle")
        drawer()
        # Порядок: grid внизу, particle над grid, text и widget наверху
        self.canvas.tag_lower("grid")
        self.canvas.tag_raise("particle", "grid")
        self.canvas.tag_raise("text_layer")
        self.canvas.tag_raise("widget_layer")

    def _draw_stars(self):
        for s in self.particles:
            s["y"] += s["vy"]
            if s["y"] > self.h:
                s["y"] = 0; s["x"] = random.uniform(0, self.w)
            k = (math.sin(self.tick*0.05+s["phase"])+1)/2
            color = blend(self.bg_color, s["color"], 0.5+0.5*k)
            r = s["r"]
            self.canvas.create_oval(s["x"]-r, s["y"]-r, s["x"]+r, s["y"]+r,
                                    fill=color, outline="", tags="particle")

    def _draw_snow(self):
        for s in list(self.particles):
            s["sway"] += s["sway_speed"]
            s["y"] += s["vy"]
            s["x"] += s["vx"] + math.sin(s["sway"])*0.6
            if s["y"] > self.h + 10:
                self.particles.remove(s)
                self.particles.append(self._new_snow())
                continue
            color = blend(self.bg_color, s["color"], s["alpha"])
            r = s["r"]
            self.canvas.create_oval(s["x"]-r, s["y"]-r, s["x"]+r, s["y"]+r,
                                    fill=color, outline="", tags="particle")

    def _draw_fire(self):
        for p in list(self.particles):
            p["x"] += p["vx"]; p["y"] += p["vy"]; p["life"] -= p["decay"]
            if p["life"] <= 0 or p["y"] < -20:
                self.particles.remove(p)
                self.particles.append(self._new_fire())
                continue
            idx = min(int(p["life"]*(len(self.FIRE_COLORS)-1)),
                      len(self.FIRE_COLORS)-1)
            color = blend(self.bg_color, self.FIRE_COLORS[idx], 0.35+0.65*p["life"])
            r = p["r"]*(0.4+0.6*p["life"])
            self.canvas.create_oval(p["x"]-r, p["y"]-r, p["x"]+r, p["y"]+r,
                                    fill=color, outline="", tags="particle")

    def _draw_leaves(self):
        for l in list(self.particles):
            l["sway"] += l["sway_speed"]; l["angle"] += l["spin"]
            l["y"] += l["vy"]; l["x"] += l["vx"] + math.sin(l["sway"])*0.7
            if l["y"] > self.h + 20:
                self.particles.remove(l)
                self.particles.append(self._new_leaf())
                continue
            s = l["size"]; cx, cy = l["x"], l["y"]; pts = []
            for ang, rad in [(0,s),(math.pi/2,s*0.6),
                             (math.pi,s),(3*math.pi/2,s*0.6)]:
                a = ang + l["angle"]
                pts.extend([cx+math.cos(a)*rad, cy+math.sin(a)*rad])
            self.canvas.create_polygon(pts, fill=l["color"], outline="", tags="particle")


# ============ ЗАМЕТКИ ============
class NotesService:
    def __init__(self):
        self.path = NOTES_PATH

    def load(self):
        try:
            if self.path.exists():
                return self.path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"[Notes] load error: {e}")
        return ""

    def save(self, text):
        try:
            self.path.write_text(text, encoding="utf-8")
            return True
        except Exception as e:
            print(f"[Notes] save error: {e}")
            return False


# ============ ПРИЛОЖЕНИЕ ============
class NeonClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Neon Clock — by Web0f")
        self.root.geometry("1300x820")
        self.root.configure(bg="#0a0012")

        self.current_zone = "Europe/Moscow"
        self.current_label = "Moscow"
        self.current_city_info = None
        self.lang = "ru"
        self.theme_name = "Малиновый неон"
        self.fx_mode = "stars"
        self.alarms = []
        self.fullscreen = False
        self.pulse = 0.0
        self.rainbow = False
        self.rainbow_hue = 0.0
        self.mode = "city" if CITIES_AVAILABLE else "zone"
        self._current_results = []
        self._last_alarm_check = ""
        self._flash_until = 0
        self._flash_state = False
        self._transitioning = False
        self.tray_icon = None

        self.city_db = CityDatabase() if CITIES_AVAILABLE else None
        self.astro = AstroService()
        self.notes = NotesService()

        self._load_settings()
        self._build_ui()
        self._apply_theme()
        self._update_lang_texts()
        self._refresh_list()
        # Принудительно задаём размер фона до реального <Configure>
        self.fx.resize(1300, 820)
        self._tick()
        self._animate_bg()
        self._update_astro()

        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _load_settings(self):
        try:
            if SETTINGS_PATH.exists():
                s = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
                self.theme_name = s.get("theme", self.theme_name)
                if self.theme_name not in THEMES: self.theme_name = "Малиновый неон"
                self.lang = s.get("lang", self.lang)
                if self.lang not in LANGS: self.lang = "ru"
                fx = s.get("fx", self.fx_mode)
                # ВАЖНО: если сохранён старый режим ("rain") → ставим "snow"
                if fx not in ("stars","snow","fire","leaves","off"):
                    fx = "stars"
                self.fx_mode = fx
                self.current_zone = s.get("zone", self.current_zone)
                self.current_label = s.get("label", self.current_label)
                self.alarms = s.get("alarms", [])
                self.rainbow = s.get("rainbow", False)
                if self.current_zone and "/" in self.current_zone and self.city_db:
                    self.current_city_info = self.city_db.find_by_zone(self.current_zone)
        except Exception as e:
            print(f"[Settings] {e}")

    def _save_settings(self):
        try:
            SETTINGS_PATH.write_text(json.dumps({
                "theme":self.theme_name,"lang":self.lang,"fx":self.fx_mode,
                "zone":self.current_zone,"label":self.current_label,
                "alarms":self.alarms,"rainbow":self.rainbow,
            }, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception as e:
            print(f"[Settings] {e}")

    def _on_close(self):
        self._save_settings()
        if self.tray_icon:
            try: self.tray_icon.stop()
            except Exception: pass
        self.root.destroy()

    def _build_ui(self):
        self.canvas = tk.Canvas(self.root, highlightthickness=0, bd=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.fx = BackgroundFX(self.canvas)
        self.fx.set_mode(self.fx_mode)

        # Верхняя панель
        self.top = tk.Frame(self.canvas)
        self.canvas.create_window(15, 12, window=self.top, anchor="nw", tags="widget_layer")

        self.search_label = tk.Label(self.top, font=("Segoe UI", 10, "bold"))
        self.search_label.pack(side=tk.LEFT, padx=(0, 4))
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._refresh_list())
        self.search_entry = tk.Entry(self.top, textvariable=self.search_var,
                                     font=("Segoe UI", 11), width=14,
                                     relief=tk.FLAT, insertbackground="#fff")
        self.search_entry.pack(side=tk.LEFT, padx=(0, 6))

        self.mode_btn = tk.Button(self.top, command=self._toggle_mode,
                                  font=("Segoe UI", 9, "bold"), relief=tk.FLAT,
                                  cursor="hand2", borderwidth=0, padx=7, pady=3)
        self.mode_btn.pack(side=tk.LEFT, padx=(0, 6))

        self.theme_label = tk.Label(self.top, font=("Segoe UI", 10, "bold"))
        self.theme_label.pack(side=tk.LEFT, padx=(0, 4))
        self.theme_var = tk.StringVar(value=self.theme_name)
        self.theme_combo = ttk.Combobox(self.top, textvariable=self.theme_var,
                                        values=list(THEMES.keys()),
                                        state="readonly", width=14)
        self.theme_combo.pack(side=tk.LEFT, padx=(0, 3))
        self.theme_combo.bind("<<ComboboxSelected>>", self._on_theme)

        self.rand_btn = tk.Button(self.top, text="🎲", command=self._random_theme,
                                  font=("Segoe UI", 10, "bold"), relief=tk.FLAT,
                                  cursor="hand2", borderwidth=0, padx=5, pady=3)
        self.rand_btn.pack(side=tk.LEFT, padx=(0, 6))

        self.rainbow_btn = tk.Button(self.top, text="🌈", command=self._toggle_rainbow,
                                     font=("Segoe UI", 10, "bold"), relief=tk.FLAT,
                                     cursor="hand2", borderwidth=0, padx=5, pady=3)
        self.rainbow_btn.pack(side=tk.LEFT, padx=(0, 8))

        self.fx_label = tk.Label(self.top, font=("Segoe UI", 10, "bold"))
        self.fx_label.pack(side=tk.LEFT, padx=(0, 4))
        # Находим метку для текущего режима (или "✨ Звёзды")
        initial_label = "✨ Звёзды"
        for lbl, key in FX_LABELS.items():
            if key == self.fx_mode:
                initial_label = lbl; break
        self.fx_var = tk.StringVar(value=initial_label)
        self.fx_combo = ttk.Combobox(self.top, textvariable=self.fx_var,
                                     values=list(FX_LABELS.keys()),
                                     state="readonly", width=10)
        self.fx_combo.pack(side=tk.LEFT, padx=(0, 6))
        self.fx_combo.bind("<<ComboboxSelected>>", self._on_fx_change)

        self.lang_label = tk.Label(self.top, font=("Segoe UI", 10, "bold"))
        self.lang_label.pack(side=tk.LEFT, padx=(0, 4))
        self.lang_var = tk.StringVar(value=self.lang)
        self.lang_combo = ttk.Combobox(self.top, textvariable=self.lang_var,
                                       values=list(LANGS.keys()),
                                       state="readonly", width=4)
        self.lang_combo.pack(side=tk.LEFT, padx=(0, 10))
        self.lang_combo.bind("<<ComboboxSelected>>", self._on_lang)

        # Кнопки справа
        self.alarm_btn = tk.Button(self.top, text="🔔", command=self._open_alarm,
                                   font=("Segoe UI", 11), relief=tk.FLAT,
                                   cursor="hand2", borderwidth=0, padx=6, pady=2)
        self.alarm_btn.pack(side=tk.LEFT, padx=(0, 3))

        self.sw_btn = tk.Button(self.top, text="⏱", command=self._open_stopwatch,
                                font=("Segoe UI", 11), relief=tk.FLAT,
                                cursor="hand2", borderwidth=0, padx=6, pady=2)
        self.sw_btn.pack(side=tk.LEFT, padx=(0, 3))

        self.astro_btn = tk.Button(self.top, text="🌙", command=self._open_astro,
                                   font=("Segoe UI", 11), relief=tk.FLAT,
                                   cursor="hand2", borderwidth=0, padx=6, pady=2)
        self.astro_btn.pack(side=tk.LEFT, padx=(0, 3))

        self.notes_btn = tk.Button(self.top, text="📝", command=self._open_notes,
                                   font=("Segoe UI", 11), relief=tk.FLAT,
                                   cursor="hand2", borderwidth=0, padx=6, pady=2)
        self.notes_btn.pack(side=tk.LEFT, padx=(0, 3))

        self.tray_btn = tk.Button(self.top, text="🖥", command=self._minimize_to_tray,
                                  font=("Segoe UI", 11), relief=tk.FLAT,
                                  cursor="hand2", borderwidth=0, padx=6, pady=2)
        self.tray_btn.pack(side=tk.LEFT)

        # Список слева
        self.left = tk.Frame(self.canvas, width=320)
        self.left.pack_propagate(False)
        self.left_window = self.canvas.create_window(15, 70, window=self.left,
                                                     anchor="nw", tags="widget_layer")
        self.listbox = tk.Listbox(self.left, font=("Segoe UI", 10),
                                  activestyle="none", borderwidth=0,
                                  highlightthickness=0)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox.bind("<<ListboxSelect>>", self._on_list_select)
        self.scroll = tk.Scrollbar(self.left, command=self.listbox.yview)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.configure(yscrollcommand=self.scroll.set)

        # ЧАСЫ (явные цвета)
        self.hm_text = self.canvas.create_text(700, 300, text="00:00",
            font=("Consolas", 110, "bold"), fill="#ffffff",
            anchor="center", tags="text_layer")
        self.sec_text = self.canvas.create_text(700, 430, text="00",
            font=("Consolas", 60, "bold"), fill="#ffffff",
            anchor="center", tags="text_layer")
        self.date_text = self.canvas.create_text(700, 500, text="",
            font=("Segoe UI", 18), fill="#ffffff",
            anchor="center", tags="text_layer")
        self.city_text = self.canvas.create_text(700, 540, text="",
            font=("Segoe UI", 14, "italic"), fill="#ffffff",
            anchor="center", tags="text_layer")

        # ⚡ Подпись создателя — прямо ПОД часами, крупнее и с glow
        self.creator_label = self.canvas.create_text(700, 600, text="",
            font=("Consolas", 22, "bold"), fill="#ffffff",
            anchor="center", tags="text_layer")

        # Астро-блок (правый верхний угол)
        self.astro_text = self.canvas.create_text(1230, 90, text="",
            font=("Segoe UI", 11, "bold"), fill="#ffffff",
            anchor="ne", tags="text_layer", justify="right")

        # Подсказка внизу
        self.hint_text = self.canvas.create_text(650, 790, text="",
            font=("Segoe UI", 9), fill="#ffffff",
            anchor="center", tags="text_layer")

        self.canvas.bind("<Configure>", self._on_canvas_resize)
        self.root.update_idletasks()
        self.canvas.tag_raise("text_layer")
        self.canvas.tag_raise("widget_layer")

    def _on_canvas_resize(self, event):
        w, h = event.width, event.height
        if w < 50 or h < 50: return
        self.fx.resize(w, h)
        self.root.update_idletasks()
        top_h = self.top.winfo_reqheight() + 22
        self.canvas.coords(self.left_window, 15, top_h)
        list_h = h - top_h - 40
        self.canvas.itemconfig(self.left_window, height=max(list_h, 120))
        left_area = 15 + 320 + 15
        right_area = w - 15
        cx = (left_area + right_area) // 2
        cy = top_h + (h - top_h - 40) // 2
        self.canvas.coords(self.hm_text, cx, cy-110)
        self.canvas.coords(self.sec_text, cx, cy+30)
        self.canvas.coords(self.date_text, cx, cy+105)
        self.canvas.coords(self.city_text, cx, cy+143)
        self.canvas.coords(self.creator_label, cx, cy+195)   # под часами!
        self.canvas.coords(self.astro_text, w-20, 90)
        self.canvas.coords(self.hint_text, w//2, h-15)
        self.canvas.tag_raise("text_layer")
        self.canvas.tag_raise("widget_layer")

    def _apply_theme_with(self, theme):
        t = theme
        self.root.configure(bg=t["bg"]); self.canvas.configure(bg=t["bg"])
        self.top.configure(bg=t["bg"]); self.left.configure(bg=t["bg"])
        for w in (self.search_label, self.theme_label, self.lang_label, self.fx_label):
            w.configure(bg=t["bg"], fg=t["accent"])
        self.search_entry.configure(bg=t["bg"], fg=t["accent"],
                                    highlightbackground=t["accent"],
                                    highlightcolor=t["glow"], highlightthickness=1)
        self.mode_btn.configure(bg=t["secondary"], fg=t["bg"],
                                activebackground=t["glow"], activeforeground=t["bg"])
        self.rand_btn.configure(bg=t["accent"], fg=t["bg"],
                                activebackground=t["glow"], activeforeground=t["bg"])
        self.rainbow_btn.configure(bg=t["glow"], fg=t["bg"],
                                   activebackground=t["accent"], activeforeground=t["bg"])
        for btn in (self.alarm_btn, self.sw_btn, self.astro_btn,
                    self.notes_btn, self.tray_btn):
            btn.configure(bg=t["glow"], fg=t["bg"],
                          activebackground=t["accent"], activeforeground=t["bg"])
        self.listbox.configure(bg=t["bg"], fg=t["accent"],
                               selectbackground=t["secondary"],
                               selectforeground=t["bg"],
                               highlightbackground=t["bg"])
        try:
            self.canvas.itemconfig(self.hm_text, fill=t["accent"])
            self.canvas.itemconfig(self.sec_text, fill=t["glow"])
            self.canvas.itemconfig(self.date_text, fill=t["glow"])
            self.canvas.itemconfig(self.city_text, fill=t["secondary"])
            self.canvas.itemconfig(self.creator_label, fill=t["secondary"])
            self.canvas.itemconfig(self.hint_text, fill=t["secondary"])
            self.canvas.itemconfig(self.astro_text, fill=t["glow"])
        except Exception as e:
            print(f"[Theme] error: {e}")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox", fieldbackground=t["bg"], background=t["accent"],
                        foreground=t["accent"], arrowcolor=t["glow"],
                        bordercolor=t["accent"], lightcolor=t["accent"],
                        darkcolor=t["accent"])
        style.map("TCombobox", fieldbackground=[("readonly", t["bg"])],
                  foreground=[("readonly", t["accent"])],
                  selectbackground=[("readonly", t["accent"])],
                  selectforeground=[("readonly", t["bg"])])
        self.fx.update_colors(t)

    def _apply_theme(self):
        self._apply_theme_with(THEMES[self.theme_name])

    def _smooth_transition(self, target_theme_name, duration_ms=500, steps=20):
        if self._transitioning: return
        self._transitioning = True
        old = THEMES[self.theme_name]; new = THEMES[target_theme_name]
        step_ms = max(duration_ms // steps, 10)
        def do_step(i):
            if i > steps:
                self.theme_name = target_theme_name
                self._apply_theme()
                self._transitioning = False
                self._save_settings()
                return
            k = i / steps
            temp = {key: blend(old[key], new[key], k) for key in old}
            self._apply_theme_with(temp)
            self.root.after(step_ms, lambda: do_step(i+1))
        do_step(0)

    def _update_lang_texts(self):
        L = LANGS[self.lang]
        self.search_label.configure(text=L["search"])
        self.theme_label.configure(text=L["theme"])
        self.lang_label.configure(text=L["lang"])
        self.fx_label.configure(text=L["fx"])
        self.mode_btn.configure(text=L["city_btn"] if self.mode=="zone" else L["zone_btn"])
        try:
            self.canvas.itemconfig(self.hint_text, text=L["hint"])
            self.canvas.itemconfig(self.creator_label, text="⚡ Created by  W e b 0 f ⚡")
        except Exception as e:
            print(f"[Lang] error: {e}")

    def _on_fx_change(self, _):
        self.fx_mode = FX_LABELS.get(self.fx_var.get(), "stars")
        self.fx.set_mode(self.fx_mode)
        # Пересоздаём частицы под выбранный режим
        w = self.canvas.winfo_width() or 1300
        h = self.canvas.winfo_height() or 820
        self.fx.resize(w, h)
        self._save_settings()

    def _animate_bg(self):
        try:
            self.fx.draw()
        except Exception as e:
            print(f"[FX] error: {e}")
        self.root.after(40, self._animate_bg)

    def _toggle_rainbow(self):
        self.rainbow = not self.rainbow; self._save_settings()

    def _toggle_mode(self):
        if not CITIES_AVAILABLE: return
        self.mode = "zone" if self.mode == "city" else "city"
        self._update_lang_texts(); self._refresh_list()

    def _on_theme(self, _):
        target = self.theme_var.get()
        if target != self.theme_name:
            self._smooth_transition(target)

    def _on_lang(self, _):
        self.lang = self.lang_var.get()
        self._update_lang_texts(); self._refresh_list(); self._save_settings()

    def _random_theme(self):
        name = f"🎲 Случайная #{random.randint(1000,9999)}"
        THEMES[name] = random_neon_theme()
        self.theme_combo.configure(values=list(THEMES.keys()))
        self.theme_var.set(name)
        self._smooth_transition(name)

    def _refresh_list(self):
        q = self.search_var.get()
        self.listbox.delete(0, tk.END)
        L = LANGS[self.lang]
        if self.mode == "city" and self.city_db:
            results = self.city_db.search(q, limit=300)
            self._current_results = results
            for c in results:
                self.listbox.insert(tk.END, f"{c['name']}, {c['country']}")
            if not results: self.listbox.insert(tk.END, f"— {L['no_results']} —")
        else:
            ql = q.lower()
            results = [z for z in ALL_ZONES if ql in z.lower()] if q else ALL_ZONES
            results = results[:300]
            self._current_results = results
            for z in results: self.listbox.insert(tk.END, z.replace("_"," "))
            if not results: self.listbox.insert(tk.END, f"— {L['no_results']} —")

    def _on_list_select(self, _):
        sel = self.listbox.curselection()
        if not sel or sel[0] >= len(self._current_results): return
        item = self._current_results[sel[0]]
        if self.mode == "city" and self.city_db:
            tz = self.city_db.get_timezone(item)
            self.current_zone = tz
            self.current_label = f"{item['name']}, {item['country']}"
            self.current_city_info = item
        else:
            self.current_zone = item
            self.current_label = item.replace("_"," ")
            self.current_city_info = self.city_db.find_by_zone(item) if self.city_db else None
        self._save_settings(); self._update_astro()

    def _update_astro(self):
        try:
            info = self.astro.get_info(self.current_zone)
            moon = f"{info['moon_emoji']} {info['moon_name']}"
            day  = f"📅 {info['day_of_year']}/{info['total_days']}"
            wk   = f"🗓️ Нед. {info['week']}"
            self.canvas.itemconfig(self.astro_text, text=f"{moon}\n{day}\n{wk}")
        except Exception as e:
            print(f"[Astro] error: {e}")

    def _open_astro(self):
        L = LANGS[self.lang]; t = THEMES[self.theme_name]
        info = self.astro.get_info(self.current_zone)
        win = tk.Toplevel(self.root); win.title(L["astro_title"])
        win.geometry("420x420"); win.configure(bg=t["bg"]); win.transient(self.root)
        tk.Label(win, text=L["astro_title"], font=("Segoe UI",16,"bold"),
                 bg=t["bg"], fg=t["accent"]).pack(pady=(15,8))
        tk.Label(win, text=self.current_label, font=("Segoe UI",12,"italic"),
                 bg=t["bg"], fg=t["secondary"]).pack(pady=(0,15))
        tk.Label(win, text=info["moon_emoji"], font=("Segoe UI",64),
                 bg=t["bg"], fg=t["glow"]).pack(pady=(0,8))
        tk.Label(win, text=info["moon_name"], font=("Segoe UI",16,"bold"),
                 bg=t["bg"], fg=t["accent"]).pack(pady=(0,20))
        for label, value in [(L["astro_day"], f"{info['day_of_year']} / {info['total_days']}"),
                             (L["astro_week"], f"{info['week']}"),
                             (L["astro_left"], f"{info['days_left']}")]:
            row = tk.Frame(win, bg=t["bg"]); row.pack(fill=tk.X, padx=30, pady=4)
            tk.Label(row, text=label, font=("Segoe UI",11),
                     bg=t["bg"], fg=t["secondary"]).pack(side=tk.LEFT)
            tk.Label(row, text=value, font=("Segoe UI",12,"bold"),
                     bg=t["bg"], fg=t["accent"]).pack(side=tk.RIGHT)
        tk.Button(win, text="OK", command=win.destroy,
                  font=("Segoe UI",10,"bold"), bg=t["accent"], fg=t["bg"],
                  relief=tk.FLAT, padx=20, pady=5, cursor="hand2",
                  borderwidth=0).pack(pady=(15,20))

    def _open_alarm(self):
        L = LANGS[self.lang]; t = THEMES[self.theme_name]
        win = tk.Toplevel(self.root); win.title(L["alarm_title"])
        win.geometry("420x440"); win.configure(bg=t["bg"]); win.transient(self.root)
        tk.Label(win, text=L["alarm_title"], font=("Segoe UI",16,"bold"),
                 bg=t["bg"], fg=t["accent"]).pack(pady=(15,10))
        frame = tk.Frame(win, bg=t["bg"]); frame.pack()
        tk.Label(frame, text=L["alarm_time"], font=("Segoe UI",11),
                 bg=t["bg"], fg=t["accent"]).pack(side=tk.LEFT, padx=(0,6))
        time_var = tk.StringVar(value=datetime.now().strftime("%H:%M"))
        tk.Entry(frame, textvariable=time_var, font=("Segoe UI",12), width=8,
                 relief=tk.FLAT, bg=t["bg"], fg=t["accent"],
                 insertbackground=t["accent"], justify="center").pack(side=tk.LEFT, padx=(0,8))
        listbox = tk.Listbox(win, font=("Segoe UI",11), height=10,
                             bg=t["bg"], fg=t["accent"], relief=tk.FLAT,
                             selectbackground=t["secondary"],
                             selectforeground=t["bg"],
                             highlightthickness=0, borderwidth=0)
        def refresh():
            listbox.delete(0, tk.END)
            if not self.alarms: listbox.insert(tk.END, f"— {L['alarm_none']} —")
            for a in self.alarms:
                listbox.insert(tk.END, f"⏰  {a['time']}   {a.get('label','')}")
        def add():
            s = time_var.get().strip()
            try:
                h,m = s.split(":"); h,m = int(h),int(m)
                if not (0<=h<24 and 0<=m<60): raise ValueError
                self.alarms.append({"time":f"{h:02d}:{m:02d}","label":self.current_label})
                self.alarms.sort(key=lambda x:x["time"])
                refresh(); self._save_settings()
            except Exception:
                messagebox.showerror("Error","HH:MM (00:00 – 23:59)")
        def delete():
            sel = listbox.curselection()
            if not sel or not self.alarms: return
            idx = sel[0]
            if 0 <= idx < len(self.alarms):
                del self.alarms[idx]; refresh(); self._save_settings()
        tk.Button(frame, text=L["alarm_add"], command=add,
                  font=("Segoe UI",10,"bold"), relief=tk.FLAT,
                  bg=t["secondary"], fg=t["bg"], padx=10, pady=3,
                  cursor="hand2", borderwidth=0).pack(side=tk.LEFT)
        tk.Label(win, text=L["alarm_list"], font=("Segoe UI",11,"bold"),
                 bg=t["bg"], fg=t["accent"]).pack(pady=(15,5))
        listbox.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0,10))
        tk.Button(win, text=L["alarm_delete"], command=delete,
                  font=("Segoe UI",10,"bold"), relief=tk.FLAT,
                  bg=t["accent"], fg=t["bg"], padx=10, pady=5,
                  cursor="hand2", borderwidth=0).pack(pady=(0,15))
        refresh()

    def _check_alarms(self, now_local):
        hhmm = now_local.strftime("%H:%M")
        if now_local.second != 0 or hhmm == self._last_alarm_check: return
        for a in self.alarms:
            if a["time"] == hhmm:
                self._last_alarm_check = hhmm; self._fire_alarm(a); break

    def _fire_alarm(self, alarm):
        L = LANGS[self.lang]
        msg = L["alarm_fire"].format(city=alarm.get("label",""), time=alarm["time"])
        self.root.bell(); self._flash_until = 10
        self.root.after(50, lambda: messagebox.showinfo("Neon Clock", msg))

    def _open_stopwatch(self):
        L = LANGS[self.lang]; t = THEMES[self.theme_name]
        win = tk.Toplevel(self.root); win.title(L["stopwatch_title"])
        win.geometry("400x460"); win.configure(bg=t["bg"]); win.transient(self.root)
        tk.Label(win, text=L["stopwatch_title"], font=("Segoe UI",16,"bold"),
                 bg=t["bg"], fg=t["accent"]).pack(pady=(15,12))
        tk.Label(win, text="⏱ Stopwatch", font=("Segoe UI",12,"bold"),
                 bg=t["bg"], fg=t["glow"]).pack()
        sw_display = tk.Label(win, text="00:00.00", font=("Consolas",36,"bold"),
                              bg=t["bg"], fg=t["accent"])
        sw_display.pack(pady=(5,10))
        sw_state = {"running":False,"start":0.0,"elapsed":0.0,"laps":[]}
        lap_display = tk.Label(win, text="", font=("Consolas",10),
                               bg=t["bg"], fg=t["secondary"], justify="left")
        def fmt(s):
            m = int(s//60); sec = s - m*60
            return f"{m:02d}:{sec:05.2f}"
        def sw_tick():
            if sw_state["running"]:
                cur = time.time() - sw_state["start"] + sw_state["elapsed"]
                sw_display.configure(text=fmt(cur)); win.after(50, sw_tick)
        def sw_start():
            if not sw_state["running"]:
                sw_state["running"] = True; sw_state["start"] = time.time(); sw_tick()
        def sw_stop():
            if sw_state["running"]:
                sw_state["elapsed"] += time.time() - sw_state["start"]
                sw_state["running"] = False
        def sw_reset():
            sw_state.update({"running":False,"start":0.0,"elapsed":0.0,"laps":[]})
            sw_display.configure(text="00:00.00"); lap_display.configure(text="")
        def sw_lap():
            if sw_state["running"]:
                cur = time.time() - sw_state["start"] + sw_state["elapsed"]
                sw_state["laps"].append(cur)
                txt = "\n".join(f"{L['stopwatch_lap']}{fmt(x)}"
                                for x in sw_state["laps"][-8:])
                lap_display.configure(text=txt)
        sw_btns = tk.Frame(win, bg=t["bg"]); sw_btns.pack()
        for txt, cmd in [(L["sw_start"], sw_start), (L["sw_stop"], sw_stop),
                         (L["sw_reset"], sw_reset), (L["stopwatch_lap"], sw_lap)]:
            tk.Button(sw_btns, text=txt, command=cmd, font=("Segoe UI",10,"bold"),
                      bg=t["secondary"], fg=t["bg"], relief=tk.FLAT, padx=8, pady=3,
                      cursor="hand2", borderwidth=0).pack(side=tk.LEFT, padx=3)
        lap_display.pack(pady=(8,10))
        tk.Label(win, text="⏳ Timer", font=("Segoe UI",12,"bold"),
                 bg=t["bg"], fg=t["glow"]).pack(pady=(10,4))
        timer_display = tk.Label(win, text="00:00", font=("Consolas",28,"bold"),
                                 bg=t["bg"], fg=t["accent"])
        timer_display.pack(pady=(2,6))
        tframe = tk.Frame(win, bg=t["bg"]); tframe.pack()
        tk.Label(tframe, text=L["timer_set"], font=("Segoe UI",10),
                 bg=t["bg"], fg=t["accent"]).pack(side=tk.LEFT, padx=(0,4))
        mins_var = tk.StringVar(value="5")
        tk.Entry(tframe, textvariable=mins_var, width=5, font=("Segoe UI",11),
                 bg=t["bg"], fg=t["accent"], insertbackground=t["accent"],
                 relief=tk.FLAT, justify="center").pack(side=tk.LEFT)
        timer_state = {"running":False,"end":0.0}
        def timer_tick():
            if not timer_state["running"]: return
            left = timer_state["end"] - time.time()
            if left <= 0:
                timer_display.configure(text="00:00")
                timer_state["running"] = False
                self.root.bell(); self.root.bell()
                messagebox.showinfo("Neon Clock", L["timer_done"]); return
            m = int(left//60); s = int(left - m*60)
            timer_display.configure(text=f"{m:02d}:{s:02d}")
            win.after(200, timer_tick)
        def timer_start():
            try:
                mins = float(mins_var.get())
                if mins <= 0: raise ValueError
            except Exception:
                messagebox.showerror("Error"," > 0"); return
            timer_state["running"] = True
            timer_state["end"] = time.time() + mins*60
            timer_tick()
        def timer_cancel():
            timer_state["running"] = False
            timer_display.configure(text="00:00")
        tbtns = tk.Frame(win, bg=t["bg"]); tbtns.pack(pady=(6,12))
        tk.Button(tbtns, text=L["timer_start"], command=timer_start,
                  font=("Segoe UI",10,"bold"), bg=t["accent"], fg=t["bg"],
                  relief=tk.FLAT, padx=10, pady=3, cursor="hand2",
                  borderwidth=0).pack(side=tk.LEFT, padx=3)
        tk.Button(tbtns, text=L["timer_cancel"], command=timer_cancel,
                  font=("Segoe UI",10,"bold"), bg=t["secondary"], fg=t["bg"],
                  relief=tk.FLAT, padx=10, pady=3, cursor="hand2",
                  borderwidth=0).pack(side=tk.LEFT, padx=3)

    # ============ ЗАМЕТКИ ============
    def _open_notes(self):
        L = LANGS[self.lang]; t = THEMES[self.theme_name]
        win = tk.Toplevel(self.root); win.title(L["notes_title"])
        win.geometry("560x600"); win.configure(bg=t["bg"]); win.transient(self.root)

        tk.Label(win, text=L["notes_title"], font=("Segoe UI",16,"bold"),
                 bg=t["bg"], fg=t["accent"]).pack(pady=(15,8))
        tk.Label(win, text=L["notes_auto"], font=("Segoe UI",9,"italic"),
                 bg=t["bg"], fg=t["secondary"]).pack(pady=(0,8))

        text_frame = tk.Frame(win, bg=t["bg"]); text_frame.pack(fill=tk.BOTH, expand=True, padx=15)
        text_widget = tk.Text(text_frame, font=("Consolas", 11),
                              bg=t["bg"], fg=t["accent"], insertbackground=t["accent"],
                              relief=tk.FLAT, wrap=tk.WORD, undo=True,
                              highlightthickness=1, highlightbackground=t["secondary"])
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb = tk.Scrollbar(text_frame, command=text_widget.yview)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.configure(yscrollcommand=sb.set)

        # Загружаем сохранённый текст
        text_widget.insert("1.0", self.notes.load())

        status = tk.Label(win, text="", font=("Segoe UI", 10, "italic"),
                          bg=t["bg"], fg=t["glow"])
        status.pack(pady=(6, 4))

        dirty = {"flag": False, "last_save": time.time()}

        def mark_dirty(event=None):
            dirty["flag"] = True

        text_widget.bind("<KeyRelease>", mark_dirty)

        def save_now(show_status=True):
            txt = text_widget.get("1.0", "end-1c")
            if self.notes.save(txt):
                dirty["flag"] = False
                dirty["last_save"] = time.time()
                if show_status:
                    status.configure(text=f"✓ {L['notes_saved']}  ({datetime.now().strftime('%H:%M:%S')})")
            else:
                status.configure(text="✗ Save failed")

        def clear_all():
            if messagebox.askyesno("Clear", "Удалить все заметки?"):
                text_widget.delete("1.0", tk.END)
                save_now()

        def auto_save():
            if win.winfo_exists():
                if dirty["flag"] and (time.time() - dirty["last_save"] > 3):
                    save_now(show_status=False)
                win.after(1000, auto_save)

        def on_close():
            save_now(show_status=False)
            win.destroy()

        win.protocol("WM_DELETE_WINDOW", on_close)

        btns = tk.Frame(win, bg=t["bg"]); btns.pack(pady=(4, 12))
        tk.Button(btns, text=L["notes_save"], command=save_now,
                  font=("Segoe UI",10,"bold"), bg=t["accent"], fg=t["bg"],
                  relief=tk.FLAT, padx=10, pady=4, cursor="hand2",
                  borderwidth=0).pack(side=tk.LEFT, padx=3)
        tk.Button(btns, text=L["notes_clear"], command=clear_all,
                  font=("Segoe UI",10,"bold"), bg=t["secondary"], fg=t["bg"],
                  relief=tk.FLAT, padx=10, pady=4, cursor="hand2",
                  borderwidth=0).pack(side=tk.LEFT, padx=3)

        text_widget.focus_set()
        auto_save()

    # ============ ТРЕЙ ============
    def _minimize_to_tray(self):
        if not TRAY_AVAILABLE:
            messagebox.showinfo("Tray", LANGS[self.lang]["tray_not_available"] +
                                "\n\npip install pystray Pillow")
            return
        self._save_settings()
        def make_icon():
            img = Image.new("RGBA",(64,64),(0,0,0,0))
            d = ImageDraw.Draw(img); t = THEMES[self.theme_name]
            d.ellipse([8,8,56,56], fill=t["accent"])
            d.ellipse([20,20,44,44], fill=t["bg"])
            d.line([32,32,32,20], fill=t["glow"], width=3)
            d.line([32,32,44,32], fill=t["glow"], width=3)
            return img
        def on_show(icon, item): self.root.after(0, self._restore_from_tray)
        def on_quit(icon, item):
            icon.stop(); self.tray_icon = None
            self.root.after(0, self._on_close)
        menu = pystray.Menu(
            pystray.MenuItem("Показать", on_show, default=True),
            pystray.MenuItem("Выход", on_quit))
        self.tray_icon = pystray.Icon("NeonClock", make_icon(),
                                      "Neon Clock — by Web0f", menu)
        self.root.withdraw()
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def _restore_from_tray(self):
        if self.tray_icon:
            try: self.tray_icon.stop()
            except Exception: pass
            self.tray_icon = None
        self.root.deiconify(); self.root.lift(); self.root.focus_force()

    def toggle_fullscreen(self, _=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)

    def exit_fullscreen(self, _=None):
        self.fullscreen = False
        self.root.attributes("-fullscreen", False)

    def _tick(self):
        try:
            now = datetime.now(ZoneInfo(self.current_zone)); now_local = datetime.now()
        except Exception:
            now = now_local = datetime.now()
        try:
            self.canvas.itemconfig(self.hm_text, text=now.strftime("%H:%M"))
            self.canvas.itemconfig(self.sec_text, text=now.strftime("%S"))
            self.canvas.itemconfig(self.date_text, text=now.strftime("%d.%m.%Y  •  %A"))
            self.canvas.itemconfig(self.city_text,
                                   text=f"{self.current_label}   [{self.current_zone}]")
            self.canvas.tag_raise("text_layer")
        except Exception as e:
            print(f"[Tick] error: {e}")

        if now_local.second == 0:
            self._update_astro()

        if self.rainbow:
            self.rainbow_hue = (self.rainbow_hue + 0.005) % 1.0
            h = self.rainbow_hue
            ar,ag,ab = colorsys.hls_to_rgb(h, 0.55, 1.0)
            gr,gg,gb = colorsys.hls_to_rgb((h+0.33)%1.0, 0.75, 1.0)
            sr,sg,sb = colorsys.hls_to_rgb((h+0.66)%1.0, 0.65, 1.0)
            accent = f"#{int(ar*255):02x}{int(ag*255):02x}{int(ab*255):02x}"
            glow   = f"#{int(gr*255):02x}{int(gg*255):02x}{int(gb*255):02x}"
            secondary = f"#{int(sr*255):02x}{int(sg*255):02x}{int(sb*255):02x}"
            try:
                self.canvas.itemconfig(self.hm_text, fill=accent)
                self.canvas.itemconfig(self.sec_text, fill=glow)
                self.canvas.itemconfig(self.date_text, fill=glow)
                self.canvas.itemconfig(self.city_text, fill=secondary)
                self.canvas.itemconfig(self.creator_label, fill=secondary)
                self.canvas.itemconfig(self.astro_text, fill=glow)
            except Exception as e:
                print(f"[Rainbow] error: {e}")
        else:
            self.pulse += 0.15
            k = (math.sin(self.pulse)+1)/2
            base = THEMES[self.theme_name]["glow"]
            accent = THEMES[self.theme_name]["accent"]
            if self._flash_until > 0:
                self._flash_until -= 1
                self._flash_state = not self._flash_state
                color = "#ff0000" if self._flash_state else "#ffffff"
                try:
                    self.canvas.itemconfig(self.sec_text, fill=color)
                    self.canvas.itemconfig(self.hm_text, fill=color)
                except Exception: pass
            else:
                try:
                    self.canvas.itemconfig(self.sec_text, fill=blend(base, accent, k))
                    self.canvas.itemconfig(self.hm_text, fill=accent)
                    # Подпись создателя мерцает
                    pp = (math.sin(self.pulse * 0.8) + 1) / 2
                    self.canvas.itemconfig(self.creator_label,
                                           fill=blend(base, accent, pp))
                except Exception: pass
        self._check_alarms(now_local)
        self.root.after(1000, self._tick)


# ============ ЗАПУСК ============
def launch_main(root):
    root.deiconify(); root.state("normal"); root.lift()
    root.attributes("-topmost", True)
    root.after(700, lambda: root.attributes("-topmost", False))
    root.focus_force()
    app = NeonClock(root)
    print("[OK] Neon Clock успешно запущен")
    return app


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    root.title("Neon Clock — by Web0f")
    root.geometry("1300x820")

    holder = {"app": None}
    def on_splash_finish():
        holder["app"] = launch_main(root)

    SplashScreen(root, on_finish=on_splash_finish, duration_ms=8000)
    root.mainloop()
