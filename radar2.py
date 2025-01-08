# import adi
# import numpy as np
# import matplotlib.pyplot as plt

# # Configuration de l'ADALM-PLUTO
# center_frequency = 860e6  # Fréquence centrale (868 MHz)
# sample_rate =3e7        # Taux d'échantillonnage (1 MSPS)
# ts = 1/sample_rate      # Temps pour un échantillion
# N = 1e7                 #Nombre de point
# bandwidth = 3e6         # Bande passante de réception (200 kHz)
# delta = 500
# # Initialisation du périphérique
# pluto = adi.Pluto("ip:192.168.2.1")  # Remplacez par l'adresse IP correcte de votre ADALM-PLUTO
# pluto.rx_lo = int(center_frequency)
# pluto.rx_rf_bandwidth = int(bandwidth)
# pluto.rx_sample_rate = int(sample_rate)
# pluto.rx_buffer_size = 2**14  # Taille du buffer

# # Préparation du graphique
# plt.ion()  # Mode interactif
# fig, ax = plt.subplots(figsize=(10, 6))
# line, = ax.plot([], [], label="Spectre reçu")
# ax.set_title("Spectre du signal reçu (ADALM-PLUTO)")
# ax.set_xlabel("Fréquence (Hz)")
# ax.set_ylabel("Amplitude (dB)")
# ax.grid()
# ax.legend()
# ax.set_xlim(center_frequency - bandwidth / 2, center_frequency + bandwidth / 2)
# # ax.set_xlim(center_frequency - delta, center_frequency + delta)
# ax.set_ylim(-100, 0)  # Plage par défaut pour l'amplitude (ajustable)

# # Boucle de mise à jour
# print("Acquisition en temps réel... Appuyez sur Ctrl+C pour arrêter.")
# try:
#     while True:
#         # Acquisition des données
#         samples = pluto.rx()
#         norm = np.sqrt(samples.real**2 + samples.imag**2)
#         # Calcul de la FFT
#         fft_data = np.fft.fftshift(np.fft.fft(norm))
#         fft_magnitude = 20 * np.log10(np.abs(fft_data) + 1e-6)  # Évite les log(0)

#         # Génération des axes de fréquences
#         freqs = np.fft.fftshift(np.fft.fftfreq(len(norm), d=1 / sample_rate))
#         freqs += center_frequency
#         t = np.arange(0, N * ts, ts)
#         # Mise à jour du graphique
#         line.set_data(freqs, fft_magnitude)
#         ax.set_ylim(0,150)
#         plt.pause(0.1)  # Pause pour l'animation

# except KeyboardInterrupt:
#     print("Arrêt de l'acquisition.")
#     plt.ioff()
#     plt.show()

import adi
import numpy as np
import matplotlib.pyplot as plt

def get_speed(max_frequency):
    return 3,6*3e8*(max_frequency/frequency -1) 



# Configuration
frequency = 800e6
sample_rate = 1e6
bandwidth = 10e3
pluto = adi.ad936x.Pluto("ip:192.168.2.1")
pluto.rx_lo = int(frequency)
pluto.rx_rf_bandwidth = int(bandwidth)
pluto.rx_sample_rate = int(sample_rate)
pluto.rx_buffer_size = 2**20

# Préparation du graphe
plt.ion()
fig, ax = plt.subplots(figsize=(10, 6))
line = ax.plot([], [])
ax.set_title("Spectre du signal reçu")
ax.set_xlabel("Fréquence (Hz)")
ax.set_ylabel("Amplitude (dB)")
ax.grid()

