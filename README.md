## Document de analiză a cerințelor clientului

### Scopul aplicației: 

*In contextul actualei crize de mediu si al incalzirii globale dorim eficientizarea consumului de energiei pentru a contribui la elminarea poluarii. Astfel, echipa noastra propune un program IOT al carui scop este de a interactiona cu device-urile smart dintr-o locuinta pentru a eficientiza energia consumata. In acest sens programul ar putea fi implementat pe o sursa smart de energie (sau pe distribuitori de energie precum un prelungitor) electrica unde ar urma sa comunice cu restul de device-uri smart cu scopul de a realiza statistici si a efectua actiuni ce vor diminua consumul de energie.*

### Obiectivele aplicației:

*Un prim obiectiv in realizarea acestui program este acela de a crea endpointuri la care se pot conecta si trimite informatii senzorii de pe device (cei de intensitatea curentului si puterea folosita) si de endpointuri prin care acesta sa poata comunica cu obiectele smart pe care le alimenteaza. 
Un alt obiectiv important este acela de a crea statistici pe baza datelor obtinute si de trimiterea lor ca raporte utilizatorului. De asemenea, se pot genera sugestii de reducere a consumului prin interpolarea statisticilor cu obiceiurile utilizatorului.*

*In continuarea functionalitatii de statistica, avem in obiectiv creearea de alerte prin care device-ul il poate instiinta pe utilizator de consumuri nedorite de energie, un exemplu fiind un device uitat pornit, si de a ii permite inchiderea acestora prin intreruperea curentului in porturile corespunzatoare.
Un selling point al device-ului il poate forma si abilitatea de a detecta anomalii de consum, permitand astfel device-ului sa instiinteze utilizatorul despre functionarea inadecvata a echipamentelor sau despre posibilele pericole (un scurt, cabluri inadecvate, etc.)
Astfel, device-ul se bazeaza pe generarea de informatii ce permit utilizatorului sa fie mai eficient in consumul de energie electrica si in acelasi timp sa previna diverse probleme ce pot aparea in functionarea acestora.*

### Grupul țintă

*Aplicatia este destinata utilizatorilor ce doresc sa eficientizeze consumul de energie, in special utilizatorilor de device-uri smart intrucat acestea permit interactiunea de la distanta cu user-ul. Identificam mai multe tipologii de utilizatori, iar pentru fiecare aducem solutii avantajoase.*

*Un prim tip de utilizatori sunt cei care doresc sa isi micsoreze consumul de energie dar intr-un mod autonom, fara prea multa implicare. Astfel, functia de inchidere automata a curentului pentru diverse device-uri este potrivita pentru acesti useri.*

*Pentru cei care doresc informatii mai detaliate despre obiceiurile lor de consum functiile de statistici si alerte le sunt foarte potrivite, avand posibilitatea de a-si invata propriile obiceiuri si de a analiza posibilele metode de reducere a consumului.*

### Colectarea cerințelor

 - [ ] Detectarea valorilor anormale a device-urilor
 - [ ] Interactiune automata - inchidere si pornirea device-urilor in functie de setarile utilizatorului
 - [ ] Preluare date device-uri
 - [ ] Monitorizarea consumului device-urilor conectate
 - [ ] Alertarea utilizatorilor asupra utilizarii energiei in mod ineficient.
 - [ ] Sfaturi de micsorare a consumului
 
### Prioritatea cerințelor
![alt text](https://github.com/SoftwareEngineerUB/SmartEnergy/blob/main/tasks.png)

### Echipa
 - Darius Buhai
 - Savu Ioan Daniel
 - Alexandra Bulaceanu
 - Rusu Andrei Cristian
 - Mitoi Stefan-Daniel
