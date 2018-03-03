operations
moveInGame: address seat: seat
	| player |
	player := waitingList at: address.
	player at: 'seat' put: seat.				"updating seat number, because it was set to 0 on creation"		
	inGame at: seat put: player.
	waitingList removeKey: address.