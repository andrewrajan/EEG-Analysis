import mne
import numpy as np
from scipy.signal import welch
import matplotlib.pyplot as plt


bands = {'Delta': (.5,4), 'Theta': (4,8), 'Alpha': (8,12), 'Beta': (13,30), 'Gamma': (30,50)}

def eeg_data(raw_fname):

    raw = mne.io.read_raw_edf(raw_fname, preload = True)
    raw_filt = raw.copy()
    raw_filt.filter(l_freq = 1, h_freq = 50)
    raw_filt.notch_filter(freqs=60)
    sfreq = raw.info['sfreq']
    return raw, raw_filt, sfreq


def print_plots(raw_filt):
    raw_filt.plot(n_channels = 100, duration = 10, title = "Filtered EEG data")
    plt.show() 

def print_psd(raw_filt):
    raw_filt.compute_psd(fmax = 100).plot()
    plt.show()


band_powers = {}

def welch_data(raw_filt, sfreq):
    data = raw_filt.get_data()
    signal = data[0].ravel()
    freqs, psd = welch(signal, fs = sfreq, nperseg=1024)
    for band, (low, high) in bands.items():
        idx = (freqs >= low) & (freqs <= high)
        band_powers[band] = np.trapz(psd[idx],freqs[idx])
    return band_powers


def band_graph(band_powers):
    plt.bar(band_powers.keys(), band_powers.values())
    plt.xlabel("Frequency Bands")
    plt.ylabel("Power")
    plt.title("EEG Band Power")
    plt.show()

def main():
    eeg1 = eeg_data("chb01_01.edf")
    eeg2 = eeg_data("chb01_04.edf")
    print_plots(eeg1[1])
    print_plots(eeg2[1])
    print_psd(eeg1[1])
    print_psd(eeg2[1])
    welch_eeg1 = welch_data(eeg1[1], eeg1[2])
    welch_eeg2 = welch_data(eeg2[1], eeg2[2])
    band_graph(welch_eeg1)
    band_graph(welch_eeg2)

if __name__ == "__main__":
    main()