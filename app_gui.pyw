import customtkinter as ctk
import socket

# Konfigurasi tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ---------------------------------------------------
# Fungsi Logika
# ---------------------------------------------------
def nslookup():
    domain = entry_domain.get().strip()

    if domain == "":
        result_label.configure(text="⚠ Masukkan domain terlebih dahulu.", text_color="orange")
        return
    
    try:
        ip_address = socket.gethostbyname(domain)
        result_label.configure(
            text=f"🔍 Hasil NSLOOKUP\n\nDomain : {domain}\nIP Address : {ip_address}",
            text_color="lightgreen"
        )
    except socket.gaierror:
        result_label.configure(
            text=f"❌ Domain tidak ditemukan:\n{domain}",
            text_color="red"
        )

def clear():
    entry_domain.delete(0, ctk.END)
    result_label.configure(text="")
    entry_domain.focus()

# ---------------------------------------------------
# GUI Modern
# ---------------------------------------------------
app = ctk.CTk()
app.title("NSLOOKUP GUI – 2A Teknik Informatika")
app.geometry("480x500")
app.resizable(False, False)

# Header
header = ctk.CTkLabel(
    app, 
    text="🔎 NSLOOKUP TOOL",
    font=("Segoe UI", 22, "bold"),
    text_color="white"
)
header.pack(pady=15)

# Identitas
identity_frame = ctk.CTkFrame(app)
identity_frame.pack(pady=10, padx=20, fill="x")

ctk.CTkLabel(identity_frame, text="Nama: Al Yasmin Assadiyah", font=("Segoe UI", 12)).pack(pady=2)
ctk.CTkLabel(identity_frame, text="NPM : 714240014", font=("Segoe UI", 12)).pack(pady=2)
ctk.CTkLabel(identity_frame, text="Kelas: 2A Teknik Informatika", font=("Segoe UI", 12)).pack(pady=2)

# Input Card
input_frame = ctk.CTkFrame(app)
input_frame.pack(pady=15, padx=20, fill="x")

ctk.CTkLabel(input_frame, text="Masukkan Domain:", font=("Segoe UI", 12)).pack(pady=5)

entry_domain = ctk.CTkEntry(input_frame, width=300, height=40, placeholder_text="contoh: google.com")
entry_domain.pack(pady=5)

# Tombol
btn_lookup = ctk.CTkButton(app, text="🔍 Jalankan NSLOOKUP", width=220, height=40, command=nslookup)
btn_lookup.pack(pady=10)

# Hasil
result_frame = ctk.CTkFrame(app)
result_frame.pack(pady=20, padx=20, fill="both", expand=True)

result_label = ctk.CTkLabel(result_frame, text="", font=("Consolas", 13), justify="left")
result_label.pack(pady=15, padx=15)

entry_domain.focus()
app.mainloop()
