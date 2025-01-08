# # Programme pour radar tactile en Python

# import time
# import adi
import math
# import matplotlib.pyplot as plt
# import numpy as np
# from scipy import signal

# # Configuration des constantes
# FREQUENCE = 858000000  # Fréquence centrale en Hz
# BANDWIDTH = 10000000   # Largeur de bande en Hz
# SAMPLE_RATE = 1000000  # Taux d'échantillonnage en Hz
# Na = 2048*2
# # Initialisation de la radio SDR
# sdr = adi.ad936x.Pluto(uri="ip:192.168.2.1")

# # Configuration des propriétés de la SDR
# sdr.rx_rf_bandwidth = BANDWIDTH
# sdr.sample_rate = SAMPLE_RATE
# sdr.rx_lo = FREQUENCE
# sdr.tx_lo = FREQUENCE
# sdr.tx_cyclic_buffer = True
# sdr.rx_hardwaregain_chan1 = -30
# sdr.gain_control_mode_chan1 = "slow_attack"

# # Configuration des canaux
# sdr.rx_enabled_channels = ["voltage0"]
# sdr.tx_enabled_channels = [0]

# # Affichage de la fréquence LO
# print(f"RX LO: {sdr.rx_lo} Hz")

# # Création d'une onde sinusoïdale pour la transmission
# fs = int(sdr.sample_rate)
# N = 1024  # Nombre de points
# fc = int(1000000 / (fs / N)) * (fs / N)  # Fréquence de l'onde sinusoïdale
# ts = 1 / float(fs)  # Période d'échantillonnage
# t = np.arange(0, N * ts, ts)
# i = np.cos(2 * np.pi * t * fc) * 2**14
# q = np.sin(2 * np.pi * t * fc) * 2**14
# iq = i + 1j * q

# # Envoi des données via le canal TX
# sdr.tx(iq)

# # Collecte et traitement des données RX
# plt.ion()  # Mode interactif pour la mise à jour continue du graphique

# for _ in range(10000):  # Nombre d'itérations de collecte
#     x = sdr.rx()  # Données reçues
#     norm = np.sqrt(x.real**2 + x.imag**2)  # Calcul de la norme
#     x_freq = np.fft.fft(norm)  # Transformation de Fourier

#     # Génération des fréquences associées
#     frequence = np.fft.fftfreq(len(norm), 1 / SAMPLE_RATE)

#     # Affichage du spectre en fréquence
#     plt.clf()
#     plt.plot(frequence, np.abs(x_freq))
#     plt.xlabel("Fréquence [Hz]")
#     plt.ylim(0,10000)
#     plt.xlim(0)
#     plt.ylabel("Amplitude [unité arbitraire]")
#     plt.title("Spectre en fréquence")
#     plt.pause(.1)  # Pause pour rafraîchir le graphique

# # Maintien du graphique à la fin
# plt.ioff()
# plt.show()


# # #Programme pour radar tactile python
# import time
# import adi
# import math
# import matplotlib.pyplot as plt
# import numpy as np
# from scipy import signal
# FREQUENCE = 88000000
# BANDWIDTH = 20000000
# SAMPLE_RATE = 1000000 

# # Create radio
# sdr = adi.ad936x.Pluto(uri="ip:192.168.2.1")

# # Configure properties
#sdr.rx_rf_bandwidth = BANDWIDTH
# sdr.sample_rate = SAMPLE_RATE
# sdr.rx_lo = FREQUENCE
# sdr.tx_lo = FREQUENCE
# sdr.tx_cyclic_buffer = True
# sdr.rx_hardwaregain_chan1 = -30
# sdr.gain_control_mode_chan1 = "slow_attack"

# # Configuration data channels
# sdr.rx_enabled_channels = ["voltage0"]
# sdr.tx_enabled_channels = [0]

# # Read properties
# print("RX LO %s" % (sdr.rx_lo))

# # Create a sinewave waveform
# fs = int(sdr.sample_rate)
# N = 1024
# fc = int(1000000 / (fs / N)) * (fs / N)
# ts = 1 / float(fs)
# t = np.arange(0, N * ts, ts)
# i = np.cos(2 * np.pi * t * fc) * 2 ** 14
# q = np.sin(2 * np.pi * t * fc) * 2 ** 14
# iq = i + 1j * q

# # Send data 
# sdr.tx(iq)

# # Collect data
# for i in range(100000):
#     # norme = []
#     # freq = []
#     x = sdr.rx()
#     x_freq = []
#     for elem in x:
#         x_freq.append(math.sqrt(elem.real**2 + elem.imag**2))
#     x_freq = np.fft.fft(x_freq)
#     print(len(x))
#     frequence = np.arange(0, 1023)*(SAMPLE_RATE/1024)
#     print(frequence)
#     #print(max(norme))
#     frequencies = np.fft.fftfreq(N, d=1/FREQUENCE)
#     f, Pxx_den = signal.periodogram(x, fs)
#     plt.clf()
#     plt.plot(frequencies, np.abs(x_freq)/1024)
#     # plt.ylim([1e-7, 1e2])
#     # plt.xlim([0, 1e9])
#     # plt.ylim(0,20)
#     plt.xlabel("frequency [Hz]")
#     plt.ylabel("PSD [V**2/Hz]")
#     plt.draw()
#     plt.pause(0.01)


# plt.show()

import numpy as np
import adi
import matplotlib.pyplot as plt

sample_rate = 1e7 # Hz
center_freq = 868000000 # Hz
num_samps = sample_rate # number of samples per call to rx()
BANDWIDTH = 2000
sdr = adi.Pluto("ip:192.168.2.1")
sdr.sample_rate = int(sample_rate)

# Config Tx
# sdr.tx_rf_bandwidth = int(sample_rate) # filter cutoff, just set it to the same as sample rate
# sdr.tx_lo = int(center_freq)
# sdr.tx_hardwaregain_chan0 = -50 # Increase to increase tx power, valid range is -90 to 0 dB

# Config Rx
sdr.rx_lo = int(center_freq)
sdr.rx_rf_bandwidth = int(sample_rate)
sdr.rx_buffer_size = num_samps
sdr.rx_rf_bandwidth = BANDWIDTH
sdr.rx_hardwaregain_chan1 = -30
sdr.gain_control_mode_chan1 = "slow_attack"

rx_samples = sdr.rx()
# print(rx_samples)
    # Calculate power spectral density (frequency domain version of signal)
psd = np.abs(np.fft.fftshift(np.fft.fft(rx_samples)))**2
psd_dB = 10*np.log10(psd)
f = np.linspace(sample_rate/-2, sample_rate/2, len(psd))
# plt.plot(f/1e6, psd_dB)
for i in range(1000) :
# Receive samples
    for i in range (0, 10):
        raw_data = sdr.rx()
    rx_samples = sdr.rx()
    psd = np.abs(np.fft.fftshift(np.fft.fft(rx_samples)))**2
    psd_dB = 10*np.log10(psd)
    f = np.linspace(sample_rate/-2, sample_rate/2, len(psd))
    norme = []
    max_norme = -100
    i_max_norme = 0
    for i in range(len(f)):
        value = math.sqrt(psd_dB[i].real**2 + psd_dB[i].imag**2)
        norme.append(value)
        if value > max_norme:
            max_norme = value
            i_max_norme = i
    print("Max is ",max_norme, " at value ",f[i_max_norme])
    plt.clf()
    plt.plot(f/1e6, psd_dB)
    plt.xlabel("Frequency [MHz]")
    plt.ylabel("PSD")
    plt.show()
    plt.draw()
    plt.pause(0.01)