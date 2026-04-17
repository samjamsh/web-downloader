import os
import json
import time
import threading
from datetime import datetime
import urllib.parse
import tempfile

try:
    import requests
except Exception as e:
    raise SystemExit("Instale requests: pip install requests")

try:
    import yt_dlp
    has_ytdlp = True
except:
    has_ytdlp = False

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# configs e paths
USERNAME = os.getlogin() if hasattr(os, "getlogin") else None
DEFAULT_DOWNLOAD_DIR = os.path.join("C:/Users", USERNAME or "", "Downloads", "Wget")
os.makedirs(DEFAULT_DOWNLOAD_DIR, exist_ok=True)
LOG_DIR = os.path.join(DEFAULT_DOWNLOAD_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "download_log.txt")
HISTORY_FILE = os.path.join(DEFAULT_DOWNLOAD_DIR, "url_history.json")

COOKIES_DATA = '''# Netscape HTTP Cookie File
# https://curl.haxx.se/rfc/cookie_spec.html
# This is a generated file! Do not edit.

.youtube.com	TRUE	/	TRUE	1795428055	LOGIN_INFO	AFmmF2swRAIgZMxxohvC7eEBxKDFk2UYCZOVvqvmBXyS4Po382vY3sQCIFhbPKMtPVWo2PoQG4SEu60igZf0ZYeAy-SayWTWmhU1:QUQ3MjNmekdmRF9IbTY4VTlFV09vX01lRzFJNkxDakIxSzZDa1RLSU9LQW01QXktZS11VzRRQXJZS3FaOVZHZm1DR01PQW9yaDlYZllXcnAyTEtzaWFDQ1k4cXpUSHNFOGsySFpPaHpvMGhocGRDWmJ5SGVZNmdybHdxN1BIb1lpNVdrX05uZjRtWEpoZGswMDFreFlJS1R0Um1feVoyazFR
.youtube.com	TRUE	/	TRUE	1809985286	PREF	f4=4000000&f6=40000000&tz=Africa.Maputo&f5=20000&f7=100
.youtube.com	TRUE	/	FALSE	1807699093	HSID	A_n9qZq7jJba-b3VM
.youtube.com	TRUE	/	TRUE	1807699093	SSID	AnFuohKDFJJnMi4r6
.youtube.com	TRUE	/	FALSE	1807699093	APISID	uQk3g3OLILOppcUa/Av50SNmyMd-ZXt6oa
.youtube.com	TRUE	/	TRUE	1807699093	SAPISID	BfPm0evUQro3pmX7/A5EWIVaVAZjR19-BV
.youtube.com	TRUE	/	TRUE	1807699093	__Secure-1PAPISID	BfPm0evUQro3pmX7/A5EWIVaVAZjR19-BV
.youtube.com	TRUE	/	TRUE	1807699093	__Secure-3PAPISID	BfPm0evUQro3pmX7/A5EWIVaVAZjR19-BV
.youtube.com	TRUE	/	FALSE	1807699093	SID	g.a0007gjS3jxMKERa7SdARkU5vyDXmWNfC5rvifm-x2MP52T3lFfQbgaR24nwkK-XuxeU1dugAgACgYKAbQSARUSFQHGX2MijmkcWxCX6TeQ1jXqK45zWRoVAUF8yKqOGJymVpwO70FfRmJYMmXN0076
.youtube.com	TRUE	/	TRUE	1807699093	__Secure-1PSID	g.a0007gjS3jxMKERa7SdARkU5vyDXmWNfC5rvifm-x2MP52T3lFfQYImbRZP4uRP1eL90gjMEMQACgYKAbESARUSFQHGX2Mi1jKQGsPXCnnYjalkaO1LMRoVAUF8yKpwwDg2dS4yaoR4Vtcvb56t0076
.youtube.com	TRUE	/	TRUE	1807699093	__Secure-3PSID	g.a0007gjS3jxMKERa7SdARkU5vyDXmWNfC5rvifm-x2MP52T3lFfQolcfdYSluNQ6UjGBovhj3wACgYKAYMSARUSFQHGX2Mi_hmjkylQpFwQELG7WBAynxoVAUF8yKomclsPDnRsd_2W8aDMy49o0076
.youtube.com	TRUE	/	TRUE	1809296805	__Secure-YENID	14.YTE=c09TVqGQ4rSz9yGomBYnA11m9p4JQVjoh_zq93kiM6e4BRUqdkdDVXqA9TpU0Gf44i2aqxVaw_eJ4GYzT-3mg8O3argY6RkwlhZHO0j0GA2Nac_tOg4bsTrGCfrwCwHNM-xwNxlqwIuFXDyeStije20IFMGWoUvm6ocLnxkgFB4PAkX80jfT4-V5BycG9HfNfqvmbjr_VgCnbex_xg-P7mvbzi-euTc8PMPx3ij3kxDTOd1g-Zy9sIUXVZvt013jZ4K0ciHaYEbn_Qox3lUdahEFHJJCM48XDqCBvr25Mf2ZE-R37bw5KCmOcymxTKmC4bGX8vz7uhOFW7lafM-CIg
.youtube.com	TRUE	/	TRUE	1790756060	VISITOR_PRIVACY_METADATA	CgJaVxIEGgAgYw%3D%3D
.youtube.com	TRUE	/	TRUE	1791165551	NID	530=R2n90yg7fq7kXlE0YmfzXzVXLksCWSzzCauQRzrtHwEvwDpRc0Bm85Nb7XDypwtfDs2cDYkVTluvlkJrHDnfOd4goKdjEOlB0BeGd0aZrLJAYWdXYaBNwOKRBRv4ajNtMCbvQjht6rbMap775FOtvZZvoMvG5InpKVrUb0uHcvDlPESTcpTKy-kEC1eID7UhPr1Etl7iKrBAPJeli6fU21GT_k3SAponKLCbE2HlJ8I4Yg
.youtube.com	TRUE	/	TRUE	1806961734	__Secure-1PSIDTS	sidts-CjUBWhotCRO69BAMN3ix4RyltP9XEoeOwqxkCf7KsLw3zhgt8yKXHegPRhTPTg6OmPNga8htLxAA
.youtube.com	TRUE	/	TRUE	1806961734	__Secure-3PSIDTS	sidts-CjUBWhotCRO69BAMN3ix4RyltP9XEoeOwqxkCf7KsLw3zhgt8yKXHegPRhTPTg6OmPNga8htLxAA
.youtube.com	TRUE	/	FALSE	1806961735	SIDCC	AKEyXzVVYAH9MeFuZF0V16-gSBIX6kZTdM552Urwz0Fa3eD1E3-ZCK_j6BkJ8ag1VuJsco7hiic
.youtube.com	TRUE	/	TRUE	1806961735	__Secure-1PSIDCC	AKEyXzU1dmoLvZLuXQY4TZPHyqYoDsgTL6nVNDR1IGgZKd1U3QVT3surJ4zX4n1_BS58PkkG7_s
.youtube.com	TRUE	/	TRUE	1806961735	__Secure-3PSIDCC	AKEyXzUBksWGdv5fZjRDFqagWdAA3yrXAhoGHpwDxecUOMOkdzfXIIIc_l9IMKLOqsDFVFXzq7g
.youtube.com	TRUE	/	TRUE	1790977282	VISITOR_INFO1_LIVE	EoBfY9wc8cA
.youtube.com	TRUE	/	TRUE	1790977282	VISITOR_PRIVACY_METADATA	CgJaVxIEGgAgYw%3D%3D
.youtube.com	TRUE	/	TRUE	0	YSC	03tLBLzNXNk
.youtube.com	TRUE	/	TRUE	1790895661	__Secure-ROLLOUT_TOKEN	CKDF2OrT8pjZ5wEQ1MTkhrytkAMYhNuWwqbVkwM%3D
.youtube.com	TRUE	/	TRUE	1790976527	__Secure-YNID	17.YT=R8UnoSR8l8NYCSEi1yQGNo1hOr1dx1KNgaxScGvhvBl3QE_vlZyCDlUjPSeoo6rXRYve1o_qMeNPSE15yFtCpu28qPyoOgFlWERVD2Ns3qNRTv9dVCMqWoIaHfJhvANLdYQWYaUst-GEJwLP5AbMx0ehbk3za03Uki8FHGZi_Y7bjDHRyHfyIrCZCf7n_C2yja1ICCvuGiMd86VQPKZf98sGJpSjqlqX5sngD4Q_aGQmnVQhjvMeQ7_SO7qDDrYpzuC6AOZZq7E0fxvwBtwzD9a8x6jOPTVU5tOO3GE0tX7bwArx7HsqeguSU0KQpyrz9U7K4bHFbClvGf2i6bgV1Q
'''

