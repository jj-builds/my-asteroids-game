# My-asteroids-game
## Introduction
This is a recreation of the classsic game of asteroids. You
move by wasd or the arrow keys. Press space to fire. Run
into red circles to gain one shield. You have a max of one
shield. The asteroids are white circles. Shoot the yellow
circles to find out what they do! 

## Installation
If you don't have uv, pygame, git, or python installed,
install them (see **More Installation**). Then run `mkdir asteroids cd asteroids`. Then run `git pull https://github.com/jj-builds/my-asteroids-game main`  or `git clone https://github.com/jj-builds/my-asteroids-game.git` in your terminal. This
makes a copy of it on your computer since I haven't figured
out how to run it on GitHub. To run the game, run `uv run main.py` (again, in your terminal). This will open a new
window with the game.

## More Installation
Run this command to install homebrew: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`. After that, run `brew install neovim` . If you're in your home directory (the command line has ~ near the end, which you probably are, if you're not, run `cd ~`), run `ls -a`. Then open your .zshrc or .bashrc file (`nvim <FILE>`) (Note: replace <FILE> with .bashrc or .zshrc) and press the i key to enter insert mode. Then add this line to the bottom: `export PATH="/opt/homebrew/bin:$PATH"`. Then type this `:wq`. That will exit out of the file and save it. Finally, run `brew install uv python git` and `uv pip install pygame`

## Obvious bugs
When the asteroids collide with the shield but not the 
player, nothing happens. That is because only if the 
asteroids collide with the player the shield gets removed. 
Also, sometimes the game ends when the player flies close 
to an asteroid but not touching it. That is because the 
player is represented as a circle for collision detection.
Please report other bugs [here](https://github.com/jj-builds/my-asteroids-game/issues) so that I can fix them.

## Upcoming features
* fuel limit & refueling
* ammunition limit & reloading

## Other notes
* I'm a beginner so please don't judge me
* Please edit the `print(high score 1294 by jj-builds)` line when you get a higher score to say `print(high score <SCORE> by <YOURNAME>)`
Note: replace `<SCORE>` with your score and `<YOURNAME>` with your name.
