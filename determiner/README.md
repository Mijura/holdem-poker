# Determniner

The method "bestHand" accept JSON array of user's cards. 

For each user:
1. calls evaluator server to get user's poker hands
2. detect best hand

After that compares user's best hands and sends back to client which user have the best hand. If more than one users have best hand, method returns array of users.

Example:

- Request

```
[
  {
    "user": "mio",
    "hand": [ "JD", "10D", "QD", "KD", "AD", "3S", "2S" ]
  },
  {
    "user": "cone",
    "hand": [ "JD", "10D", "QD", "KD", "7S", "3P", "2P" ]
  }
]
```
- Response

```
{
    "mio": {
        "cards": [ "JD", "10D", "QD", "KD", "AD" ],
        "type": "royal_flush"
    }
}
```

## Prerequisites

You will need to install Tealight from Pharo's Catalog Browser.

## Running

To start a web server for the application, run command in Pharo Playground:

    Determiner new server.

Note: Server calls another server (evaluator server). For properly use, you must also start it. Check folder "evaluator".

## License

Copyright © 2017 
