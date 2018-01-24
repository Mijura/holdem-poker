server handling
core

	| kernel teapot |
	
	kernel := PokerKernel new.
	teapot := Teapot configure: { #defaultOutput -> #json. #port -> 8080. #debugMode -> true }.
	
	teapot
		GET: '/players' -> kernel players;
		
   		GET: '/inGame' -> kernel inGame;
		
		GET: '/waitingList' -> kernel waitingList;
		
   		POST: '/registerPlayer' -> [ :req | kernel registerPlayer: (req at: #name) address: (req at: #address)];
																				
		POST: '/takeSeat' -> [ :req | kernel takeSeat: (req at: #seat) address: (req at: #address)];
		
   		
   		start.