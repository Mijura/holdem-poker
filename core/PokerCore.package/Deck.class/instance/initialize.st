initialize
initialize
	| numbers suits|
	
	numbers := Array newFrom: #('2' '3' '4' '5' '6' '7' '8' '9' '10' 'J' 'Q' 'K' 'A').
	suits := Array newFrom: #('C' 'D' 'H' 'S' ).
	cards := OrderedCollection new.
	numbers do: [:n | 
		suits do: [:s | cards add: n,s. ].].
	cards := cards asSet asOrderedCollection shuffled. 