from itertools import chain
import os.path
import serial
import matplotlib.pyplot as plt
import numpy as np

Reference_V = 4.5 # A/D konverter referentni napon
Amp_Gain = 24 # Pojacanje EMG pojacala
f = 0.002 # 1s / 500Hz


# Konvertuje prva tri bajta signala u vrednost napona formulom datom u uvodu projekta
def konverzija(signal):
    napon = signal[0] << 16 | signal[1] << 8 | signal[2]
    if napon >= 8388608:
        napon -= 16777216
    Scale_Factor_uV = 1000000 * ((Reference_V / (8388608 - 1)) / Amp_Gain)
    return napon * Scale_Factor_uV


# Funkcija koja broji prolaske kroz nulu u datoj listi radi nalazenja zamora misica
def prolasci_kroz_nulu(lista):
    lista = np.array(lista)
    lista = lista[np.nonzero(lista)]
    return ((lista[:-1] * lista[1:]) < 0).sum()


# Analiziranje zamora misica brojanjem prolazaka kroz nulu Vrijednosti napona
def analiziraj_signal(lista_napona):
    broj_prolazaka = []
    vremenski_intervali = []
    podjeljena_lista = [lista_napona[x:x+100] for x in range(0, len(lista_napona), 100)]
    for deo in podjeljena_lista:
        broj_prolazaka.append(prolasci_kroz_nulu(deo))
        vremenski_intervali.append(len(broj_prolazaka) * 0.2) # Duzina liste broja prolazaka kroz nulu * broj elemenata u podeljenoj listi * interval
    return vremenski_intervali, broj_prolazaka


# Main funkcija
def main():
    # Otvaramo port preko kog komuniciramo sa EMG Pojacavacem
    port = serial.Serial('COM6', baudrate=921600, rtscts=True, timeout=1)
    # Zapocinjemo komunikaciju putem komandi navedenih u informacijama projekta
    port.write(b'(CHs:ON)')
    port.write(b'(NORMAL)')
    port.write(b'(START)')

    naponi = [] # Inicijalizacija liste koja ce drzati sve Vrijednosti napona sa signala (X osa grafika)
    vrijeme  = [] # Inicijalizacija liste koja ce drzati vrijemena koja odgovaraju datim naponima (Y osa grafika)

    figura, (osa1, osa2) = plt.subplots(nrows=2, ncols=1, figsize=(13, 7), constrained_layout=True) # Inicijalizacija figure grafika, osa za prvi grafik i drugi grafik
    plt.ion() # Ukljucujemo interakciju sa grafikom
    plt.show() # Prikazujemo grafik

    emg_data = port.readline # Citanje signala s porta
    signali = emg_data().split(b')(') # Citamo i razdvajamo podatke u pojedinacne signale
    # Format signala koji su nam potrebni je [CH Bajt 1, CH Bajt 2, CH bajt 3, Brojac, Baterija, Checksum]
    while len(signali) > 1 or signali[0]:
        for signal in signali: # Vrtimo petlju preko svih signala kako bi pronasli napone
            if len(signal) >= 7: # Filtriramo signale tako da radimo samo sa onim ciji format je adekvatan
                naponi.append(konverzija(signal)) # Dodajemo sve napone u listu koriscenu za Y osu grafika
                vrijeme.append(len(naponi) * f) # Mnozimo broj signala sa frekvencijom kako bi dobili vrijeme signala iliti X osu grafika
                print(f'Analizirali smo {vrijeme[-1]:.2f} sekundi signala', end='\r', flush=True)
        signali = emg_data().split(b')(')

    osa1.plot(vrijeme, naponi, linewidth=0.5, label='Vrijednosti napona') # Postavljamo Vrijednosti prvog grafika iliti X i Y osu
    osa1.set_title('EMG DATA') # Postavljamo naslov prvog grafika
    osa1.set_xlabel('vrijeme [s]') # Postavljamo naziv  X ose
    osa1.set_ylabel('Napon [mV]') # Postavljamo naziv Y ose
    osa1.legend() # Ukljucujemo prikaz imena linija grafika
    plt.draw() # Iscrtavamo grafik

    zamor = input('Analizirati signal i detektovati zamor misica? DA/NE: ') # Da li zelite da se pokrene algoritam detekcije zamora misica

    # Loop koji uzima input proslog pitanja i postavlja ga ponovo sve dok odgovor nije validan (da/ne)
    while True:
        if zamor.lower() == 'da': # Ako je odgovor da nastavljamo sa analizom sacuvanih Vrijednosti napona i iscrtavamo donji grafik koji prikazuje zamor misica
            interval, prolasci = analiziraj_signal(naponi) # Pozivamo funkciju koja obavlja analizu prethodno sacuvanih Vrijednosti napona
            # Pravimo grafik isto kao i ranije
            osa2.plot(interval, prolasci, linewidth=0.5, label='Broj prolazaka kroz nulu') # Postavljamo Vrijednosti X i Y ose drugog grafika 
            osa2.set_title('ZAMOR MISICA') # Postavljamo naslov drugog grafika
            osa2.set_xlabel('vrijeme [s]') # Postavljamo naziv X ose
            osa2.set_ylabel('Prolasci kroz nulu') # Postavljamo naziv Y ose
            # Nalazimo liniju trenda putem matematickih funkcija numpy bilbioteke
            plyfit = np.polyfit(interval, prolasci, 3.6)
            linija_trenda = np.poly1d(plyfit)
            osa2.plot(interval, linija_trenda(interval), "m--", linewidth=1.2, label='Analiza zamora') # Postavljamo vrednost linije trenda koja prikazuje zamor iscrtane u magenta boji sa isprekidanim linijama
            osa2.legend() # Ukljucujemo prikaz imena linija grafika
            plt.draw() # Iscrtavamo drugi grafik
            break
        elif zamor.lower() == 'ne': # Ako je odgovor ne izlazimo iz petlje
            break
        else: # U slucaju da odgovor nije vaidan postaljvamo pitanje opet
            zamor = input('Pogresan unos! Pokusajte opet.')

    # Isti princip kao i gore ali ovaj put sa cuvanjem grafika u slikovni fajl (jpg/png)
    sacuvati = input('Zelite li da sacuvate grafik? DA/NE: ')
    while True:
        if sacuvati.lower() == 'da':
            ime = input('Ime fajla: ')
            plt.savefig('C:/Users/MVIKIC/Desktop/emg_projekat' + ime + '.png', bbox_inches='tight')
            break
        elif sacuvati.lower() == 'ne':
            break
        else:
            sacuvati = input('Pogresan unos! Pokusajte opet.')


if __name__ == "__main__":
    main()