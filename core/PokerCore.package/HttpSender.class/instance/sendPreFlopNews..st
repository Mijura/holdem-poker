operations
sendPreFlopNews: kernel
	"send news to all players"
	(kernel players values) do: [:each | 
		self sendPreFlop: (kernel players values) address: (each at: 'address')].
			
	(kernel waitingList values) do: [:each | 
		self sendPreFlop: (kernel players values) address: (each at: 'address')].