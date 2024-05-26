import cv2
import pygame
import sys
import numpy as np
import requests
import imageio
import pygame
from io import BytesIO

# Inisialisasi Pygame dan OpenCV
pygame.init()
cap = cv2.VideoCapture(0)  # Memulai tangkapan video (webcam)
pygame.display.set_caption("Permainan Cuci Tangan")

# Pengaturan jendela Pygame
LEBAR_JENDELA, TINGGI_JENDELA = 800, 600
screen = pygame.display.set_mode((LEBAR_JENDELA, TINGGI_JENDELA))

# Muat GIF (ganti dengan path file Anda)

# URL gambar GIF
url = "https://media.giphy.com/media/j5SL8PK4zSBDOAM2iy/giphy.gif"

# Mengunduh gambar GIF dari URL
response = requests.get(url)
gif_bytes = BytesIO(response.content)

# Memuat gambar GIF menggunakan imageio
gif_images = imageio.mimread(gif_bytes)

# Inisialisasi Pygame
pygame.init()

# Pengaturan jendela Pygame
LEBAR_JENDELA, TINGGI_JENDELA = 800, 600
screen = pygame.display.set_mode((LEBAR_JENDELA, TINGGI_JENDELA))

# Memainkan gambar GIF
for gif_image in gif_images:
    pygame_surface = pygame.image.frombuffer(gif_image.tobytes(), gif_image.shape[1::-1], "RGB")
    screen.blit(pygame_surface, (0, 0))
    pygame.display.flip()
    
# Konstan
WAKTU_TAMPIL = 3000  # Waktu tampil setiap GIF dalam milidetik

# Fungsi untuk menampilkan sebuah GIF
def tampilkan_gif(nomor):
    gif = pygame.transform.scale(gifs[nomor], (400, 300))  # Menyesuaikan ukuran GIF
    screen.blit(gif, (400, 0))  # Meletakkan GIF di layar

# Fungsi untuk mendeteksi gerakan
def deteksi_gerakan(frame_sebelum, frame_sekarang):
    # Mengonversi gambar ke skala abu-abu
    frame_sebelum_abu = cv2.cvtColor(frame_sebelum, cv2.COLOR_BGR2GRAY)
    frame_sekarang_abu = cv2.cvtColor(frame_sekarang, cv2.COLOR_BGR2GRAY)

    # Menghitung perbedaan antara frame berturut-turut
    diff = cv2.absdiff(frame_sebelum_abu, frame_sekarang_abu)

    # Menerapkan ambang batas untuk mengidentifikasi area dengan perbedaan signifikan
    _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

    # Temukan kontur di area yang berbeda
    kontur, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    return len(kontur) > 0  # Mengembalikan True jika ada gerakan

# Fungsi untuk menampilkan feed kamera
def tampilkan_kamera(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)
    frame = pygame.transform.flip(frame, True, False)
    frame = pygame.transform.scale(frame, (400, 300))  # Menyesuaikan untuk muat di layar
    screen.blit(frame, (0, 0))  # Meletakkan di layar

# Menangkap frame pertama
ret, frame_sebelum = cap.read()
if not ret:
    print("Gagal menangkap video dari webcam. Periksa apakah webcam terhubung dan berfungsi.")
    sys.exit()
    
# Fungsi utama permainan
def permainan():
    global frame_sebelum  # Menggunakan variabel global frame_sebelum

    running = True
    waktu_mulai = pygame.time.get_ticks()
    indeks_gif_sekarang = 0

    while running:
        ret, frame_sekarang = cap.read()
        if not ret:
            print("Gagal membaca frame dari webcam.")
            break

        if deteksi_gerakan(frame_sebelum, frame_sekarang):
            print("Gerakan Terdeteksi!")

        frame_sebelum = frame_sekarang.copy()  # Memperbarui frame sebelumnya

        waktu_sekarang = pygame.time.get_ticks()
        if waktu_sekarang - waktu_mulai > WAKTU_TAMPIL:
            waktu_mulai = waktu_sekarang
            indeks_gif_sekarang = (indeks_gif_sekarang + 1) % len(gifs)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))  # Membersihkan layar
        tampilkan_gif(indeks_gif_sekarang)  # Menampilkan GIF saat ini
        tampilkan_kamera(frame_sekarang)  # Menampilkan feed kamera

        pygame.display.update()

    pygame.quit()
    cap.release()

# Jalankan permainan
permainan()
