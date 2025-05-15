import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy.signal import lfilter, periodogram, freqz, correlate
import soundfile as sf
from scipy.fft import fft
from scipy.signal import freqz, lfilter
import sounddevice as sd

def densidadEspectralPotenciaAR(coef_a: np.array, coef_b: float, frecuencias: np.array,
                               S_U: np.array, fs: int) -> np.array:
    """
    Calcula la PSD de la salida de un proceso AR (AutoRegresivo)
    
    Parámetros:
    - coef_a: array con coeficientes AR [a1, a2, ..., aP]
    - coef_b: ganancia (escalar)
    - frecuencias: array con frecuencias en Hz
    - S_U: array con PSD de entrada para cada frecuencia
    - fs: frecuencia de muestreo
    
    Retorna:
    - S_X: array con PSD de salida para cada frecuencia 
    """
    omega = 2 * np.pi * frecuencias / fs

    H_f = coef_b / np.abs(1 - np.sum([coef_a[i] * np.exp(-1j * omega * (i + 1)) 
                                      for i in range(len(coef_a))], axis=0))**2

    # PSD = |H(f)|^2 * S_U
    S_X = np.abs(H_f)**2 * S_U
    return S_X

def gen_pulsos(f0, N, fs):
    """
    Genera un tren de impulsos periodico en el tiempo.
    f0: frecuencia fundamental (pitch) del tren de impulsos [Hz].
    N: cantidad de puntos que posee el array de la secuencia generada.
    fs: frecuencia de muestreo [Hz].
    Retorna: tren de impulsos (con varianza normalizada) de frecuencia f0.
    """
    s = np.zeros(N)
    s[np.arange(N) % round(fs / f0) == 0] = np.sqrt(fs / f0)
    return s

def psd_pulsos(f0, N, fs):
    """
    Genera la densidad espectral de potencia de un tren de impulsos.
    f0: frecuencia fundamental [Hz] (pitch) del tren de impulsos en el tiempo.
    N: cantidad de puntos que posee el array de la PSD resultante (SU(w)).
    fs: frecuencia de muestreo [Hz].
    Retorna:
    - PSD del tren de impulsos
    - Vector de frecuencias del espectro [Hz]
    """
    u = gen_pulsos(f0, N, fs)
    f = np.arange(N) * fs /N    # Vector de frecuencias (Hz)
    Su = np.abs(fft(u))**2 / N  # Periodograma
    return Su, f

def suavizar_bordes(x, fade=20):
    """
    Suaviza los bordes de una señal.
    x: señal original (array).
    fade: (float) porcentaje de transición en los bordes (0-50% del largo de x)
    retorna: versión suavizada de x
    """
    N = len(x)
    fade = max(1, min(fade, 50))  # Limita fade entre 1 y 50
    M = 2 * int(fade / 100 * N)
    v = np.hamming(M)
    fade_in = v[:M // 2]
    fade_out = v[M // 2:]
    window = np.concatenate([fade_in, np.ones(N - M), fade_out])
    s = window * x
    return s

def reproducir(audio, fs):
    """
    Reproducir audio usando soundevice
    audio: array con el contenido de la señal
    fs: freucencia de muestreo [Hz]
    """
    sd.play(audio, fs)
    sd.wait()

