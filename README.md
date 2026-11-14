Uppgift 3

# Svar
Den stulen datorn är *makar*. Den ligger på *59.8586, 17.6391* vilket är i *Uppsala*.

De andra 18 datorerna står i tre grupper: stockholm, göteborg och malmö. Makar är den enda som lämnat flocken. Den hade tur att den inte hette Link, för då hade den väl hittat tillbaka hem själv (obligatoriskt Zelda skämt)

# Hur programmet fungerar
Programmet l'ser `tracking.json` och jämför alla datorer med varandra. två datorer räknas som på samma plats om både latituden och longituden skiljer sig med mindre än 0.01 grader (ca 1,1 km). Datorer som har en granne markeras, och den som aldrig markeras är den stulna. Om ingen eller flera datorer är ensamma kastar programmet ett `ValueError` i stället för att gissa.

# Köra programmet
Gå in i mappen uppgift-3 och skriv:

 "uv run python solution.py" skriver ut namnet på den stulna datorn
 "uv run pytest solution.py" kör testerana

# Tröskelvärdet
Min tröskel är 0.01 grader, ungefär 1,1 km. Datorer på samma plats skiljer sig med ca 0.001 grader, medan städerna ligger flera grader från varandra. Tröskeln måste ligga mellan dessa två avstånd.

- **0.0001 (ca 11 m):** typ ingen dator räknas som granne, så nästan alla blir ensamma. Programmet kastar `ValueError` eftersom det inte går att avgöra vilken som är stulen.
- **1 (ca 111 km):** Uppsala ligger inom en grad från Stockholm, så makar räknas som nära de andra. Då är ingen ensam och programmet kastar `ValueError`.

# Antaganden

- Filen har formatet som beskrivs i uppgiften.
- Exakt en dator är ensam.
- Skillnaden i grader används direkt, utan omräkning till km.
