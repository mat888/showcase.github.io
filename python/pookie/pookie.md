Pookie! Pookie is the first serious game I have ever programmed. Inspired by a recent obsession with poker, I wanted to make 'poker-lite,' and I wanted to play it with friends. Pookie is structured much like poker with two rounds of betting, distribution of 'hands' and 'community points' which together determine final scores. 

Internally, apart from cards being simplified to personal numbers (1 - 10) and a community number (1 - 20) which are revealed in seperate turns and together determine final player scores, the game functions just like poker. A round of gameplay takes place within one class instantiation composed with of all the functions necessary. 

A particular pride point is the recursive algorithm (one that calls itself internally) to determine whose turn it is to bet, which has to end sometime but in certain cases can go on forever. This is `functional_betting` in the file. The game is completely interface through a Discord (social media platform) bot API library.

If I were to remake this I would focus on, as much as possible, seperating the game logic from the Discord IO, such that the game could be easily extracted and adapted to work on any platform.