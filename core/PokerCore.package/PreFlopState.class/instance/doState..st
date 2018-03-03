operations
doState: kernel

	| newState cards vals index|
	
	kernel players: kernel inGame.
	(kernel handFinished)
		ifFalse:[
			kernel deck: Deck new.
			
			vals := kernel players values.
			vals do: [:each | 
				cards := (kernel deck get: 2) asSet. 			"two cards for each player"
				each at: 'cards' put: cards.
				each at: 'in game' put: true.].
			
			"determination big blind, small blind and which player is on the move"
			((kernel started) isNil)									"previous state was WaitState - there are only two players at table"
				ifTrue: [kernel on_move: 1.
							kernel started: 1.
							vals first at: 'on move' put: true.
							vals first at: 'chips' put: ((vals first at: 'chips') - 25).
							vals first at: 'bet' put: 25. 
							vals second at: 'bet' put: 50. 
							vals second at: 'chips' put: ((vals second at: 'chips') - 50).] 
				ifFalse:[
							index := kernel started.
							(index == vals size)
								ifTrue:[kernel started: 1.]								"end of array - create cycle"
								ifFalse:[kernel started: (index + 1).].				"next player is on move"
							vals at: (kernel started) at: 'on move' put: true.
							vals at: (index-1) at: 'chips' put: ((vals first at: 'chips') - 25).
							vals at: (index-1) at: 'bet' put: 25.
							vals at: index at: 'bet' put: 50.
							vals at: index at: 'chips' put: ((vals second at: 'chips') - 50).
							
					].

			newState:= BetState new.
			kernel gameState: newState.
			
			"send news to all users"
			kernel sender sendNews: kernel].
	
		