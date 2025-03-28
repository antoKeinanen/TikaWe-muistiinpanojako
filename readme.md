# Muistiinpanojako

Sovelluksessa käyttäjät pystyvät luomaan sekä lukemaan muistiinpanoja sekä kommentoida niitä.

## Esittely
### Kirjautumis sivu
![login page](https://github.com/antoKeinanen/TikaWe-muistiinpanojako/blob/main/media/login.png?raw=true)

### Uusi muistiinpano
![new note](https://github.com/antoKeinanen/TikaWe-muistiinpanojako/blob/main/media/new.png?raw=true)

### Lue muistiinpano
![read note](https://github.com/antoKeinanen/TikaWe-muistiinpanojako/blob/main/media/read.png?raw=true)

## Asennus
```bash
# Lataa repositorio
git clone https://github.com/antoKeinanen/TikaWe-muistiinpanojako.git
cd tikawe-muistiinpanojako

# Asenna riippuvuudet
pip install flask
```

### Vaihtoehtoinen asennus
Sovellus on täysin toimiva vaikka käyttäisit yllä mainittuja asennus ohjeita. Oman kehittäjä kokemuksen parantamiseksi voidaan projektiin asentaa myös lisää riippuvuuksia poetryn avulla.

``` bash
# Lataa repositorio
git clone https://github.com/antoKeinanen/TikaWe-muistiinpanojako.git
cd tikawe-muistiinpanojako

# Asenna riippuvuudet
poetry install
```

## Sovelluksen käynnistys
```bash
# Alusta tietokanta
python scripts/setup.py

# Käynnistä sovellus
flask --app src/main run
```

### Vaihtoehtoinen sovelluksen käynnistys
Jos asensit sovelluksen poetryä käyttäen:
```bash
# Käynnistä sovellus
invoke start

# Jos tarkoituksena on kehittää tai muutella sovellusta
invoke start -d
```

## Sovelluksen testaus ja laadunvarmistus
Koska automatisoitu testaus ja -laadunvarmistus ei ole kurssin arvioinnin piirissä vaatii nämä toiminnot asennusta poetryllä.

### Testaus
VAROITUS: testaus poistaa kaikki tietokannassa olemassaolevat tiedot!
```bash
# Alusta tietokanta
invoke setup

# Käynnistä sovellus
invoke start

# Aja testit toisessa terminaali-ikkunassa
invoke test
```

### Lint
Lint komennon avulla voidaan tunnistaa automaattisesti yleisiä virheitä koodikannasta.
```bash
invoke lint
```

### Formatointi
Formatoi automaattisesti koko koodikannan yhtenäiseksi.
```
invoke format
```

## Ominaisuudet

- [x] Käyttäjä voi rekisteröityä
- [x] Käyttäjä voi kirjautua sisään
- [x] Käyttäjä voi luoda uuden muistiinpanon
- [x] Käyttäjä voi poistaa oman muistiinpanonsa
- [x] Käyttäjä voi muokata omaa muistiinpanoa
- [x] Käyttäjä voi hakea muistiinpanoja otsikon perusteella
- [x] Käyttäjä näkee kenen tahansa muistiinpanon
- [x] Sovelluksen teema valitaan käyttäjän järjestelmän teema valinnan mukaan
- [ ] Käyttäjä voi lisätä yhden tai useamman aiheen muistiinpanolle
- [ ] Käyttäjä voi hakea muistiinpanoja aiheen perusteella
- [ ] Käyttäjä näkee toisen käyttäjän käyttäjäsivun
- [ ] Käyttäjäsivulla näkyy kaikki toisen käyttäjän muistiinpanot
- [ ] Käyttäjäsivulla näkyy tilastoja toisesta käyttäjästä
- [ ] Käyttäjä voi lisätä muistiinpanoon kommentteja


## Lisenssi
Jaetaan MIT-lisenssin mukaisesti. Katso lisätietoja `LICENSE`-tiedostosta.