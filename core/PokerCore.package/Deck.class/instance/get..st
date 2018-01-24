accessing
get: number
	
	| result |
	result := cards first: number.
	cards removeFirst: number.
	^result