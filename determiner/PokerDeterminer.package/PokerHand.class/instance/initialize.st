initialize
initialize
	super initialize .

	strength := Dictionary newFrom: { 'high_card'-> 1 . 
												'pair'-> 2 .
												'two_pairs'-> 3 . 
												'three_of_a_kind'-> 4 .
												'straight'-> 5 .
												'flush'-> 6 .
												'full_house'-> 7 .
												'poker'-> 8 .
												'straight_flush'-> 9 .
												'royal_flush'-> 10}.