# Er is gekozen om de PostgreSQL database te gebruiken voor gegevensopslag

* Status: Accepted
* Deciders: Dennis Hakvoort
* Date: 2020-11-20

## Context and Problem Statement

[Describe the context and problem statement, e.g., in free form using two to three sentences. You may want to articulate the problem in form of a question.]

## Decision Drivers <!-- optional -->

* Het moet in staat zijn om veel data op te slaan
* Het moet de volgende data goed op kunnen slaan:
    - Grote, ruwe tekst en hun preprocessed variant
    - De afstand tussen twee documenten

## Considered Options

*De keuze ging grotendeels tussen SQL en noSQL databases. Voor SQL is gekozen voor PostgreSQL en voor noSQL MongoDB. De keuze voor deze specifieke databases is gebaseerd op aanwezige kennis van de student.*

* 1: PostgreSQL
* 2: MongoDB

## Decision Outcome

Gekozen optie: PostgreSQL, omdat het opslaan van afstanden tot documenten een uniek relationeel probleem is waar MongoDB niet goed mee om zou kunnen gaan zonder het als een relationele database te behandelen, waarmee de voordelen van Mongo verdwijnen.

### Positive Consequences <!-- optional -->

* De student heeft veel ervaring met relationele databases en PostgreSQL.
* Het opslaan van de documentafstanden kan makkelijk gedaan worden door gebruik te maken van key relaties.

### Negative Consequences <!-- optional -->

* Mocht in de toekomst het datamodel veranderen en om meer flexibiliteit vragen is dat moeilijker te realiseren binnen een PostgreSQL database.

## Pros and Cons of the Options <!-- optional -->

### MongoDB

Minder bekend voor de student dan een relationele database. Er is overleg gepleegd met een collega over deze optie, hier zijn een aantal problemen geïdentificeert die er uiteindleijk voor hebben gezorgd dat we hebben kunnen vaststellen dat het geen goede optie is voor dit project.
* \+ er valt veel te leren voor de student, hoewel ervaring aanwezig is met MongoDb is dit niet zo veel als met een relationele database.
* \- Je zou de afstand tussen documenten idealiter als eigenschap van een document opslaan. Dit zou echter betekenen dat voor iedere toevoeging van een document een aanpassing nodig is bij alle andere documenten (om de afstand toe te voegen). Dit is onefficient.
* \- Een grote reden om voor een noSQL database te kiezen is wanneer je verschillende data opslaat per object. Tot zover nu bekend is is dit niet van toepassing binnen dit project.
