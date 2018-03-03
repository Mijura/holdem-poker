operations
send: players address: address
	"send post request to user"
	ZnClient new
   		url: 'http://', address;
   		contentWriter: [ :object | ZnEntity with: (NeoJSONWriter toString: object) type: ZnMimeType applicationJson ];
		contents: players ;
   		post.