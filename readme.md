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

```bash
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
# Alusta tietokanta
invoke setup

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

-   [x] Käyttäjä voi rekisteröityä
-   [x] Käyttäjä voi kirjautua sisään
-   [x] Käyttäjä voi luoda uuden muistiinpanon
-   [x] Käyttäjä voi poistaa oman muistiinpanonsa
-   [x] Käyttäjä voi muokata omaa muistiinpanoa
-   [x] Käyttäjä voi hakea muistiinpanoja otsikon perusteella
-   [x] Käyttäjä voi hakea muistiinpanoja sisällön perusteella
-   [x] Käyttäjä näkee kenen tahansa muistiinpanon
-   [x] Sovelluksen teema valitaan käyttäjän järjestelmän teema valinnan mukaan
-   [x] Käyttäjä voi lisätä muistiinpanoon kommentteja
-   [x] Käyttäjä näkee toisen käyttäjän käyttäjäsivun
-   [x] Käyttäjäsivulla näkyy kaikki toisen käyttäjän muistiinpanot
-   [x] Käyttäjäsivulla näkyy tilastoja toisesta käyttäjästä
-   [x] Käyttäjä voi lisätä yhden tai useamman aiheen muistiinpanolle
-   [x] Käyttäjä voi hakea muistiinpanoja yhden aiheen perusteella
-   [x] Käyttäjä voi laajentaa ja supistaa hakua erikoismerkeillä.

## Haku erikoismerkkien avulla
Tavallisesti haku tapahtuu vain kokonaisten sanojen perusteella. Haut eivät ota huomioon isojen ja pienien merkkien eroa. Jos käyttäjä kuitenkin haluaa hakea vain sanan alku osalla voidaan käyttää `*` operaattoria. Esimerkiksi `Yks*` vastaisi sanoja `Yksi` ja `Yksitoista`. Merkillä `^` voidaan puolestaan rajata, että tekstin on alettava sanalla. Esimerkiksi `^kissa` vaatii, että joko sisältö tai otsikko alkaa sanalla kissa. 

## Tekoälyn käyttö raportti

Osa koodinkannan dokumentaatio kommenteista on kirjoitettu tekoälyn avulla. Dokumentaatio on kuitenkin aina ihmisen tarkistama ja korjaama.

### Käytetty alustuskehote

```
You are a skilled senior software developer your task is to write docstrings for given python functions. Use the following example as guide:

---

@csrf.validate("signin_page")
@flash_fields
def signin_action():
    """
    Handle the sign-in action, validating user credentials and responding
    accordingly.

    Retrieves form data, validates the credentials, and
    checks the password against the stored hash. If there are any errors
    during this process, appropriate error messages are flashed and the
    user is redirected back to the sign-in page. On successful validation,
    a token is generated and the user is redirected to the next page.

    Returns:
        Response: A Flask response object that either flashes errors and
        redirects to the sign-in page or responds with a token and
        redirects to the next page.
    """

    username, plain_password, next_page = _get_form_data()
    errors = _validate_credentials(username, plain_password)
    if errors:
        return flash_errors(errors, "signin_page", next=next_page)

    user, error = auth_service.get_user_by_username(username)
    if error:
        return flash_errors(error, "signin_page", next=next_page)

    if not check_password_hash(user.password_hash, plain_password):
        error = "Virheellinen käyttäjätunnus ja/tai salasana"
        return flash_errors(error, "signin_page", next=next_page)

    return _respond_with_token(user.token, next_page)

