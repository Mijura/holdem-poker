comparing
> otherHand
	"Answer whether the receiver is stronger hand than otherHand."
	| type1 |
	type1 := strength at: type.
	((strength at: type) asNumber > (strength at: (otherHand type)) asNumber) ifTrue: [^true].
	((strength at: type) asNumber = (strength at: (otherHand type)) asNumber) ifTrue: [^value > otherHand value].
	^false.
	