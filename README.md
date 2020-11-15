# Labylib - Animated Textures
Animated textures for Labymod.

This is a sample program for VictorWesterlund/labylib

[Supported Labymod cosmetics](https://github.com/VictorWesterlund/labylib#supported-cosmetics) more coming soon!

## Installation
1. Download and install [Python 3.x.x](https://www.python.org/downloads/) for your computer's architecture
2. Clone this repo to your machine, or [download a zip](/VictorWesterlund/labylib-animated-textures/archive/master.zip) if you don't speak git
```bash
$ git clone https://github.com/VictorWesterlund/labylib-animated-textures/
$ gh repo clone VictorWesterlund/labylib-animated-textures
```
3. Extract/copy the `labylib` folder into your project (or make it a dependancy)

## Quickstart
1. Upload textures to the texture folder(s) found in `~/animated-textures/<cosmetic>`.
```
~/animated-textures/cape/coolCape-1.png
~/animated-textures/cape/coolCape-2.png
~/animated-textures/cape/coolCape-3.png
...
```
2. Run `start.py` from a Python 3.x.x CLI
```bash
$ python3 start.py
```
3. The program will ask you if you want to start a guided setup (first time). Type `y` and/or press <kbd>⏎ Enter/Return</kbd>
4. You are now asked to provide a `PHPSESSID`; This is the core-functionality of labylib. [Here's how you locate your `PHPSESSID`](https://github.com/VictorWesterlund/labylib#find-your-phpsessid-cookie). Once you've located your `PHPSESSID`-cookie. Paste it and press <kbd>⏎ Enter/Return</kbd>
5. Type `n` and/or press <kbd>⏎ Enter/Return</kbd> to skip advanced configuration.
6. That should be it! Type `y` and/or press <kbd>⏎ Enter/Return</kbd> to start
...
7. To exit the program, Type `stop` and/or press <kbd>⏎ Enter/Return</kbd> (<kbd>Ctrl</kbd>+<kbd>C</kbd> a few times to force quit; still in pre-release after all)
