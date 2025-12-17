import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import psutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time
import os
import csv

# =================================================
# Variabel Global
# =================================================
running = False
paused = False
upload_data = []
download_data = []

peak_upload = 0.0
peak_download = 0.0

# =================================================
# Fungsi Monitoring (Thread)
# =================================================
def monitor_bandwidth():
    global upload_data, download_data, peak_upload, peak_download

    old_sent = psutil.net_io_counters().bytes_sent
    old_recv = psutil.net_io_counters().bytes_recv

    while running:
        time.sleep(1)

        if paused:
            continue

        new_sent = psutil.net_io_counters().bytes_sent
        new_recv = psutil.net_io_counters().bytes_recv

        upload_speed = (new_sent - old_sent) / 1024
        download_speed = (new_recv - old_recv) / 1024

        old_sent = new_sent
        old_recv = new_recv

        upload_data.append(upload_speed)
        download_data.append(download_speed)

        # Peak speed
        peak_upload = max(peak_upload, upload_speed)
        peak_download = max(peak_download, download_speed)

        current_upload.set(round(upload_speed, 2))
        current_download.set(round(download_speed, 2))
        peak_up_var.set(round(peak_upload, 2))
        peak_down_var.set(round(peak_download, 2))

        if len(upload_data) > 50:
            upload_data.pop(0)
            download_data.pop(0)

        update_graph()

# =================================================
# Kontrol
# =================================================
def start_monitor():
    global running, paused
    if not running:
        running = True
        paused = False
        status_text.set("🟢 Monitoring Aktif")
        threading.Thread(target=monitor_bandwidth, daemon=True).start()
        btn_start.config(state="disabled")
        btn_stop.config(state="normal")
        btn_pause.config(state="normal")

def stop_monitor():
    global running
    running = False
    status_text.set("🔴 Monitoring Berhenti")
    btn_start.config(state="normal")
    btn_stop.config(state="disabled")
    btn_pause.config(state="disabled")

def pause_resume():
    global paused
    paused = not paused
    if paused:
        status_text.set("⏸ Monitoring Dijeda")
        btn_pause.config(text="▶ RESUME")
    else:
        status_text.set("🟢 Monitoring Aktif")
        btn_pause.config(text="⏸ PAUSE")

def reset_graph():
    global peak_upload, peak_download
    upload_data.clear()
    download_data.clear()
    peak_upload = 0.0
    peak_download = 0.0
    current_upload.set(0.0)
    current_download.set(0.0)
    peak_up_var.set(0.0)
    peak_down_var.set(0.0)
    update_graph()

def export_csv():
    if not upload_data:
        messagebox.showwarning("Info", "Belum ada data untuk diexport.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")]
    )
    if not file_path:
        return

    with open(file_path, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Detik", "Upload (KB/s)", "Download (KB/s)"])
        for i, (u, d) in enumerate(zip(upload_data, download_data), start=1):
            writer.writerow([i, round(u, 2), round(d, 2)])

    messagebox.showinfo("Sukses", "Data berhasil diexport ke CSV.")

# =================================================
# Update Grafik
# =================================================
def update_graph():
    global ax
    ax.clear()
    ax.set_facecolor("#1e1e1e")

    ax.plot(upload_data, label="Upload (KB/s)", linewidth=2, color="#ff6b6b")
    ax.plot(download_data, label="Download (KB/s)", linewidth=2, color="#4dabf7")

    ax.set_title("Monitor Trafik Jaringan Real-Time", color="white", fontsize=12, fontweight="bold")
    ax.set_xlabel("Waktu (detik)", color="white")
    ax.set_ylabel("Kecepatan (KB/s)", color="white")
    ax.tick_params(colors="white")
    ax.legend(facecolor="#2b2b2b", labelcolor="white")
    ax.grid(True, linestyle="--", alpha=0.3)

    ax.relim()
    ax.autoscale_view()
    canvas.draw()

# =================================================
# Close Event
# =================================================
def on_closing():
    global running
    running = False
    root.destroy()
    os._exit(0)

# =================================================
# GUI
# =================================================
root = tk.Tk()
root.title("Bandwidth Monitor - by. Al Yasmin")
root.geometry("1000x760")
root.configure(bg="#121212")

# Tkinter Variables
current_upload = tk.DoubleVar(root, 0.0)
current_download = tk.DoubleVar(root, 0.0)
peak_up_var = tk.DoubleVar(root, 0.0)
peak_down_var = tk.DoubleVar(root, 0.0)
status_text = tk.StringVar(root, "🔴 Monitoring Berhenti")

# Header
header = tk.Frame(root, bg="#1f1f1f", height=60)
header.pack(fill="x")
tk.Label(header, text="MONITOR JARINGAN", fg="white", bg="#1f1f1f",
         font=("Segoe UI", 18, "bold")).pack(pady=15)

# Info Panel
info = tk.Frame(root, bg="#121212")
info.pack(pady=10)

def info_box(col, title, var):
    tk.Label(info, text=title, fg="#aaaaaa", bg="#121212").grid(row=0, column=col, padx=25)
    tk.Label(info, textvariable=var, fg="white", bg="#121212",
             font=("Segoe UI", 12, "bold")).grid(row=1, column=col)

info_box(0, "Upload (KB/s)", current_upload)
info_box(1, "Download (KB/s)", current_download)
info_box(2, "Peak Upload", peak_up_var)
info_box(3, "Peak Download", peak_down_var)

tk.Label(info, textvariable=status_text, fg="#4caf50",
         bg="#121212", font=("Segoe UI", 10, "bold")).grid(row=0, column=4, rowspan=2, padx=25)

# Grafik
card = tk.Frame(root, bg="#1e1e1e", bd=1, relief="solid")
card.pack(padx=20, pady=15, fill="both", expand=True)

fig, ax = plt.subplots(figsize=(8, 4))
fig.patch.set_facecolor("#1e1e1e")
canvas = FigureCanvasTkAgg(fig, master=card)
canvas.get_tk_widget().pack(padx=15, pady=15, fill="both", expand=True)

# Tombol
controls = tk.Frame(root, bg="#121212")
controls.pack(pady=15)

style = ttk.Style()
style.configure("Dark.TButton", font=("Segoe UI", 11), padding=10)

btn_start = ttk.Button(controls, text="▶ MULAI", command=start_monitor, style="Dark.TButton")
btn_stop = ttk.Button(controls, text="⏹ BERHENTI", command=stop_monitor, style="Dark.TButton")
btn_pause = ttk.Button(controls, text="⏸ PAUSE", command=pause_resume, style="Dark.TButton")
btn_reset = ttk.Button(controls, text="🔄 RESET", command=reset_graph, style="Dark.TButton")
btn_export = ttk.Button(controls, text="💾 EXPORT CSV", command=export_csv, style="Dark.TButton")

btn_start.grid(row=0, column=0, padx=8)
btn_stop.grid(row=0, column=1, padx=8)
btn_pause.grid(row=0, column=2, padx=8)
btn_reset.grid(row=0, column=3, padx=8)
btn_export.grid(row=0, column=4, padx=8)

btn_stop.config(state="disabled")
btn_pause.config(state="disabled")

# Footer
tk.Label(root, text="© Bandwidth Monitor | Al Yasmin",
         fg="gray", bg="#121212", font=("Segoe UI", 9)).pack(pady=5)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
