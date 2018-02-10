operations
doState: kernel

	| newState cards first|
	
	kernel players: kernel inGame.
	(kernel handFinished)
		ifFalse:[
			kernel deck: Deck new.
			
			first := true.
			(kernel players values) do: [:each | 
				cards := (kernel deck get: 2) asSet. 			"two cards for each player"
				each at: 'cards' put: cards.
				(first)
					ifTrue: [each at: 'on move' put: true.  each at: 'big blind' put: 50. ].
				first:= false].
	
			newState:= BetState new. 
			kernel gameState: newState.].
		