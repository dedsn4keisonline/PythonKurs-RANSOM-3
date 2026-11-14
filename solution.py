import json

import pytest

# Två datorer räknas som på samma plats om både latitud och longitud skiljer
# sig med mindre än 0.01 grader (ca 1,1 km). Datorer på samma plats skiljer
# sig bara med ca 0.001 grader, men städerna ligger flera grader ifrån
# varandra. 0.01 ligger mittemellan, så en stulen dator som flyttats till en
# annan stad räknas inte som nära de andra.
NEAR_THRESHOLD = 0.01


def are_close(pos1, pos2):

    """svarar på om två positioner är på samma plats.

    Funktionen tar två positioner som [latitud, longitud] och returnerar
    True om både latituden och longituden skiljer sig med mindre än
    NEAR_THRESHOLD, annars False. Jag använder abs() så att det inte
    spelar någon roll vilken position som står först.
    """
    
    lat1, lon1 = pos1
    lat2, lon2 = pos2

    lat_nara = abs(lat1 - lat2) < NEAR_THRESHOLD
    lon_nara = abs(lon1 - lon2) < NEAR_THRESHOLD
    return lat_nara and lon_nara


def solution(path):
    
    """Hittar den stulna datorn, alltså den som är ensam på sin plats.

    Funktionen läser JSON-filen på sökvägen path. Nyckeln är datorns namn
    och värdet är [latitud, longitud]. Alla datorer jämförs med varandra,
    och de som är nära någon annan dator markeras. Den som inte markeras
    är den stulna, och funktionen returnerar dess namn som en sträng.

    Jag antar att filen har formatet som beskrivs i uppgiften och att det
    bara finns en stulen dator. Om ingen dator är ensam, eller om flera är
    det, kastar funktionen ett ValueError eftersom det då inte går att veta
    vilken som är stulen.
    """
    # with stänger filen automatiskt när vi är klara

    with open(path) as fil:
        positions = json.load(fil)

# Ingen dator är markerad från början
    
    marked = {}
    for name in positions:

        marked[name] = False

    # Jämför alla datorer med alla andra
    for name1 in positions:
        for name2 in positions:
            if name1 != name2 and are_close(positions[name1], positions[name2]):

                marked[name1] = True

    # Samla de som aldrig markerades
    alone = []
    for name in marked:
        if marked[name] == False:
            alone.append(name)

    if len(alone) == 0:
        raise ValueError("Ingen dator är ensam, så den stulna går inte att hitta.")

    if len(alone) > 1:
        raise ValueError("Flera datorer är ensamma, så det går inte att veta vilken som är stulen.")

    return alone[0]


def test_solution(tmp_path):
    namn = solution("tracking.json")

    assert type(namn) == str, "solution() should return a string"
    with open("tracking.json") as fil:
        assert namn in json.load(fil), "The name should be one of the computers in the file"

    
# Ett litet exempel med en egen testfil (tmp_path är en tillfällig mapp från pytest).

    fil = tmp_path / "exempel.json"
    fil.write_text(
        json.dumps(
            {
                "a": [59.3291, 18.0681],
                "b": [59.3293, 18.0687],
                "c": [57.7089, 11.9746],
            }

        )
    )
    assert solution(str(fil)) == "c"


def test_ingen_ensam(tmp_path):
    #Här står alla datorer på samma plats, så det finns ingen stulen dator att hitta.
    # Funktionen ska inte gissa. Det här testet godtar vilket undantag som helst:
    # i dina egna tester ska du vara mer exakt.
    fil = tmp_path / "ingen.json"
    fil.write_text(json.dumps({"a": [59.3291, 18.0681], "b": [59.3293, 18.0687]}))
    with pytest.raises(Exception):
        solution(str(fil))


#Egna tester
def  test_are_close_nara(): # Skiljer 0.001 grader, mindre än tröskeln
    assert are_close([59.0, 18.0], [59.001, 18.001])


def test_are_close_langt_bort():

    # Skiljer 0.1 grader, mer än tröskeln
    assert not are_close([59.0, 18.0], [59.1, 18.0])


def test_are_close_bara_latitud_nara():    # Samma latitud men helt olika longitud, alltså inte samma plats
    assert not are_close([59.0, 18.0], [59.0, 12.0])


def test_are_close_ordning():      #Ordningen ska inte spela någon roll
    a = [59.0, 18.0]
    b = [59.001, 18.001]
    assert are_close(a, b) == are_close(b, a)


def test_ingen_ensam_valueerror(tmp_path):
    fil = tmp_path / "ingen_ensam.json"

    fil.write_text(json.dumps({"a": [59.0, 18.0], "b": [59.001, 18.001]}))
    
    with pytest.raises(ValueError):
        solution(str(fil))


def test_flera_ensamma_valueerror(tmp_path):

    
    
     # c och d ligger i olika städer, så båda är ensamma
    fil = tmp_path / "flera_ensamma.json"
    fil.write_text(
        json.dumps(
            {
             "a": [59.0, 18.0],
                "b": [59.001, 18.001],
                "c": [57.7089, 11.9746],
                "d": [55.6045, 13.0033],
            }
        )

    )
    with pytest.raises(ValueError):

        solution(str(fil))



if __name__ == "__main__":
    print(solution("tracking.json"))
