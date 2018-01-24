operations
registerPlayer: name address: address
	| player |
	player := { 'name' -> name. 'address' -> address. 'seat' -> 0. 'chips' -> 2000} asDictionary.
	waitingList at: address put: player.	
	^player