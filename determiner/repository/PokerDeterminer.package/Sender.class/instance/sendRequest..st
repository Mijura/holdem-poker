operation
sendRequest: cards
	"send post request to port 3000 and return result"
	| a |
	a:=ZnClient new url: 'http://localhost:3000/recognize';
			accept: ZnMimeType applicationJson;
			contentReader: [ :entity | entity ifNotNil: [ (NeoJSONReader on: (entity contents) readStream)
				mapInstVarsFor: PokerHand ;
				for: #ArrayOfPokerHands
					customDo: [ :mapping | mapping listOfElementSchema: PokerHand  ];
				nextAs: #ArrayOfPokerHands.] ];
			contentWriter: [ :object | ZnEntity with: (NeoJSONWriter toString: object) type: ZnMimeType applicationJson ];
			contents: cards; post.
	^a
	