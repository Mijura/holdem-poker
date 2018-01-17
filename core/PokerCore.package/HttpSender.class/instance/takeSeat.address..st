operation
takeSeat: user address: address
	"send post request to user"
	| addr message a |
	addr := 'http://' , address.
	message := Dictionary newFrom: { 'message'-> 'take seat' . 'name'-> (user at: 'name'). 'chips'-> (user at: 'chips'). 'seat'-> (user at: 'seat').}.
	a := ZnClient new
   		url: addr;
		enforceHttpSuccess: true;
   		ifFail: [ :ex | self inform: 'Cannot get numbers: ', ex printString ];
   		contentWriter: [ :object | ZnEntity with: (NeoJSONWriter toString: object) type: ZnMimeType applicationJson ];
		contents: message ;
   		post.
	^a