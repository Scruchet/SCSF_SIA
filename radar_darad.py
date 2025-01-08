import adi  # PyADI pour interfacer avec la SDR
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.signal import welch

# Fonction pour détecter le décalage Doppler
def get_doppler_shift(received_frequency, transmitted_frequency):
    # Calcul du décalage Doppler (approximatif)
    return (received_frequency - transmitted_frequency)
def get_speed(max_frequency,transmitted_frequency):
    return 3,6*3e8*(max_frequency/transmitted_frequency -1) 


# Connexion à la PlutoSDR
sdr = adi.Pluto("ip:192.168.2.1")  # Changez l'adresse selon votre configuration (ex: 'usb:' pour USB direct)
freq = int(910e6)
display_band = 100e6
# Configuration de la SDR en RX
sdr.rx_lo = int(freq)  # Fréquence centrale à 868 MHz
sdr.rx_rf_bandwidth = int(1e3)
sdr.sample_rate = int(1e6)  # Débit d'échantillonnage de 1 MSPS
sdr.rx_enabled_channels = [0]  # Utilisation d'un seul canal
sdr.rx_buffer_size = 2048*100  # Taille du buffer de réception
sdr.tx_cyclic_buffer = False  # Enable cyclic TX buffer
# Configuration de la SDR en TX
TRANSMIT = True
if (TRANSMIT):
    sdr.gain_control_mode_chan0="slow_attack"
    sdr.tx_hardwaregain_chan0   = -10
    sdr.tx_lo = freq  # TX LO frequency (same as RX for full duplex)
    sdr.tx_enabled_channels = [0]  # Enable TX channel 0
    sdr.tx_cyclic_buffer = True  # Enable cyclic TX buffer
    
#Emission
if (TRANSMIT) :
    # Génération du signal à freq

    fs = int(1e6)  # Sampling rate
    N = 1024  # Number of samples
    t = np.arange(N) / fs
    tx_data = 0.5 * np.exp(2j * np.pi * int(freq) * t)  # TX a 1 kHz tone
    sdr.tx(tx_data)

# Préparation de la figure Matplotlib pour la DSP
fig, ax = plt.subplots()
line_dsp, = ax.plot([], [], label="DSP", color="blue")

## Ajuster l'axe x pour être centré autour de 868 MHz
freq_center = sdr.rx_lo  # Fréquence centrale LO
freq_span = sdr.sample_rate  # Plage totale couverte (taux d'échantillonnage)
ax.set_xlim(freq_center - freq_span / 2, freq_center + freq_span / 2)  # Centré autour de 868 MHz
#ax.set_xlim(freq-display_band,freq+display_band)
ax.set_ylim(-100, 80)  # Amplitude en dB
ax.legend()
titre = "Densité spectrale de puissance (DSP) centrée sur " + str(freq) + "Hz"
ax.set_title(titre)
ax.set_xlabel("Fréquence (Hz)")
ax.set_ylabel("Amplitude (dBm)")

# Fonction pour calculer la DSP avec la méthode de Welch
def calculate_dsp(samples, sample_rate, lo_freq):
    # Calcul de la densité spectrale de puissance (DSP) avec la méthode de Welch
    f, Pxx = welch(samples, fs=sample_rate, nperseg=1024*1000000)

    # Décalage des fréquences pour que le centre soit autour de la fréquence LO
    f = f + lo_freq

    # Conversion de la densité spectrale en dBm
    # Pxx est en dB/Hz, donc on doit appliquer la conversion dBm sur la puissance
    Pxx_dBm = 10 * np.log10(Pxx * 1000)  # Conversion de la puissance en dBm (en considérant Pxx en Watts)

    return f, Pxx_dBm

# Fonction de mise à jour du graphique
def update(frame):
    samples = sdr.rx()  # Acquisition des données en continu
    if len(samples) == 0:  # Vérifier si des échantillons sont reçus
        print("Aucun échantillon reçu")
        return line_dsp,

    freqs, power = calculate_dsp(samples, sdr.sample_rate, freq_center)

    # Vérifier les fréquences calculées et la puissance
    max_index = 0
    max_amplitude = 0
    for i in range(len(power)):
        if power[i] > max_amplitude:
            max_amplitude = power[i]
            max_index = i
    print("Fréquence du pic", freqs[max_index], "Hz")
    print("Puissance calculée: ", max_amplitude)
    shift = get_doppler_shift(freqs[max_index], freq)
    if shift < 0 :
        print("Le sujet s'éloigne à", -shift,"km\h\n")
    else :
        print("Le sujet arrive à", shift,"km\h\n")
    line_dsp.set_data(freqs, power)
    return line_dsp,

# Animation en temps réel
ani = FuncAnimation(fig, update, interval=100)  # Intervalle en ms pour l'animation
plt.tight_layout()
plt.show()

# Libération des ressources SDR après arrêt
sdr.rx_destroy_buffer()