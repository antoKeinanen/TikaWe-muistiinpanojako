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
-   [x] Käyttäjä näkee kenen tahansa muistiinpanon
-   [x] Sovelluksen teema valitaan käyttäjän järjestelmän teema valinnan mukaan
-   [x] Käyttäjä voi lisätä muistiinpanoon kommentteja
-   [x] Käyttäjä näkee toisen käyttäjän käyttäjäsivun
-   [x] Käyttäjäsivulla näkyy kaikki toisen käyttäjän muistiinpanot
-   [x] Käyttäjäsivulla näkyy tilastoja toisesta käyttäjästä
-   [x] Käyttäjä voi lisätä yhden tai useamman aiheen muistiinpanolle
-   [x] Käyttäjä voi hakea muistiinpanoja yhden aiheen perusteella

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

### Ennen optimointia

-   Rekisteröityminen: 0.353s
    -   Salasanan hash-arvon generointi: 0.346s
    -   Tietokantaan kirjoitus: 0.007s
-   Etusivu: 9.069s
    -   Kirjautumisen tarkistus: 0.420s
    -   Sivulla näkyvien muistiinpanojen haku: 8.306s
    -   Kaikkien muistiinpanojen laskeminen: 0.334s
    -   Sivupohjan täyttäminen: 0.009s
-   Yksittäinen muistiinpano: 3.502s
    -   Kirjautumisen tarkistus: 0.063s
    -   Muistiinpanon sisällön haku: 0.003s
    -   Muistiinpanon kommenttien haku: 2.825
    -   Muistiinpanon tagien hakeminen: 0.911s
    -   Sivupohjan täyttäminen: 0.008s
-   Käyttäjäsivu: 4.137s
    -   Kirjautumisen tarkistus: 0.063s
    -   Sivulla näkyvien muistiinpanojen haku: 1.224s
    -   Käyttäjän tilastojen haku: 2.842s
    -   Sivupohjan täyttäminen: 0.008s
-   Uuden muistiinpanon luominen: 0.094s
    -   Kirjautumisen tarkistus: 0.064
    -   Muistiinpanon kirjoitus tietokantaan: 0.029s
-   Muistiinpanojen haku termillä "a": 17.260s
    -   Kirjautumisen tarkistus: 0.064s
    -   Sivulla näkyvien muistiinpanojen haku: 14.797s
    -   Haun täyttävien muistiinpanojen laskeminen: 2.392s
    -   Sivupohjan täyttäminen: 0.008s
-   Sisäänkirjautuminen: 0.339s
-   Muistiinpanon poistaminen: 5.753s
    -   Kirjautumisen tarkistus: 0.065s
    -   Muistiinpanon poisto tietokannasta: 5.688s

### Päätelmät

Tutkimalla palvelimelta kerättyjä aika profiileja voidaan havaita, että sovelluksen suurin pullonkaula on tietokanta ja erityisesti kyselyt, joissa joudutaan lukemaan suuri määrä tietoa. Tämä voidaan korjata lisäämällä tietokantaan indeksejä.

### Indeksien jälkeen

-   Rekisteröityminen: 0.426s
    -   Kirjautumisen tarkistus: 0.004s
    -   Salasanan hash-arvon generointi: 0.409s
    -   Tietokantaan kirjoitus: 0.017s
-   Etusivu: 0.378s
    -   Kirjautumisen tarkistus: 0.004s
    -   Sivulla näkyvien muistiinpanojen haku: 0.369s
    -   Sivupohjan täyttäminen: 0.008s
-   Yksittäinen muistiinpano: 0.017s
    -   Kirjautumisen tarkistus: 0.004s
    -   Muistiinpanon sisällön haku: 0.003s
    -   Muistiinpanon kommenttien haku: 0.004s
    -   Muistiinpanon tagien hakeminen: 0.002s
    -   Sivupohjan täyttäminen: 0.004s
-   Käyttäjäsivu: 11.8s
    -   Kirjautumisen tarkistus: 0.003s
    -   Sivulla näkyvien muistiinpanojen haku: 8.225s
    -   Käyttäjän tilastojen haku: 3.623s
    -   Sivupohjan täyttäminen: 0.018s
-   Uuden muistiinpanon luominen: 0.034s
-   Muistiinpanojen haku termillä "a": 3.316s
    -   Sivulla näkyvien muistiinpanojen haku: 0.005s
    -   Haun täyttävien muistiinpanojen laskeminen: 3.303
    -   Sivupohjan täyttäminen: 0.008
-   Sisäänkirjautuminen:
    -   Käyttäjän haku tietokannasta: 0.023s
    -   Salasanan hash-arvon validointi: 0.385s
-   Muistiinpanon poistaminen: 0.010s
    -   Kirjautumisen tarkistus: 0.004s
    -   Muistiinpanon poisto tietokannasta: 0.006s

### Päätelmät

Indeksit selvästi paransivat sovelluksen nopeutta. Toisaalta käyttäjäsivun lataaminen hidastui. Lisäksi haut, jotka laskevat jotakin vievät vielä liian pitkän ajan.

## Lisenssi

Jaetaan MIT-lisenssin mukaisesti. Katso lisätietoja `LICENSE`-tiedostosta.
