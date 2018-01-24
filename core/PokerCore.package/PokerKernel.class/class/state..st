initialization
state: state 
	| kernel |
	kernel := PokerKernel new.
	kernel state: state.
	^kernel