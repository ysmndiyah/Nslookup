import tkinter as tk
from tkinter import ttk
import psutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time
import os
import sys

# Variabel Global
running = False
upload_data = []
download_data = []

# --- Fungsi Monitor (Back-end) ---
def monitor_bandwidth():
    global upload_data, download_data
    # Ambil data awal
    old_sent = psutil.net_io_counters().bytes_sent
    old_recv = psutil.net_io_counters().bytes_recv
    
    while running:
        time.sleep(1) # Update setiap 1 detik
        
        # Ambil data baru
        new_sent = psutil.net_io_counters().bytes_sent
        new_recv = psutil.net_io_counters().bytes_recv
        
        # Hitung kecepatan (Bytes ke KB)
        upload_speed = (new_sent - old_sent) / 1024
        download_speed = (new_recv - old_recv) / 1024
        
        # Simpan data untuk referensi putaran berikutnya
        old_sent = new_sent
        old_recv = new_recv
        
        # Masukkan ke list data grafik
        upload_data.append(upload_speed)
        download_data.append(download_speed)
        
        # Batasi data biar grafik tidak kepanjangan (simpan 50 detik terakhir)
        if len(upload_data) > 50:
            upload_data.pop(0)
            download_data.pop(0)
            
        # Update tampilan grafik
        update_graph()

# --- Fungsi Kontrol ---
def start_monitor():
    global running
    if not running:
        running = True
        # Jalankan di thread terpisah biar aplikasi gak macet
        thread = threading.Thread(target=monitor_bandwidth, daemon=True)
        thread.start()
        btn_start.config(state="disabled")
        btn_stop.config(state="normal")

def stop_monitor():
    global running
    running = False
    btn_start.config(state="normal")
    btn_stop.config(state="disabled")

# --- Fungsi Update Grafik ---
def update_graph():
    # Hapus grafik lama
    ax.clear()
    
    # Gambar garis baru
    ax.plot(upload_data, label="Upload (KB/s)", color="red")
    ax.plot(download_data, label="Download (KB/s)", color="blue")
    
    # Setting tampilan grafik
    ax.set_ylabel("Kecepatan (KB/s)")
    ax.set_xlabel("Waktu (detik)")
    ax.legend(loc="upper left")
    ax.set_title("Monitor Trafik Jaringan Real-Time")
    ax.grid(True)
    
    # Tampilkan ke canvas tkinter
    canvas.draw()

# --- Tampilan GUI (Front-end) ---
def on_closing():
    global running
    running = False
    root.destroy()
    os._exit(0) # Paksa berhenti total

root = tk.Tk()
root.title("Bandwidth Monitor - Zahra")
root.geometry("800x600")

# Judul
lbl_title = tk.Label(root, text="MONITOR JARINGAN", font=("Arial", 16, "bold"))
lbl_title.pack(pady=10)

# Area Grafik (Matplotlib)
fig, ax = plt.subplots(figsize=(8, 5))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(pady=10, fill=tk.BOTH, expand=True)

# Tombol Kontrol
frame_btn = ttk.Frame(root)
frame_btn.pack(pady=10)

btn_start = ttk.Button(frame_btn, text="MULAI MONITOR", command=start_monitor)
btn_start.grid(row=0, column=0, padx=10)

btn_stop = ttk.Button(frame_btn, text="BERHENTI", command=stop_monitor)
btn_stop.grid(row=0, column=1, padx=10)
btn_stop.config(state="disabled") # Matikan tombol stop di awal

# Event saat aplikasi ditutup
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()