# TexasHoldemPoker

This is the implementation one of the most popular poker game [Texas Hold 'em](https://en.wikipedia.org/wiki/Texas_hold_%27em).

Application allows users to play this version of poker via net. Game is written in four various programming languages Python, Clojure, Haskell and Pharo.

## Application parts

* GUI - desktop app (Python)
* Core game - server (Haskell)
* Hand recognition - server (Clojure)
* Determiner of best hand - server (Pharo)

### Hand recognition - server (Clojure)

Implementation of this application part is stored in folder with name "evaluator". To launch server we use [Leiningen](https://leiningen.org/). First you must navigate terminal in folder "evaluator" and then execute command:
```
lein ring server
```
After that server is started on port 3000.

### Determiner of best hand - server (Pharo)

Implementation of this application part is stored in folder with name "determiner". To start the server, take a few steps:

1) get repository
```
repositorySpec := 'Mijura/TexasHoldemPoker:master/determiner'.
Metacello new
  baseline: 'PokerDeterminer';
  repository: 'github://', repositorySpec;
  load.
```
2) load code from repository in Monticello Browser

![alt text](https://s10.postimg.org/63yfqyyhl/load.png)

3) Install Tealight from Catalog Browser (Tools -> Catalog Browser)

4) Run in Playground: 
```
Determiner new server.
```
