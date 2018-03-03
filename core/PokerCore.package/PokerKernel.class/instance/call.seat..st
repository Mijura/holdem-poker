operations
call: call seat: seat
	| player chips bet index result|
	
	player := players at: seat.
	(player at: 'on move') 														
		ifTrue: [
			chips := (player at: 'chips') - (call asNumber).
			bet := (player at: 'bet') + (call asNumber).
			player at: 'chips' put: chips.
			player at: 'bet' put: bet.		
			player at: 'on move' put: false.
			
			index := self on_move.
			
			(index == players size)
				ifTrue:[ self on_move: 1]								"end of array - create cycle"
				ifFalse:[ self on_move: (index + 1)].				"next player is on move"
			
			player := players values at: (self on_move).	
			player at: 'on move' put: true.
			
			gameState doState: self.
			result := true]
		ifFalse: [ result := false].
	^result
