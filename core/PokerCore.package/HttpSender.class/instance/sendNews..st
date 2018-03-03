operations
sendNews: kernel
	"send news to all players"
	(kernel players values) do: [:each | 
		self send: (kernel players values) address: (each at: 'address')].
			
	(kernel waitingList values) do: [:each | 
		self send: (kernel players values) address: (each at: 'address')].