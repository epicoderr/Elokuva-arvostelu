# Elokuva-arvostelu
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan arvosteluita.
* Käyttäjä näkee sovellukseen lisätyt arvostelut
* Käyttäjä pystyy etsimään arvosteluja hakusanalla
* Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja ja käyttäjän lisäämät arvostelut.
* Käyttäjä pystyy valitsemaan arvostetulle elokuvalle genren. Mahdolliset genret ovat tietokannassa.
* Käyttäjä pystyy antamaan kommenteja arvostelujen alle

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