```

## Käyttö suurella tietomäärällä

Suuren suuren tietomäärän testejä varten tietokanta on alustettu `scripts/seed.py` skriptillä. Tauluissa on siis seuraavat määrät rivejä:

-   Users: 1 000 000
-   Notes: 5 000 000
-   Tags: 3 000 000
-   Comments: 15 000 000

Restit suoritetaan automaattisesti `scripts/performance_test.py` scriptillä. Skripti kutsuu sovelluksen rajapintaa kuin käyttäjä ja suorittaa seuraavat tapahtumat:

-   Luo käyttäjä
-   Lataa etusivu
-   Lataa muistiinpano 1
-   Lataa käyttäjä 1
-   Luo uusi muistiinpano
-   Muokkaa muistiinpanoa
-   Poista muistiinpano
-   Kirjaudu ulos
-   Kirjaudu sisään

Aikaprofilointiin käytin pyinstrument kirjastoa ja version sovelluksesta, jossa kyseinen kirjasto oli vielä käytössä voi löytää [täältä](https://github.com/antoKeinanen/TikaWe-muistiinpanojako/blob/44e083accffa29f1eea15c37b9b11e73aa75c716/src/main.py#L18-L39).

### Ennen optimointia

```
POST /api/signup took 8.185 seconds
GET / took 7.600 seconds
GET /note/1 took 1.247 seconds
GET /user/User1 took 1.875 seconds
POST /api/note/new took 1.300 seconds
POST /api/note/5000002/update took 1.438 seconds
POST /api/note/5000002/delete took 10.302 seconds
GET /search?query=a took 67.337 seconds
GET /signout took 0.010 seconds
POST /api/signin took 8.167 seconds
```

Tutkimalla palvelimelta kerättyjä aikaprofiileja voidaan havaita, että sovelluksen suurin pullonkaula on tietokanta ja erityisesti kyselyt, joissa joudutaan lukemaan suuri määrä tietoa. Tämä voidaan korjata lisäämällä tietokantaan indeksejä.

### Indeksien jälkeen

```
POST /api/signup took 0.437 seconds
GET / took 0.048 seconds
GET /note/1 took 0.013 seconds
GET /user/User1 took 2.748 seconds
POST /api/note/new took 0.022 seconds
POST /api/note/5000001/update took 0.032 seconds
POST /api/note/5000001/delete took 0.056 seconds
GET /search?query=a took 2.894 seconds
GET /signout took 0.009 seconds
POST /api/signin took 0.395 seconds
```

Indeksit selvästi paransivat sovelluksen nopeutta. Tavoitteenani kuitenkin olisi saada kaikki sivut lataamaan noin sekunnissa. Palvelimelta kerätyistä aikaprofiileista voidaan päätellä, että pullonkaulana ovat `get_user_statistics` ja `get_note_by_query` funktiot. Tilastojen laskennassa voidaan hyödyntää triggereitä tunnistamaan milloin käyttäjä luo tai poistaa muistiinpanoja ja kommentteja, jolloin tietokanta voi säilöä tilastot erillisessä taulussa.

### Triggerien jälkeen

```
POST /api/signup took 0.413 seconds
GET / took 0.047 seconds
GET /note/1 took 0.012 seconds
GET /user/User1 took 0.014 seconds
POST /api/note/new took 0.020 seconds
POST /api/note/5000007/update took 0.030 seconds
POST /api/note/5000007/delete took 0.058 seconds
GET /search?query=a took 1.919 seconds
GET /signout took 0.009 seconds
POST /api/signin took 0.387 seconds
```

Jäljelle jää vielä `note_by_query`, jossa pullonkaulana on tekstistä hakeminen. `LIKE '%haku%` on todella hidas suurilla tietomäärillä. Sqlite kuitenkin tarjoaa laajennuksen nimeltä `FTS5` eli full text search 5. FTS5 laajennuksen avulla voidaan hakea merkkijonoja tekstin keskeltä todella tehokkaasti

### Lopullinen toiminta suurella tietomäärällä

```
POST /api/signup took 1.182 seconds
GET / took 0.045 seconds
GET /note/1 took 0.014 seconds
GET /user/User1 took 0.016 seconds
POST /api/note/new took 0.026 seconds
POST /api/note/5000001/update took 0.032 seconds
POST /api/note/5000001/delete took 0.052 seconds
GET /search?query=a took 0.168 seconds
GET /signout took 0.010 seconds
POST /api/signin took 0.386 seconds
```

Sovellus toimii nyt riittävän tehokkaasti myös suurilla tietomäärillä. Ainoa ongelma, jolle en voi mitään on se, että jos hyppäämme viimeiselle sivulle esimerkiksi etusivulla, lataa sovellus todella kauan. Tämä kuitenkin johtuu siitä, että sqlite joutuu hakemaan kaikki muistiinpanot tietokannasta.

## Lisenssi

Jaetaan MIT-lisenssin mukaisesti. Katso lisätietoja `LICENSE`-tiedostosta.
