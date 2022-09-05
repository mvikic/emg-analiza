Ukratko da Vam opišem rad programa.

1) Pokrenuti EMG_Amplifier.exe
2) Pritiskom na dugme SCAN skeniraju se svi dostupni portovi na računaru.
3) U padajućem meniju COM port vrši se odabir porta koji će koristiti simulator
4) Klikom na dugme Select file bira se fajl sa EMG podacima sa ekstenzijom .csv
5) Pokrenuti emg_analiza.py u jednom od Python okruženja (radio sam u Visual Studio Code na Python 3.6.7 veziji)
6) Klikom na dugme CONNECT pokreće se simulator
7) Pokrenuti program 
8) U konzoli se ispisuje poruka koja obavještava korisnika da se vrši analizaranje signala u pozadini
9) Na skrinsotovima analiziran je EMG DATA 3d.csv signal koji traje otprilike 15 sekundi
10) Kada se završi analiza otvara se prozor na kom se nalaze dva grafika, gornji predstavlja EMG signal, donji predstavlja izračunat zamor
11) Sa otvaranjem prozora za iscrtavanje grafika u konzoli se ispisuje upit u vezi sa čuvanjem grafika u .png fajl, odnosno u vidu slike
12) Prije pokretanja samog programa u mom slučaju bilo je potrebno ukucati sledeću komandu u konzolu radi promjene trenutne radne putanje:
		cd C:\Users\MVIKIC\Desktop\emg_projekat_final\DATA 
13) save_path = os.getcwd() ugradjenom funkcijom getcwd() iz biblioteke os nalazi trenutnu radnu putanju i dodjeljuje je u vidu stringa promjenljivoj save_path koja se dalje koristi za čuvanje .png fajla

Pozdrav! 

Vikić Marko
BI 47/2017