def get_temp_cookies():
    # cria um arquivo temporario que o windows reconheca como real
    temp_dir = tempfile.gettempdir()
    cookie_path = os.path.join(temp_dir, "ytdlp_temp_cookies.txt")
    print(f"cookie_path -> {cookie_path}")
    
    with open(cookie_path, "w", encoding="utf-8") as f:
        f.write(COOKIES_DATA)
    
    return cookie_path

cookie_path = get_temp_cookies();

# Utils
def log_event(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {msg}\n")

def format_size(b):
    if b is None:
        return "unknown"
    b = int(b)
    if b < 1024: return f"{b} B"
    if b < 1024**2: return f"{b/1024:.1f} KB"
    if b < 1024**3: return f"{b/1024**2:.2f} MB"
    return f"{b/1024**3:.2f} GB"

def is_valid_url(url):
    url = url.strip()
    parsed = urllib.parse.urlparse(url)
    return parsed.scheme in ("http", "https") and parsed.netloc != ""

def save_history(url):
    try:
        hist = []
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                hist = json.load(f)
        if url in hist:
            hist.remove(url)
        hist.insert(0, url)
        hist = hist[:20]
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(hist, f, ensure_ascii=False, indent=2)
    except Exception as e:
        log_event(f"Erro salvando histórico: {e}")

def load_history():
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except:
        pass
    return []

class DownloadTask:
    def __init__(self, parent, url, folder, filename=None, item_id=None, manager=None):
        self.parent = parent  # referência ao app (UI)
        self.url = url
        self.folder = folder
        self.provided_filename = filename
        self.item_id = item_id
        self.manager = manager
        #self._lock = threading.Lock()
        self._total_size = None
        self._downloaded = 0
        self._start_time = None
        self._part_path = None
        self._final_path = None
        self.status = "Queued"

        r = requests.head(url)
        size = r.headers.get("Content-Length")

    def _update_ui(self):
        # atualiza Treeview via root.after
        if self.item_id:
            percentage = (self._downloaded/(self._total_size) * 100) if self._total_size else 1
            if percentage > 100: percentage = 100

            pct_text = f"{percentage:.1f}%" if self._total_size else "-"  # {(self._downloaded/percentage):.1f}%" if self._total_size else "-"
            speed = (self._downloaded / max(1, time.time()-self._start_time)) if self._start_time else 0
            speed_text = f"{speed/1024:.1f} KB/s"
            self.parent.root.after(0, lambda: self.parent.update_task_row(self.item_id,
                                                                          progresso=pct_text,
                                                                          velocidade=speed_text,
                                                                          status=self.status))
    def _run(self):
        try:
            self.status = "Starting"
            self._update_ui()
            save_history(self.url)

            # filename
            if self.provided_filename:
                out_name = self.provided_filename
            else:
                parsed = urllib.parse.urlparse(self.url)
                fname = os.path.basename(parsed.path)
                out_name = fname if fname else "downloaded_file"

            final_path = os.path.join(self.folder, out_name)
            part_path = final_path + ".part"
            self._part_path = part_path
            self._final_path = final_path

            # create folder
            os.makedirs(self.folder, exist_ok=True)

            # resume if part exists
            downloaded = 0
            if os.path.exists(part_path):
                downloaded = os.path.getsize(part_path)

            headers = {"User-Agent": "Mozilla/5.0"}
            if downloaded:
                headers["Range"] = f"bytes={downloaded}-"

            #print(f"downloaded before: {downloaded}")
            self._start_time = time.time()
            with requests.get(self.url, headers=headers, stream=True, timeout=15) as r:
                r.raise_for_status()
                print(f"content -> {len(r.content)}")
                total = r.headers.get("Content-Length")
                #print(f"total from headers: {total}")
                if total is not None:
                    total = int(total) + downloaded if "Range" in headers else int(total)
                self._total_size = total
                #print(f"total after: {total}")
                self._downloaded = downloaded
                #print(f"downloaded after: {downloaded}")

                # if filename from content-disposition
                if not self.provided_filename:
                    cd = r.headers.get("content-disposition")
                    if cd and "filename=" in cd:
                        try:
                            fn = cd.split("filename=")[1].strip(' "')
                            final_path = os.path.join(self.folder, fn)
                            part_path = final_path + ".part"
                            self._part_path = part_path
                            self._final_path = final_path
                        except:
                            pass

                mode = "ab" if downloaded else "wb"
                chunk_size = 8192
                self.status = "Downloading"
                self._update_ui()

                with open(part_path, mode) as f:
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        if self._stop_event.is_set():
                            self.status = "Cancelled"
                            log_event(f"Cancelled: {self.url}")
                            return
                        # handle pause
                        while self._pause_event.is_set():
                            time.sleep(0.2)
                            if self._stop_event.is_set():
                                self.status = "Cancelled"
                                log_event(f"Cancelled while paused: {self.url}")
                                return

                        if chunk:
                            f.write(chunk)
                            self._downloaded += len(chunk)
                            print(f"new downloaded -> {self._downloaded}")
                            # update ui
                            self._update_ui()

                # rename part to final
                try:
                    if os.path.exists(final_path):
                        base, ext = os.path.splitext(final_path)
                        i = 1
                        while os.path.exists(f"{base}_{i}{ext}"):
                            i += 1
                        final_path = f"{base}_{i}{ext}"
                    os.replace(part_path, final_path)
                except Exception as e:
                    log_event(f"Erro renomeando .part: {e}")

                self.status = "Completed"
                self._update_ui()
                log_event(f"Completed: {self.url} -> {final_path} | {format_size(self._total_size)}")


        except requests.HTTPError as he:
            self.status = f"HTTP {he.response.status_code}"
            self._update_ui()
            log_event(f"HTTPError {he.response.status_code} for {self.url}")
        except requests.Timeout:
            self.status = "Timeout"
            self._update_ui()
            log_event(f"Timeout: {self.url}")
        except requests.RequestException as re:
            self.status = "RequestError"
            self._update_ui()
            log_event(f"RequestException: {re} for {self.url}")
        except Exception as e:
            self.status = "Error"
            self._update_ui()
            log_event(f"Exception: {e} for {self.url}")

# UI principal
class WDDApp:
    global tcolor
    tcolor = "#414245" # top color

    global t_color
    t_color = "#39393b"  # top controls color

    global c_color
    c_color = "#323335" # configure color

    def __init__(self, root):
        self.root = root
        self.root.title("Web Data Downloader - WDD (Full)")
        self.root.geometry("900x650")
        self.root.resizable(True, True)
        self.root.configure(bg="#323335")
        self.tasks = {}  # item_id -> DownloadTask
        self.titles = [[None, None]]
        self.title_ = None
        
        icon_path = r"C:\projects\webGet\icon.ico"  # caminho do .ico
        if os.path.exists(icon_path):
            root.iconbitmap(icon_path)

        # top controls
        top_frame = tk.Frame(root, bg="#284850")
        top_frame.pack(fill="x", padx=14, pady=8)

        tk.Label(top_frame, text="URL:", fg="#fff", bg="#284850", font=("Consolas", 11)).pack(side="left")
        self.url_var = tk.StringVar()
        hist = load_history()
        self.url_combo = ttk.Combobox(top_frame, textvariable=self.url_var, values=hist, width=70)
        self.url_combo.pack(side="left", padx=6)

        # coloca o cursor automaticamente no campo de URL
        self.url_combo.focus_set()

        paste_btn = tk.Button(top_frame, text="📋", command=self.paste_clipboard, width=3, bg="#303F42")
        paste_btn.pack(side="left")

        tk.Label(top_frame, text="Folder:", fg="#fff", bg="#284850", font=("Consolas", 11)).pack(side="left", padx=(10,0))
        self.folder_var = tk.StringVar(value=DEFAULT_DOWNLOAD_DIR)
        tk.Entry(top_frame, textvariable=self.folder_var, width=30, bg="#8a999e").pack(side="left", padx=6)
        tk.Button(top_frame, text="Browse Now", command=self.browse_folder, bg="#3F666F").pack(side="right")

        # filename optional
        # Frame para filename na mesma linha
        filename_frame = tk.Frame(root, bg="#3e565d")
        filename_frame.pack(fill="x", padx=14, pady=(0,8))

        tk.Label(filename_frame, text="Filename (optional):", fg="#fff", bg="#3e565d", font=("Consolas", 10)).pack(side="left")

        self.filename_var = tk.StringVar()
        tk.Entry(filename_frame, textvariable=self.filename_var, bg="#8a999e", width=54).pack(side="left", padx=6)

        tk.Button(filename_frame, text="Open Folder", command=self.open_selected_folder, bg="#3F666F").pack(side="right")

        # control buttons
        controls = tk.Frame(root, bg="#325964")
        controls.pack(fill="x", padx=14)

        tk.Button(controls, text="Start Download", command=self.choose_download, width=21, bg="#303F42").pack(side="left")
        #tk.Button(controls, text="Start as Crawler (page)", command=self.start_crawler, width=18, bg="#303F42").pack(side="left", padx=6)
        '''self.yt_btn = tk.Button(controls, text="Download (yt-dlp)", command=self.choose_download, width=16)
        self.yt_btn.pack(side="left") '''
        
        if not has_ytdlp:
            self.yt_btn.configure(state="disabled", text="yt-dlp not found")

        tk.Button(controls, text="Clear History", command=self.clear_history, bg="#303F42").pack(side="right")

        # theme toggle
        self.theme = "dark"
        self.theme_btn = tk.Button(controls, text=" 🌙 ", command=self.toggle_theme, width=3, bg="#303F42")
        self.theme_btn.pack(side="right", padx=6)

        # treeview for tasks
        cols = ("File", "Progress", "Speed", "Status")
        self.tree = ttk.Treeview(root, columns=cols, show="headings", height=18)
        
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=200, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=14, pady=13)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # row action buttons
        self.row_actions = tk.Frame(root, bg="#3D5562")  # bg="#12252A"
        self.row_actions.pack(fill="x", padx=14, pady=(0,10))

        # bottom status
        self.status_label = tk.Label(self.row_actions, text="Ready", bg="#3D5562")  # bg="#12252A"
        self.status_label.pack(anchor="w", padx=12, pady=4)

        # load theme colors
        self.apply_theme("dark")

    # ---------- UI helpers ----------
    def paste_clipboard(self):
        try:
            txt = self.root.clipboard_get()
            self.url_var.set(txt)
            self.url_combo.focus_set()
        except:
            pass

    def on_tree_select(self, event):
        selected_items = self.tree.selection()
        if selected_items:
            item_id = selected_items[0]
            # obtem os valores da linha (File, Progress, Speed, Status)
            values = self.tree.item(item_id, "values")
            print(f"item-id: [{int(item_id[1:])} | {item_id}]  --  title: {self.title_}")
            id = int(item_id[1:])

            print(f"titles({self.titles[id][1]}) == id({id})  ? {self.titles[id][1] == id}")
            if self.titles[id][1] == id:
                self.title_ = self.titles[id][0]
                print(f"title = {self.title_}")
            else:
                url = self.url_var.get()
                filename = self.filename_var.get().strip() or os.path.basename(urllib.parse.urlparse(url).path)
                self.title_ = filename
                print(f"else title <- {filename}")

            if values:
                filename = values[0]
                self.status_label.config(text=f"Selected: {self.title_ if self.title_ else filename}")

    def browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.folder_var.get())
        if folder:
            self.folder_var.set(folder)

    def toggle_theme(self):
        self.theme = "light" if self.theme == "dark" else "dark"
        self.apply_theme(self.theme)

    def apply_theme(self, mode):
        fgb = "black"
        if mode == "light":
            #fgb = "black"
            bg="#ffffff"; fg="#343030"; accent="#3D5562" #"#b8d7ec"
            self.theme_btn.config(text=" ☀️ ")
            self.row_actions.config(bg="#3D5562")
            self.status_label.config(bg="#3D5562")
            
        else:
            fgb = "white"
            bg="#0b0c10"; fg="#1A1D1C"; accent="#3D5562"
            self.theme_btn.config(text=" 🌙 ")
            self.row_actions.config(bg="#12252A")  # bg="#12252A"
            self.status_label.config(bg="#12252A")  #bg="#12252A"

        self.root.configure(bg=bg)
        # update a few widgets
        for w in (self.url_combo, ):
            try:
                w.configure(background=bg, foreground=fg)
            except:
                pass

        # Treeview style colors (simple)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", background=bg, fieldbackground=bg, foreground=fgb)
        style.configure("Treeview.Heading", background=accent, foreground="#000000")

    # ---------- task management ----------
    def add_download(self):
        url = self.url_var.get().strip()
        folder = self.folder_var.get().strip() or DEFAULT_DOWNLOAD_DIR
        filename = self.filename_var.get().strip() or None
        self.title_ = filename
        #print(f"filename -> {filename}")

        if not url:
            messagebox.showerror("Error", "Please insert an URL.")
            return
        if not is_valid_url(url):
            messagebox.showerror("Error", "Invalid URL.")
            return
    
        # add row
        display_name = filename if filename else os.path.basename(urllib.parse.urlparse(url).path) or url
        item = self.tree.insert("", "end", values=(display_name, "0%", "0 KB/s", "Queued"))

        task = DownloadTask(parent=self, url=url, folder=folder, filename=filename, item_id=item, manager=self)
        self.tasks[item] = task
        task.start()
        self.status_label.config(text=f"Started: {url}")
        log_event(f"Queued: {url} -> {folder}")


    def update_task_row(self, item_id, progresso=None, velocidade=None, status=None):
        try:
            vals = list(self.tree.item(item_id, "values"))
            if progresso is not None:
                vals[1] = progresso
            if velocidade is not None:
                vals[2] = velocidade
            if status is not None:
                vals[3] = status
            self.tree.item(item_id, values=vals)
        except Exception as e:
            log_event(f"Erro atualizando row: {e}")

    def open_selected_folder(self):
        folder = self.folder_var.get() 
        os.startfile(folder)

    def clear_history(self):
        try:
            if os.path.exists(HISTORY_FILE):
                os.remove(HISTORY_FILE)
            self.url_combo['values'] = []
            
            for item in self.tree.get_children():
                self.tree.delete(item)

            messagebox.showinfo("History", "History has been cleaned.")

        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível limpar histórico: {e}")

