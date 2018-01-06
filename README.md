# TexasHoldemPoker

This is the implementation one of the most popular poker game [Texas Hold 'em](https://en.wikipedia.org/wiki/Texas_hold_%27em).

Application allows users to play this version of poker via net. Game is written in four various programming languages Python, Clojure, Haskell and Pharo.

## Application parts

* GUI - desktop app (Python)
* Core game - server (Haskell)
* Hand recognition - server (Clojure)
* Determiner of best hand - server (Pharo)

### Hand recognition - server (Clojure)

Response from this server will be use for hand comparation. When we compare two hands we first look at hand types. According to [poker rules](http://www.ontexasholdem.com/pokerhandrankings.html), the hand with stronger type wins pot. But when we have two hands with same type we need some value who show which hand is better.

The method "recognize" accept JSON array of 7 cards (example ```["JD", "AK", "3K", "3D", "AD", "3P", "3D"]```). Than, creates array of all combinations with 5 cards (all hands). For each hand determinates hand type (royal flush, straight flush, poker, full, flush, straight, three of a kind, two pairs, one pair, high card) and calculates hand value.  Response contains JSON array of dictionaries with keys: "hand", "hand-type", "hand-value".

To solve this problem, we created "poker histogram". This is not standard histogram. Keys in histogram are poker cards, but values are 4-bits binary number. 4-bit number has as many units as card is repeated in hand. For example, hand ```A A A A J```, has following histogram ```{"A":1111, "J":0001}```.

Now, we could recognize some hand types. Sum of histogram values for hands with the same type is always the same, no matter what cards this type contains. "Poker" always has sum value 16, "full house" always has sum value 10... Hands with all different cards (royal flush, straight flush, flush, straight, high card). This is only problem. We must to derminate is the hand from family "straight" or is "high card" hand. To solve this problem we used formula for the sum of the first n natural numbers ![alt text](http://www.9math.com/files/tex/2ff9e2a566efe8449e40da11658614c67d6201bc.png). We could use that formula because our card strengths has values from 1 to 13. We need to decide which is the cards with min and max strength. If expression ![alt text](https://latex.codecogs.com/gif.latex?%5Cfrac%7Bmax%28max&plus;1%29%7D%7B2%7D-%5Cfrac%7Bmin%28min&plus;1%29%7D%7B2%7D&plus;min) is equal with hand value, hand is from straight family.

Implementation of this application part is stored in folder with name "evaluator". To launch server we use [Leiningen](https://leiningen.org/). First you must navigate terminal in folder "evaluator" and then execute command:
```
lein ring server
```
After that server is started on port 3000. We could test this functionality sending POST request with body ```["JD", "10D", "QD", "KD", "AD"]``` at localhost:3000/recognize and result will be ```{"value":55, "hand-type":"royal-flush"}```.

Idea for poker histogram is inspired by [poker hand analyzer](https://www.codeproject.com/Articles/569271/A-Poker-hand-analyzer-in-JavaScript-using-bit-math).
