## Document de analiză a cerințelor clientului

### Scopul aplicației: 

*În contextul actualei crize de mediu și al încălzirii globale dorim eficientizarea consumului de energiei pentru a contribui la eliminarea poluării. Astfel, echipa noastra propune un program IoT al cărui scop este de a interacționa cu device-urile smart dintr-o locuință pentru a eficientiza energia consumată. În acest sens programul ar putea fi implementat pe o sursa smart de energie (sau pe distribuitori de energie precum un prelungitor) electrica unde ar urma sa comunice cu restul de device-uri smart cu scopul de a realiza statistici și a efectua acțiuni ce vor diminua consumul de energie.*

### Obiectivele aplicației:

*Un prim obiectiv în realizarea acestui program este acela de a crea endpointuri la care se pot conecta și trimite informații senzorii de pe device (cei de intensitatea curentului și puterea folosită) și de endpointuri prin care acesta sa poată comunica cu obiectele smart pe care le alimentează.*

*Un alt obiectiv important este acela de a crea statistici pe baza datelor obținute și de trimiterea lor sub formă de rapoarte către utilizator. De asemenea, se pot genera sugestii de reducere a consumului prin interpolarea statisticilor cu obiceiurile utilizatorului.*

*În continuarea funcționalității de statistica, avem în obiectiv crearea de alerte prin care device-ul îl poate înștiința pe utilizator de consumuri nedorite de energie, un exemplu fiind un device uitat pornit, și de a îi permite închiderea acestora prin întreruperea curentului în porturile corespunzătoare.*

*Un selling point al device-ului îl poate forma și abilitatea de a detecta anomalii de consum, permitand astfel device-ului sa instiinteze utilizatorul despre funcționarea inadecvată a echipamentelor sau despre posibilele pericole (un scurtcircuit, cabluri inadecvate, etc.)*

*Astfel, device-ul se bazează pe generarea de informații ce permit utilizatorului să fie mai eficient în consumul de energie electrică și în același timp să prevină diverse probleme ce pot apărea în funcționarea acestora.*

### Grupul țintă

*Aplicatia este destinata utilizatorilor ce doresc sa eficientizeze consumul de energie, in special utilizatorilor de device-uri smart intrucat acestea permit interactiunea de la distanta cu user-ul. Identificam mai multe tipologii de utilizatori, iar pentru fiecare aducem solutii avantajoase.*

*Un prim tip de utilizatori sunt cei care doresc sa isi micsoreze consumul de energie dar intr-un mod autonom, fara prea multa implicare. Astfel, functia de inchidere automata a curentului pentru diverse device-uri este potrivita pentru acesti useri.*

*Pentru cei care doresc informatii mai detaliate despre obiceiurile lor de consum functiile de statistici si alerte le sunt foarte potrivite, avand posibilitatea de a-si invata propriile obiceiuri si de a analiza posibilele metode de reducere a consumului.*

*În același timp, aceste tipuri de utilizatori beneficiază și de feature-ul răspunzător de pornirea și oprirea automată a diverșilor consumatori în funcție de momentul din zi în care se afla.*

*De asemenea, identificăm un alt segment important și anume firmele, ce ar fi interesate îndeosebi de feature-urile de pornire/oprire automată a anumitor device-uri in functie de perioada corespunzatoare din zi și de statisticile de consum pentru a-și reduce costurile.*

### Colectarea cerințelor

 - [x] Detectarea valorilor anormale a device-urilor 
 - [x] Monitorizarea consumului device-urilor conectate
 - [ ] Comunicarea dintre mai multe device-uri care se afla in aceeasi cladire 
 - [x] Alertarea utilizatorilor asupra utilizarii energiei in mod ineficient.
 - [x] Interactiune automata - inchidere si pornirea device-urilor in functie de setarile utilizatorului 
 - [x] Sfaturi de micsorare a consumului
 - [ ] Invatare automata a obiceiurilor utilizatorului pentru a interactiona cu device-urile si a reduce consumul
 - [ ] Conectarea cu alte device-uri smart pentru a prelua informatii de utilizare a acestora
 - [ ] Eficientizarea operatiilor pentru a reduce energia consumata de catre sursa

