#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 00:02:01 2024

@author: luiz
"""

import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
from sklearn.decomposition import NMF

from scipy import signal
from scipy.ndimage import gaussian_filter1d

from music21 import midi
from midigenlib import populate_midi_track_from_data  # own library in this folder

from os import path

# Step 1: Load the known bell sounds and the mixture sound
# Load bell sound samples (assuming you have three bell samples: bell1.wav, bell2.wav, bell3.wav)
bell1, sr = librosa.load('/home/luiz/Music/Baixadas/Sinos de São João del Rey/Carmo - sino pequeno.wav', sr=None)
bell2, sr = librosa.load('/home/luiz/Music/Baixadas/Sinos de São João del Rey/Carmo - sino médio.wav', sr=None)
bell3, sr = librosa.load('/home/luiz/Music/Baixadas/Sinos de São João del Rey/Carmo - sino grande.wav', sr=None)

# cut
bell1 = bell1[1100:10000]
bell2 = bell2[980:10000]
bell3 = bell3[1600:10000]

# fade out
bell1[-600:] = bell1[-600:] * np.linspace(1, 0, 600)
bell2[-600:] = bell2[-600:] * np.linspace(1, 0, 600)
bell3[-600:] = bell3[-600:] * np.linspace(1, 0, 600)

# Load the mixture audio file (where bells are superimposed)
fpath = '/home/luiz/Music/Baixadas/Sinos de São João del Rey/Terentena carmo.wav'
mixture, sr = librosa.load(fpath, sr=None)

# Step 2: Compute the STFT (Short-Time Fourier Transform) for all sounds
def compute_stft(audio):
    return librosa.stft(audio, n_fft=2048, hop_length=512)

# Compute STFT of each bell and the mixture
S_bell1 = compute_stft(bell1)
S_bell2 = compute_stft(bell2)
S_bell3 = compute_stft(bell3)
S_mixture = compute_stft(mixture)

# Convert the complex STFT results into magnitude spectrograms
magnitude_mixture = np.abs(S_mixture)

# Step 3: Apply NMF to the mixture spectrogram to separate components
nmf_model = NMF(n_components=3, init='random', random_state=0, max_iter=500)
W = nmf_model.fit_transform(magnitude_mixture)  # W: basis components
H = nmf_model.components_  # H: activations over time

# Step 4: Visualize the decomposition
plt.figure(figsize=(10, 6))
plt.subplot(3, 1, 1)
librosa.display.specshow(librosa.amplitude_to_db(magnitude_mixture, ref=np.max), sr=sr, hop_length=512, x_axis='time', y_axis='log')
plt.title('Original Mixture Spectrogram')

plt.subplot(3, 1, 2)
librosa.display.specshow(librosa.amplitude_to_db(W, ref=np.max), sr=sr, hop_length=512, x_axis='time', y_axis='log')
plt.title('NMF Components (W)')

plt.subplot(3, 1, 3)
librosa.display.specshow(librosa.amplitude_to_db(H, ref=np.max), sr=sr, hop_length=512, x_axis='time', y_axis='log')
plt.title('NMF Activations (H)')

plt.tight_layout()
plt.show()

# Step 5: Match the NMF components with the known bell spectrograms
# We can now compare the components (W) with each bell sound
def compare_components(bell_spectrogram, nmf_components):
    # Take the average or sum across the time axis of the bell spectrogram (reduce to frequency dimension)
    bell_magnitude = np.mean(np.abs(bell_spectrogram), axis=1)  # Averaging over time

    # Now compare this bell's frequency profile with the NMF components
    similarities = np.zeros(nmf_components.shape[1])  # One similarity value per NMF component
    for i in range(nmf_components.shape[1]):
        # Measure similarity (e.g., correlation) between bell and NMF component
        similarity = np.corrcoef(bell_magnitude.flatten(), nmf_components[:, i].flatten())[0, 1]
        similarities[i] = similarity
    return similarities

# Compare each bell with the NMF components
similarity_bell1 = compare_components(S_bell1, W)
similarity_bell2 = compare_components(S_bell2, W)
similarity_bell3 = compare_components(S_bell3, W)

# Step 6: Output the results
print(f"Similarity with Bell 1: {similarity_bell1}")
print(f"Similarity with Bell 2: {similarity_bell2}")
print(f"Similarity with Bell 3: {similarity_bell3}")

# Based on these similarities, we can map which NMF component corresponds to which bell

# transposing H
H = H.T

# filtering over time
b, a = signal.ellip(4, 0.01, 120, 0.125)  # Filter to be applied.

H_fgust = signal.filtfilt(b, a, H, method="gust", axis=0)

H_gauss = gaussian_filter1d(H, sigma=2, axis=0)  # sigma controls the smoothness


f, ax = plt.subplots()

# Normalize along a specific axis
def normalize_along_axis(arr, axis):
    min_vals = np.min(arr, axis=axis, keepdims=True)
    max_vals = np.max(arr, axis=axis, keepdims=True)
    normalized_arr = (arr - min_vals) / (max_vals - min_vals)
    return normalized_arr

sgn = H_fgust
normalized_H = normalize_along_axis(H, axis=0)
normalized_sgn = normalize_along_axis(sgn, axis=0)

lines = ax.plot(normalized_H, linestyle='--')
for i, line in enumerate(lines):
    ax.plot(normalized_sgn[:, i], color=line.get_color(), linestyle='-')  # 


peaks_all = []
for idx, i_bell in enumerate(normalized_sgn.T):
    peaks, properties = signal.find_peaks(i_bell, height=0.3, distance=16, prominence=0.08)
    peaks_all.append(peaks)
    
    color=lines[idx].get_color()
    ax.vlines(peaks, ymin=0, ymax=1, colors=color)


# Generating midi file
nT = H.shape[1]
mts = []
for iT in range(nT):
    mts.append(midi.MidiTrack(iT))

time_stretch = 200

data = []
bell_pitches = [50, 28, 80]
for idxPs, iPs in enumerate(peaks_all):
    pitch = bell_pitches[idxPs]
    data_t = []  # for the track
    iPs = np.append(iPs, iPs[-1] + 500)  # adding a last note length at the end
    for idxP, iP in enumerate(iPs[:-1]):
        duration = (iPs[idxP + 1] - iPs[idxP]) * time_stretch
        velocity = int(normalized_sgn[:, idxPs][iP] * 127)
        
        data_t.append((duration, pitch, velocity))
    
    data.append(data_t)

for iT in range(nT):
    populate_midi_track_from_data(mts[iT], data[iT], initial_delay=peaks_all[iT][0] * time_stretch)
    
mf = midi.MidiFile()
for mt in mts:
    mf.tracks.append(mt)

# env = environment.Environment()
# temp_filename = env.getTempFile('.mid')
filename = fpath[:-4] + '.mid'
print("Saving file to: %s" % filename)
mf.open(filename, 'wb')
mf.write()
mf.close()
