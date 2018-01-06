comparing
= otherHand
	"Answer whether the receiver is equal with otherHand."
	| type1 type2 |
	type1 := (strength at: type) asNumber.
	type2 := (strength at: (otherHand type)) asNumber.
	^(type1 = type2 and: value = otherHand value).