# Elokuva-arvostelu
* Sovelluksessa käyttäjät pystyvät jakamaan tietoa katsomistaan elokuvista.
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään elokuvia ja muokkaamaan ja poistamaan niitä.
* Käyttäjä näkee sovellukseen lisätyt elokuvat.
* Käyttäjä pystyy etsimään elokuvia hakusanalla.
* Käyttäjäsivu näyttää, montako elokuvaa käyttäjä on lisännyt ja listan käyttäjän lisäämistä elokuvista.
* Käyttäjä pystyy valitsemaan elokuvalle yhden tai useamman luokittelun (esim. komedia, toiminta, draama).
* Käyttäjä pystyy antamaan elokuvalle kommentin ja arvosanan. Reseptistä näytetään kommentit ja arvosana.

# Nykyinen tilanne
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan tietokohteita.
* Käyttäjä näkee sovellukseen lisätyt tietokohteet
* Käyttäjä pystyy etsimään tietokohteita hakusanalla
* Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja ja käyttäjän lisäämät tietokohteet.
* Käyttäjä pystyy valitsemaan tietokohteelle yhden tai useamman luokittelun. Mahdolliset luokat ovat tietokannassa.

## Sovelluksen asennus

Asenna `flask`-kirjasto:

```
$ pip install flask
```

Luo tietokannan taulut ja lisää alkutiedot:

```
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
```

Voit käynnistää sovelluksen näin:

```
$ flask run
```
