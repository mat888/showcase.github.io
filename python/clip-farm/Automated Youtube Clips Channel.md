Automated Twitch clip retreiver, editor and poster to Youtube in Python.

Due to the long video render time from the editing library, the project wasn't warranting a PC running for hours per day to do the work, but to make sure the system functioned I did run it for several days, and the results can be seen here.

https://www.youtube.com/channel/UCWEGifuIi9rF3FztK9yP58Q

This challenge presented many challenges along the way, mostly organizational. A unique algorithm had to be made to determine the 'best' clips of the day, and the database had to be kept well organized to keep the project ordered and maintainable. 

The structure of the program consists of several python files responsible for different jobs like fetching, editing and posting clips. To me this was a far more readable version of object oriented programming. Rather than having a few files with many class instantiations, the namespaces were seperated by different files which serve very obvious functions.

This made navigating the codebase very easy, and debugging problems from the top layer to one of the contributing files simple. For large scale projects, this structuring is the preferred method for me.
