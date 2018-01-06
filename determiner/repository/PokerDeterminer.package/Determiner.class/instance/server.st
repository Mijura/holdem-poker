server handling
server
	
	|teapot result sender |
	result := Dictionary new.
	sender := Sender new.
	teapot := Teapot configure: {
 		#defaultOutput -> #json. #port -> 8000. #debugMode -> true }.
	teapot
   		POST: '/bestHand' -> [ :req | | users user_hands max largest best|
     		users := (NeoJSONReader on: (req at: #hands) readStream)
						propertyNamesAsSymbols: true;
						next.
			best := Dictionary new.
			users do: [:each | 
				user_hands:= sender sendRequest: (each at: #hand).
				max:=user_hands at: 1.
				user_hands do: [:e | (e>max) ifTrue: [max:=e]].
				best at: (each at: #user) put: max
			].
				
			max := nil. 
			largest := nil.
			best keysAndValuesDo: [:k :v |
  				(max isNil or: [v > largest])
    				ifTrue: [				
						max := k.
      					largest := v.
					 	result := Dictionary new].
				(largest=v)ifTrue:[result at: k put: v asDictionary ]].
			result 
		];
   		exception:
      		KeyNotFound -> (TeaResponse notFound body: 'KeyNotFound');
   		start. 