# evaluator

Response from this server will be use for hand comparation. When we compare two hands we first look at hand types. According to [poker rules](http://www.ontexasholdem.com/pokerhandrankings.html), the hand with stronger type wins pot. But when we have two hands with same type we need some value who show which hand is better.

The method "recognize" accept JSON array of 7 cards (example ```["JD", "AK", "3K", "3D", "AD", "3P", "3D"]```). Then, creates array of all combinations with 5 cards (all hands). For each hand determinates hand's type (royal flush, straight flush, poker, full, flush, straight, three of a kind, two pairs, one pair, high card) and calculates hand's value.  Response contains JSON array of dictionaries with keys: "hand", "type", "value".

First we defined cards strengths. Card 2 has lowest strength (1), then it goes 3 with strength (2),..., and finally A is strongest card (13).
To determine hand's type and value we created "poker histogram". This is not standard histogram. Keys in histogram are poker cards, but values are 4-bits binary number. 4-bit number has as many units as card is repeated in hand. For example, hand ```A A A A J```, has following histogram ```{"A":1111, "J":0001}```.

#### Hand's type

Now, we could recognize some hand types. Summation of histogram's values for hands with the same type is always the same, no matter what cards this type contains. "Poker" always has sum value 16 (![alt text](https://latex.codecogs.com/gif.latex?2%5E%7B0%7D&plus;2%5E%7B1%7D&plus;2%5E%7B2%7D&plus;2%5E%7B3%7D)), "full house" always has sum value 10... Hands with all different cards (royal flush, straight flush, flush, straight, high card) has sum value 5. Last case needs additional tests.

#### Hand's value

We will explain calculating hand's value at example. If user have "full-house", for example ```[7 7 7 2 2]```. This hand is stronger than any other "full-house" which has triplet card lower than 7 (for example, ```[6 6 6 A A]``` is weaker hand). It means that triplet card must be more appreciated than pair card. If we tag tripplet card with 'a', and pair card with 'b' (In our case a=7 and b=2), we can calculate hand's value using expression ```a*13+b```. Since 'b' can have a maximum value 13, multiplication 'a' with 13 prevent that hand with a lower triplet has a higher value. In a similar way, wе calculates value for other types of hands.

Idea for poker histogram is inspired by [poker hand analyzer](https://www.codeproject.com/Articles/569271/A-Poker-hand-analyzer-in-JavaScript-using-bit-math).


## Prerequisites

You will need [Leiningen][] 2.0.0 or above installed.

[leiningen]: https://github.com/technomancy/leiningen

## Running

To start a web server for the application, run:

    lein ring server

## License

Copyright © 2017 