### Interpretarea si prioritizarea cerintelor
Cerinte functionale:
* Detectarea valorilor anormale a device-urilor
* Interactiune automata - inchidere si pornirea device-urilor in functie de setarile utilizatorului
* Monitorizarea consumului device-urilor conectate
* Alertarea utilizatorilor asupra utilizarii energiei in mod ineficient.
* Sfaturi de micsorare a consumului

Cerinte nefunctionale:
* Comunicarea dintre mai multe device-uri care se afla in aceeasi cladire 
* Conectarea cu alte device-uri smart pentru a prelua informatii de utilizare a acestora
* Eficientizarea operatiilor pentru a reduce energia consumata de catre sursa
* Invatare automata a obiceiurilor utilizatorului pentru a interactiona cu device-urile si a reduce consumul 

### Gruparea cerintelor
Devops - self-explanatory
- Initializare Hosting
- Initializare baza de date

Data Transfer - cerinte ce tin de transmiterea, validarea si stocarea de date
- Implementare Flask MQTT
- Implementare Flask HTTP
- Preluare date device-uri

Data Processing - cerinte ce tin de prelucrarea si monitorizarea de date:
- Detectarea valorilor anormale a device-urilor
- Monitorizarea consumului device-urilor conectate 
- Alertarea utilizatorilor asupra utilizarii energiei in mod ineficient

Automatic interaction - cerinte ce includ detectarea si interactiunea automata 
- Invatarea automata a obiceiurilor utilizatorului 
- Detectarea valorilor anormale a device-urilor 
- Alertarea utilizatoriilor asupra utilizarii energiei in mod ineficient


### Planning Poker results

| *P = Prioritate;  *D = Dificultate; 5 = max priority / dif                                                   | Johnny P/D | Alexandra P/D | Darius P/D | Ștefan P/D | Andrei P/D | Călin  P/D |
|------------------------------------------------------------------------------------------------------------|:----------:|:-------------:|:----------:|:----------:|:----------:|:----------:|
| Comunicarea dintre mai multe device-uri care se afla in aceeasi cladire                                    |     4/3    |      4/4      |     4/4    |     2/4    |     3/4    |     4/4    |
| Invatare automata a obiceiurilor utilizatorului pentru a interactiona cu device-urile si a reduce consumul |     5/2    |      5/3      |     4/5    |     3/5    |     4/5    |     3/5    |
| Conectarea cu alte device-uri smart pentru a prelua informatii de utilizare a acestora                     |     3/3    |      3/3      |     3/3    |     3/4    |     3/4    |     3/3    |
| Eficientizarea operatiilor pentru a reduce energia consumata de catre sursa                                |     3/4    |      3/4      |     3/4    |     4/3    |     3/3    |     4/3    |
| Detectarea valorilor anormale a device-urilor                                                              |     3/4    |      4/3      |     3/3    |     4/3    |     4/2    |     4/2    |
| Interactiune automata - inchidere si pornirea device-urilor in functie de setarile utilizatorului          |     4/2    |      4/2      |     4/2    |     3/3    |     4/1    |     5/1    |
| Monitorizarea consumului device-urilor conectate                                                           |     4/3    |      4/3      |     4/2    |     4/2    |     4/3    |     5/3    |
| Alertarea utilizatorilor asupra utilizarii energiei in mod ineficient.                                     |     3/2    |      3/2      |     3/3    |     3/3    |     3/1    |     3/1    |
| Sfaturi de micsorare a consumului                                                                          |     3/3    |      2/2      |     4/4    |     2/2    |     2/1    |     3/2    |

### Prioritatea cerințelor
![alt text](https://github.com/SoftwareEngineerUB/SmartEnergy/blob/main/tasks.png)

### Echipa
 - Darius Buhai
 - Savu Ioan Daniel
 - Alexandra Bulaceanu
 - Rusu Andrei Cristian
 - Mitoi Stefan-Daniel
 - Stanciu Andrei-Calin

### Link Aplicatie
[https://smart-energy-ub.herokuapp.com/](https://smart-energy-ub.herokuapp.com/)
