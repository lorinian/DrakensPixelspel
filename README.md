# DrakensPixelspel
Ralfs Drakspel. Spela om du vågar.

## Starta spelet

Första gången (installerar pygame):

    python3 -m venv .venv
    .venv/bin/pip install -r requirements.txt

Sedan:

    .venv/bin/python drakspel.py

## Styrning

- Piltangenter (eller WASD): flytta
- Mellanslag: skjut
- Enter: starta / spela igen
- Esc: avsluta
- 2 (på startskärmen): hoppa direkt till bana 2

## Banor

1. **Draken** - besegra den stora draken.
2. **Djungeln** - gå långt genom djungeln, förbi ormar, getingar, grodor och
   småspindlar. Längst bort väntar slutbossen: en stor spindel.

## Ändra i spelet

Överst i `drakspel.py` finns inställningar (liv, fart, bossens hälsa) och
pixelbilderna för huvudpersonen och bossen. Bilderna är ritade med bokstäver,
där varje bokstav är en färg, så det går att rita om dem direkt i filen.
