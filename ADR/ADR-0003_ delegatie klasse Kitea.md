# Implementatie van een delegatieklasse in het Kitea component

* Status: Proposed <!-- optional -->
* Deciders: Dennis Hakvoort <!-- optional -->
* Date: 2020-12-07 <!-- optional -->

Technical Story: POC-210 <!-- optional -->

## Context and Problem Statement

In de initele architectuur van het Kitea onderdeel wisten veel componenten van de volgende stap in de flow. Dit zorgt ervoor dat klassen van componenten weten waar zij idealiter niets van weten en dat de functies meer deden dan de naam deed vermoeden.

## Decision Drivers <!-- optional -->

* 1: Op het moment is het zonder delegatieklasse geïmplementeerd
* 2: Het moet zorgen voor het verhogen van de single responsibility en de leesbaarheid van de code.

## Considered Options

* Het laten zoals het nu is, zonder enige delegatie
* Iedere package een eigen delegatieklasse geven die de taken van die package behandeld en de volgende in het proces aanroept
* een centrale delegatieklasse creëren die de andere funcites één voor één aanroept en de volgende in het proces daarna aanroept.

## Decision Outcome

Chosen option: "1", omdat dit uiteindelijk zorgt voor de hoogste volging van het single-responsibility principe en het voorkomt dat functies meer doen dan hun naam doet suggereren. Bijvoorbeeld de functie "preprocess documents" slaat het niet langer meer op in de database en roept de distance calculator niet meer aan.

### Positive Consequences <!-- optional -->

* Verhoging van de leesbaarheid van de code en het single-responsibility principe.
* De functies zijn beter herbruikbaar omdat ze nu niet allerlei neveneffecten hebben.

### Negative Consequences <!-- optional -->

* het kost tijd om te implementeren.


