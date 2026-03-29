import mne
import numpy as np
from scipy.signal import welch
import matplotlib.pyplot as plt


bands = {
    'Delta': (0.5, 4),
    'Theta': (4, 8),
    'Alpha': (8, 12),
    'Beta': (13, 30),
    'Gamma': (30, 50)
}


def eeg_data(raw_fname):
    raw = mne.io.read_raw_edf(raw_fname, preload=True)
    raw_filt = raw.copy()
    raw_filt.filter(l_freq=1, h_freq=50)
    raw_filt.notch_filter(freqs=60)
    sfreq = raw.info['sfreq']
    return raw, raw_filt, sfreq


def print_plots(raw_filt):
    raw_filt.plot(n_channels=100, duration=10, title="Filtered EEG data")
    plt.show()


def print_psd(raw_filt):
    raw_filt.compute_psd(fmax=100).plot()
    plt.show()


def welch_data(raw_filt, sfreq):
    data = raw_filt.get_data()
    signal = data[0].ravel()
    freqs, psd = welch(signal, fs=sfreq, nperseg=1024)

    band_powers = {}
    for band, (low, high) in bands.items():
        idx = (freqs >= low) & (freqs <= high)
        band_powers[band] = np.trapezoid(psd[idx], freqs[idx])

    return band_powers


def extract_features(raw_filt, sfreq):
    data = raw_filt.get_data()
    signal = data[0].ravel()

    freqs, psd = welch(signal, fs=sfreq, nperseg=1024)

    band_powers = welch_data(raw_filt, sfreq)
    total_power = sum(band_powers.values())

    if total_power > 0:
        band_percentages = {
            band: (power / total_power) * 100
            for band, power in band_powers.items()
        }
    else:
        band_percentages = {band: 0 for band in band_powers}

    line_length = np.sum(np.abs(np.diff(signal)))

    cumulative_power = np.cumsum(psd)
    total_psd_power = cumulative_power[-1]

    if total_psd_power > 0:
        sef_idx = np.where(cumulative_power >= 0.95 * total_psd_power)[0][0]
        sef = freqs[sef_idx]
    else:
        sef = 0

    def safe_div(a, b):
        return a / b if b != 0 else 0

    alpha_beta = safe_div(band_powers["Alpha"], band_powers["Beta"])
    theta_alpha = safe_div(band_powers["Theta"], band_powers["Alpha"])

    features = {
        # Band %
        "Delta %": band_percentages["Delta"],
        "Theta %": band_percentages["Theta"],
        "Alpha %": band_percentages["Alpha"],
        "Beta %": band_percentages["Beta"],
        "Gamma %": band_percentages["Gamma"],

        # Power
        "Total Power": total_power,

        # Signal stats
        "RMS": np.sqrt(np.mean(signal ** 2)),
        "Variance": np.var(signal),
        "Std Dev": np.std(signal),
        "Peak-to-Peak": np.ptp(signal),

        # NEW Tier 1 features
        "Line Length": line_length,
        "SEF (95%)": sef,
        "Alpha/Beta": alpha_beta,
        "Theta/Alpha": theta_alpha,
    }

    return features


def band_graph(band_powers):
    plt.bar(band_powers.keys(), band_powers.values())
    plt.xlabel("Frequency Bands")
    plt.ylabel("Power")
    plt.title("EEG Band Power")
    plt.show()