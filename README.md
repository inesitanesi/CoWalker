# CoWalker

Esta aplicación se encarga de realizar planes de viajes minimizando el impacto ambiental. 

## Glosario

- Grupo: conjunto de personas que quieren ir de viaje juntos.
- Miembro: persona perteneciente a un grupo.

## Características

- Todos los miembros de un grupo tienen que tener el mismo vuelo, es decir, tener un vuelo de un sitio A a un sitio B y el objetivo es que todos los miembros vayan al sitio A
- Si dos miembros están cercanos el algoritmo tratará de juntarlos y pasan a ser 1 a ojos del algoritmo.
- Se considera que 2 miembros están cercanos si están a menos de 50km a la redonda. Este kilometraje aumenta (sumando) al unirse 2 miembros. Por ejemplo, si Ana y Juan están a 10km a la redonda, van a un punto de encuentro, se une su límite 50+50=100km y si Felipe está a 60km de distancia se une a ellos también.
- Se establece un límite de 2km a la redonda para caminar, si se pasa de ese límite el algoritmo buscará una forma para que vaya en transporte público.
