# TexasHoldemPoker

[Texas Hold 'em](https://en.wikipedia.org/wiki/Texas_hold_%27em) — The most popular version of poker, now playable online. This application allows users to enjoy the game remotely and is developed using four programming languages: Python, Clojure, Haskell, and Pharo.

![alt text](http://res.cloudinary.com/webp/image/upload/v1524244628/image_ryues5.png)

## Application parts

* GUI - desktop app (Python)
* Core game - server (Pharo)
* Hand recognition - server (Clojure)
* Determiner of best hand - server (Haskell)

### Hand recognition - server (Clojure)

Implementation of this application part is stored in folder with name "evaluator". To launch server we use [Leiningen](https://leiningen.org/). First you must navigate to the folder "evaluator" in terminal and then execute command:
```
lein ring server
```

### Determiner of best hand - server (Haskell)

Implementation of this application part is stored in folder with name "determiner". To launch server we use [Stack](https://docs.haskellstack.org/en/stable/README/). First you must navigate to the folder "determiner" in terminal and then execute commands:
```
stack build
stack exec determiner
```

### Core game - server (Pharo)

Implementation of this application part is stored in folder with name "core". To start the server, take a few steps:

1) Run Pharo
2) Install Tealight from Catalog Browser (Tools -> Catalog Browser)
3) To get package from repository run in the Playground following code: 
```
repositorySpec := 'Mijura/TexasHoldemPoker:master/core'.
Metacello new
  baseline: 'PokerCore';
  repository: 'github://', repositorySpec;
  load.
```
4) Load code into image from Monticello Browser.

![alt text](https://s13.postimg.org/b1igsvl9z/load.png)

5) Run in Playground: 
```
PCore new core.
```

### GUI - desktop app (Python)

Implementation of this application part is stored in folder with name "client". To start GUI app, navigate to the folder "client" in terminal and execute command:
```
python app.py
```
