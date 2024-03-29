# Top View Racer

## Installation
- Install Python3.10.
- Clone this repository. Then from its root directory, run the following commands in a terminal:
  - `python -m venv .venv`
  - `.venv\Scripts\activate` (for Linux: `.venv/bin/activate`)
  - `pip install poetry`
  - `poetry install`
  - `poetry run src/main.py`

## Gameplay
- Select a map to play (click the title).
- Use arrow up to accelerate, arrow down to break (neither means slow breaking).
- Use the left and right keys to rotate your car.
- Collect all checkpoints (green) and race to the finish (blue). Avoid red (slowdown).
- If you drive into a wall, your speed will be set to 0.

## Creating maps
- Register a new map in the maps.json file. Specify the following fields:
  - name (the map name)
  - author (the author name)
  - img (the filename of the image, should be in the same folder)
  - start (a list of 2 numbers, indicating x and y coordinates of the car starting position)
  - rotation (the rotation of the car in the starting position, in degrees (0=upward, 90=right, 180=down, 270=left))
- Optionally, define these fields:
  - colors (contains multiple fields, each of which contains a list of 3 numbers for RGB values 0-255:)
    - wall (if not given: [0, 0, 0])
    - checkpoint (if not given: [0, 255, 0])
    - finish (if not given: [0, 0, 255])
    - slowdown (if not given: [255, 0, 0])
- In the 'maps' folder, create a .png file.
  - The colors should correspond to the `colors` field in the JSON.
  - If a color in the image doesn't correspond to either of these elements, it has no effect on the game.
    - wall: you can't drive through them.
    - checkpoint: collect (touch) all of them before driving to the finish.
    - finish: destination of the race.
    - slowdown: reduce your speed

## To do
- Check links
  - https://www.geeksforgeeks.org/how-to-use-multiple-screens-on-pygame/
  - https://www.geeksforgeeks.org/snake-game-in-python-using-pygame-module/

