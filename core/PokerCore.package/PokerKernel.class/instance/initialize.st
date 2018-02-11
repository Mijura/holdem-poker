initialize
initialize
	super.
	gameState := WaitState new.
	deck := nil.
	waitingList := Dictionary new.
	inGame := Dictionary new.
	sender := HttpSender new.
	players := Dictionary new.
	on_move := nil.
	started := nil.
	handFinished := true.