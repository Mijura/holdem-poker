operations
doState: kernel

	| newState |
	
	kernel players: kernel inGame.
	(kernel handFinished & (kernel inGame size>1))
		ifTrue:[
			kernel handFinished: false.
			
			newState:= PreFlopState new.
			kernel gameState: newState.
			newState doState: kernel]
		ifFalse:[
			"send news to all users"
			kernel sender sendPreFlopNews: kernel].
		