operations
takeSeat: seat address: address

	| result |
	(inGame includesKey: seat) 														
		ifFalse: [
			self moveInGame: address seat: seat. 	"if the seat is freely, moves the player from waiting list into a game"
			
			gameState doState: self.
			
			"send news to all users"
			(players values) do: [:each | 
				sender sendPreFlop: (players values) address: (each at: 'address')].
			
			(waitingList values) do: [:each | 
				sender sendPreFlop: (players values) address: (each at: 'address')].
	
			result := inGame]										"operation is succesful"
 		ifTrue: [result := 0].							"if the seat isn't freely, operation is unsuccessful"
	^result		