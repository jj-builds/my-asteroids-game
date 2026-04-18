# My-asteroids-game
## Introduction
This is a recreation of the classsic game of asteroids. You
move by wasd or the arrow keys. Press space to fire. Run
into red circles to gain one shield. You have a max of one
shield. The asteroids are white circles. Shoot the yellow
circles to find out what they do! 

## Installation
If you don't have uv, pygame, git, or python installed,
install them. Then run `git pull https://github.com/jj-builds/my-asteroids-game main` in your terminal. This
makes a copy of it on your computer since I haven't figured
out how to run it on GitHub. To run the game, run `uv run main.py` (again, in your terminal). This will open a new
window with the game.

## Obvious bugs
When the asteroids collide with the shield but not the 
player, nothing happens. That is because only if the 
asteroids collide with the player the shield gets removed. 
Also, sometimes the game ends when the player flies close 
to an asteroid but not touching it. That is because the 
player is represented as a circle for collision detection.
Please report other bugs on GitHub so that I can fix them.

## Other notes
- I'm a beginner so don't judge me
- Please edit the `print(high score 357 by jj-builds)` line when you get a higher score to say `print(high score <SCORE> by <YOURNAME>)`
Note: replace <SCORE> with your score and <YOURNAME> with your name.