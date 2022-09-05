import serial
import matplotlib.pyplot as plt
import numpy as np
import os


def prolasci_kroz_nulu(vrijednosti_lista):
    vrijednosti_lista = np.array(vrijednosti_lista)
    vrijednosti_lista = vrijednosti_lista[np.nonzero(vrijednosti_lista)]
    return ((vrijednosti_lista[:-1] * vrijednosti_lista[1:]) < 0).sum()

f = 0.002
referentno_V = 4.5
pojacanje = 24

def analiza_signala(naponi_lista):
    br_prolasci = []
    intervali_vrijeme = []
    podjeljena_lista = [naponi_lista[i:i+100] for i in range(0, len(naponi_lista), 100)]
    for dio in podjeljena_lista:
        br_prolasci.append(prolasci_kroz_nulu(dio))
        intervali_vrijeme.append(len(br_prolasci) * f * 100)
    return intervali_vrijeme, br_prolasci

def konverzija(signal):
    napon = signal[0] << 16 | signal[1] << 8 | signal[2]
    if napon >= 8388608:
        napon -= 16777216
    faktor_skaliranja_uV = 1000000 * ((referentno_V / (8388608 - 1)) / pojacanje)
    return napon * faktor_skaliranja_uV

def main():

    com_port = serial.Serial('COM3', baudrate=921600, rtscts=True, bytesize=8, timeout=1)
    com_port.write(b'(CHs:ON)')
    #com_port.write(b'(TEST)')
    com_port.write(b'(NORMAL)')
    com_port.write(b'(START)')

    naponi = []
    vrijeme  = []

    fig, (osa_gore, osa_dole) = plt.subplots(nrows=2, ncols=1, figsize=(15, 8), constrained_layout=True)
    emg_podaci = com_port.readline
    emg_signali = emg_podaci().split(b')(') 
    while len(emg_signali) > 1 or emg_signali[0]:
        for signal in emg_signali:
            if len(signal) >= 7: 
                naponi.append(konverzija(signal)) 
                vrijeme.append(len(naponi) * f) 
                print(f'Analizira se... Molim sacekajte!', end='\r')
        emg_signali = emg_podaci().split(b')(')
    plt.ion()
    plt.show()
    osa_gore.plot(vrijeme, naponi, linewidth=0.7, label='Vrijednosti napona')
    osa_gore.set_title('EMG PODACI')
    osa_gore.set_xlabel('Vrijeme [s]')
    osa_gore.set_ylabel('Napon [mV]')
    osa_gore.legend()
    plt.draw()
    interval, prolasci = analiza_signala(naponi)
    osa_dole.plot(interval, prolasci, linewidth=0.7, label='Broj prolazaka kroz nulu') 
    osa_dole.set_title('ZAMOR MISICA')
    osa_dole.set_xlabel('Vrijeme [s]')
    osa_dole.set_ylabel('Prolasci kroz nulu')
    plyfit = np.polyfit(interval, prolasci, 3.6)
    trend = np.poly1d(plyfit)
    osa_dole.plot(interval, trend(interval), "r--", linewidth=1.4, label='Analiza zamora') 
    osa_dole.legend()
    plt.draw() 
      
    cuvanje = input('Da li zelite da sacuvate grafik? Da/ne: ')
    while True:
        if cuvanje.lower() == 'da':
            save_path = os.getcwd()
            ime = input('Unesite ime fajla: ')
            ime_putanja = os.path.join(save_path, ime + '.png')
            plt.savefig(ime_putanja, bbox_inches='tight')
            break
        elif cuvanje.lower() == 'ne':
            break
        else:
            cuvanje = input('Pogresan unos! Pokusajte opet.')


if __name__ == "__main__":
    main()