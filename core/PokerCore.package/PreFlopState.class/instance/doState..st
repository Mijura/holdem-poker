operations
doState: kernel

	| newState cards first|
	
	kernel players: kernel inGame.
	(kernel handFinished & (kernel inGame size>1))
		ifTrue:[
			kernel handFinished: false.
			kernel deck: Deck new.
			
			first := true.
			(kernel players values) do: [:each | 
				cards := (kernel deck get: 2) asSet. 			"two cards for each player"
				each at: 'cards' put: cards.
				(first)
					ifTrue: [each at: 'on move' put: true].
				first:= false].
	
			newState:= BetState new. 
			kernel gameState: newState.].
	
	"send news to all users"
	(kernel players values) do: [:each | 
		kernel sender sendPreFlop: (kernel players values) address: (each at: 'address')].
			
	(kernel waitingList values) do: [:each | 
		kernel sender sendPreFlop: (kernel players values) address: (each at: 'address')].
		