###################### youtube
    def start_ydlp(self):
        import re
        def clean_str(s):
            """Remove códigos ANSI e caracteres não imprimíveis."""
            if not s:
                return "0 KB/s"
            # remove ANSI
            s = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', s)
            return s.strip()

        import yt_dlp
        import time
        import os
        ffmpeg_path = r"C:\ffmpeg\ffmpeg-2025-10-27-git-68152978b5-essentials_build\bin\ffmpeg.exe"
        url = self.url_var.get().strip()
        folder = self.folder_var.get().strip() or DEFAULT_DOWNLOAD_DIR
        if not url:
            messagebox.showerror("Erro", "Insert URL from YouTube video.")
            return

        # adiciona linha na tabela
        item = self.tree.insert("", "end", values=("YouTube Video", "0%", "0 KB/s", "Starting..."))
        self.status_label.config(text="Starting download from YouTube...")

        start_time = time.time()
        
        def progress_hook(d):
            status = d.get('status')
            if status == 'downloading':
                total = d.get('total_bytes') or d.get('total_bytes_estimate')
                downloaded = d.get('downloaded_bytes', 0)

                # se total for None, nao calcula porcentagem
                if total:
                    pct_text = f"{downloaded / total * 100:.1f}%"
                else:
                    pct_text = " "

                speed_raw = d.get('_speed_str', "0 KB/s")
                speed = clean_str(speed_raw)

                eta = d.get('eta', 0)  # pode ser None
                if eta is None:
                    eta_text = "calculating..."
                elif eta < 60:
                    eta_text = f"{int(eta)} s"
                elif eta < 3600:
                    eta_text = f"{int(eta//60)} min {int(eta%60)} s"
                else:
                    eta_text = f"{int(eta//3600)} h {int((eta%3600)//60)} min"

                self.update_task_row(item, progresso=pct_text, velocidade=speed, status=f"Downloading | ETA: {eta_text}")
            elif status == 'finished':
                self.update_task_row(item, status="Processing...")

        def work():
            try:
                import yt_dlp
                # caminho completo do ffmpeg
                ffmpeg_path = r"C:\ffmpeg\ffmpeg-2025-10-27-git-68152978b5-essentials_build\bin\ffmpeg.exe"

                ydl_opts = {
                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                    'outtmpl': os.path.join(folder, '%(title)s.%(ext)s'), # salvar no dir selecionado
                    'ffmpeg_location': ffmpeg_path,
                    'postprocessors': [{
                        'key': 'FFmpegVideoConvertor',
                        'preferedformat': 'mp4',  # converte para mp4
                    }],
                    'noplaylist': True,
                                    
                    'retries': 10,             
                    'fragment_retries': 10,    
                    'file_access_retries': 5,
                    'continuedl': True,
                    'http_headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                        'Sec-CH-UA': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
                        'Sec-CH-UA-Platform': '"Windows"',
                        'Referer': 'https://www.youtube.com/',
                        'cookiefile': cookie_path,   #'www.youtube.com_cookies.txt',
                    },
                    # --- FIXES FOR 403 FORBIDDEN ---
                    'quiet': True,
                    'no_warnings': True,                    # -------------------------------
                    'progress_hooks': [progress_hook],
                }
                #url = "https://www.youtube.com/watch?v=EK8EctJQ5B4"
                url = self.url_var.get().strip()
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)

                self.title_ = title = info.get("title", "Vídeo")

                #self.titles.append(self.title_, {int(item_id[1:])})
                self.titles.append([self.title_, int(item[1:])])
                print(f"title append to titles: [({self.title_}, {int(item[1:])})]")
                print(f"yt-item: {int(item[1:])}")
                self.status_label.config(text=f"{title} downloading...")

                # comececar a baixar
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    
                    info = ydl.extract_info(url, download=False)
                    ydl.download([url])  # baixando

                # title = info.get("title", "Vídeo")
                self.update_task_row(item, progresso="100%", velocidade="0 KB/s", status="Finished")
                self.status_label.config(text=f"{title} finished!")

                filename = self.filename_var.get().strip() or ""
                if filename == "": filename = title
                print(f"filename -> {filename}")

                final_path = os.path.join(folder, f"{title}.mp4")
                log_event(f"yt-dlp OK: {title} -> {final_path}")

                self.filename_var.set("") # reset

            except yt_dlp.utils.DownloadError as e:
                msg = str(e)
                self.update_task_row(item, status="Error in YouTube")
                log_event(f"yt-dlp ERROR: {msg} | {url}")
                self.root.after(0, lambda: messagebox.showerror("Erro YouTube", msg))
                self.status_label.config(text="Error in YouTube download.")
            except Exception as e:
                self.update_task_row(item, status="Unexpected error")
                log_event(f"yt-dlp EXCEPTION: {e} | {url}")
                self.root.after(0, lambda: messagebox.showerror("Erro YouTube", str(e)))
                self.status_label.config(text="YouTube unexpected error.")

        threading.Thread(target=work, daemon=True).start()

    def choose_download(self):
        """Decide se é download normal ou YouTube"""
        url = self.url_var.get().strip().lower()
        if "youtube.com" in url or "youtu.be" in url:
            self.start_ydlp()
        else:
            self.add_download()

if __name__ == "__main__":
    root = tk.Tk()
    app = WDDApp(root)
    root.mainloop()
