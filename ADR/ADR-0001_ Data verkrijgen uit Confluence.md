# Data wordt uit confluence gehaald door een API te bouwen als Confluence plugin.

* Status: Accepted
* Deciders: Dennis Hakvoort
* Date: 2020-11-17

## Context and Problem Statement

Voor het POC is data uit conflunece nodig. Er moet een manier worden gekozen om deze data uit Confluence te halen. De volgende data is nodig:
* Alle documenten binnen Confuence.
* De edit geschiedenis van de ingelogde gebruiker.
* De meest recent geupdate documenten.

## Decision Drivers <!-- optional -->

* force 1: het moet aansluiten op de Avisi Confluence Omgeving
* Force 2: het moet alle benodigde data kunnen verkrijgen.

## Considered Options

* 1: Confluence Cloud gebruiken en de REST api daarvan raadplegen
* 2: Confluence datacenter/server gebruiken en de REST api daarvan raadplegen
* 3: Confluence datacenter/server gebruiken en de java interfaces raadplegen om een eigen API aan te kunnen bieden.

## Decision Outcome

Gekozen optie: optie 3 omdat het de enige optie is die aansluit op de datacenter omgeving van Avisi en waar de benodigde data te verkrijgen is.

### Negative Consequences <!-- optional -->

* Significant meer werk dan het aanspreken van de standaard API binnen Confluence

## Pros and Cons of the Options <!-- optional -->

### 1:

- \+ Een betere API dan Confluence server/datacenter, voorkomt extra werk met ophalen van data.
- \- Avisi maakt geen gebruik van Cloud en heeft geen plannen om over te stappen.

### 2:

- \+ Avisi maakt gebruik van server/datacenter.
- \+ Het gebruiken van de API voorkomt extra werk voor de programmeur.
- \- Het is niet mogelijk om direct de geschiedenis van een gebruiker op te vragen, hiervoor zou je alle documenten moeten checken of de gebruiker hier een aanpassing op heeft staan.
- \- Het is niet mogelijk om alle nieuw aangepaste documenten te verkijgen.

### 3

- \+ Avisi maakt gebruik van server/datacenter.
- \+ Het verkrijgen van alle data lijkt goed mogelijk via de interfaces die aangeboden worden.
- \- Het vereist extra werk om een eigen API te schrijven die de benodigde data aanbied.
- \- De eisen voor security zijn niet bekend als het gaat om het aanbieden van een extra API.

