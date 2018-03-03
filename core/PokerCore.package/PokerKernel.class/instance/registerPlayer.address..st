operations
registerPlayer: name address: address
	| player |
	player := { 'name' -> name. 'address' -> address. 'chips' -> 2000. 'seat' -> 0. 
					'on move' -> false. 'set player' -> true. 'cards' -> {}. 'bet' -> 0. 'in game' -> false} asDictionary.
	waitingList at: address put: player.	
	^player