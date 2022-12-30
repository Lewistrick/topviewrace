import pygame

from car import Car
from game_loop import game_loop
from main_menu import main_menu
from track import Track
from ui import Screen

pygame.init()
pygame.display.set_caption("TopView Racer")

# UI settings
size = width, height = 1200, 800
posx: float = 200
posy: float = 200
rotation: float = 0

if __name__ == "__main__":
    screen = Screen(width, height)
    choice = main_menu(screen)

    # load the map
    print(f"Loading map {choice}...")
    track = Track(choice)
    screen = Screen.from_track(track)

    # load the car image
    car = Car(track.startx, track.starty, track.rotation)
    t = game_loop(screen, track, car)

    print(f"Finished in {t:.2f} seconds!")
