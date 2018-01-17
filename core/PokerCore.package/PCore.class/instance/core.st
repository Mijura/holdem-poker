server handling
core

	| users seats sender teapot |
	users := Dictionary new.
	seats := Dictionary new.
	sender := HttpSender new.
	teapot := Teapot configure: {
   		#defaultOutput -> #json. #port -> 8080. #debugMode -> true }.
	teapot
   		GET: '/users' -> users;
   		POST: '/addUser' -> [ :req | | user |
      		user := {'name' -> (req at: #name).
						'seat' -> 0.
						'chips' -> 2000} asDictionary.
      		users at: (req at: #address) put: user.
		 	user];
		POST: '/takeSeat' -> [ :req | | res seat user|
			seat := (req at: #seat) asInteger.
			(seats includesKey: (req at: #address)) 
				ifFalse: [seats at: (req at: #address) put: seat.
							 user := users at: (req at: #address).
							 user at:'seat' put: seat.
							 users at: (req at: #address) put: user.
							 sender takeSeat: (users at: (req at: #address)) address: (req at: #address).
							 res:=1]
 				ifTrue: [res := 0].
			res		
		];
   		DELETE: '/users/<address>' -> [ :req | users removeKey: (req at: #address) ];
   		exception:
      		KeyNotFound -> (TeaResponse notFound body: 'Param Error');
   		start.