try:
    while True:
        samples = pluto.rx()
        fft_data = np.fft.fftshift(np.fft.fft(samples, len(samples)))
        fft_magnitude = 20 * np.log10(np.abs(fft_data) + 1e-6)
        freqs = np.fft.fftshift(np.fft.fftfreq(len(fft_data), d=1/sample_rate)) 
        print("fft_magnitude :" , fft_magnitude)
        print("freqs :" ,freqs, "len(freq)", len(freqs))
        # Recherche du max
        max = 0
        max_index = 0
        for i in range (len(fft_magnitude)):
            if (fft_magnitude[i] > max) :
                max = fft_magnitude[i]
                max_index = i


        print("Fréquence du pic :",freqs[max_index], "Hz")

        line.set_data(freqs, fft_magnitude)
        ax.set_xlim(frequency - bandwidth / 2, frequency + bandwidth / 2)
        ax.set_ylim(fft_magnitude.min() - 10, fft_magnitude.max() + 10)
        plt.pause(0.1)
except KeyboardInterrupt:
    print("Arrêt.")
    plt.ioff()
#     plt.show()






# import adi
# import numpy as np
# import matplotlib.pyplot as plt

# # Configuration de l'ADALM-PLUTO
# center_frequency = 860e6  # Fréquence centrale de transmission (860 MHz)
# sample_rate = 2e6         # Taux d'échantillonnage (2 MSPS)
# bandwidth = 200e3         # Bande passante de réception (200 kHz)

# # Initialisation du périphérique
# pluto = adi.Pluto("ip:192.168.2.1")  # Remplacez par l'adresse IP de votre ADALM-PLUTO
# pluto.rx_lo = int(center_frequency)  # Fréquence locale de réception
# pluto.rx_rf_bandwidth = int(bandwidth)  # Bande passante de réception
# pluto.rx_sample_rate = int(sample_rate)  # Taux d'échantillonnage de réception
# pluto.rx_buffer_size = 2**14  # Taille du buffer de réception

# # Transmission de la fréquence porteuse modifiée par un signal sinusoïdal (par exemple)
# tone_frequency = 50e3  # Fréquence du signal modulé
# pluto.tx_lo = int(center_frequency)  # Fréquence locale de transmission
# pluto.tx_rf_bandwidth = int(bandwidth)  # Bande passante de transmission
# pluto.tx_sample_rate = int(sample_rate)  # Taux d'échantillonnage de transmission

# # Préparation du graphique
# plt.ion()
# fig, ax = plt.subplots(figsize=(10, 6))
# line, = ax.plot([], [])
# ax.set_title("Spectre du signal reçu")
# ax.set_xlabel("Fréquence (Hz)")
# ax.set_ylabel("Amplitude (dB)")
# ax.grid()

# # Fonction pour détecter le décalage Doppler
# def get_doppler_shift(received_frequency, transmitted_frequency):
#     # Calcul du décalage Doppler (approximatif)
#     return (received_frequency - transmitted_frequency)

# # Boucle de transmission et réception continue
# try:
#     while True:
#         # Acquisition des données reçues
#         samples = pluto.rx()
        
#         # Calcul de la FFT des données reçues
#         fft_data = np.fft.fftshift(np.fft.fft(samples))
#         fft_magnitude = 20 * np.log10(np.abs(fft_data) + 1e-6)  # Prendre le log d'amplitude

#         # Génération des axes de fréquence
#         freqs = np.fft.fftshift(np.fft.fftfreq(len(samples), d=1 / sample_rate)) + center_frequency

#         # Détection du pic de puissance (signal reçu)
#         peak_index = np.argmax(fft_magnitude)
#         peak_frequency = freqs[peak_index]

#         # Calcul du décalage Doppler
#         doppler_shift = get_doppler_shift(peak_frequency, center_frequency)
        
#         # Affichage des résultats
#         print(f"Fréquence reçue : {peak_frequency / 1e6:.6f} MHz")
#         print(f"Décalage Doppler : {doppler_shift / 1e3:.2f} kHz")

#         # Mise à jour du graphique
#         line.set_data(freqs, fft_magnitude)
#         ax.set_ylim(fft_magnitude.min() - 10, fft_magnitude.max() + 10)
#         plt.pause(0.1)

# except KeyboardInterrupt:
#     print("Arrêt de l'acquisition.")
#     plt.ioff()
#     plt.show()
