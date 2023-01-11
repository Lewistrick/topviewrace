import pygame

from car import Car
from track import Track
from ui import Screen


def game_loop(
    screen: Screen,
    track: Track,
    car: Car,
) -> float:
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        # draw background
        screen.update()

        # get pressed keys
        pressed = pygame.key.get_pressed()

        # move the car, given the speed and rotation
        prevpos = car.pos
        previntpos = car.intpos
        # The turn and accelerate methods only change the speed and rotspeed
        # attributes of the car, they don't actually move the car.
        car.turn(pressed[pygame.K_LEFT], pressed[pygame.K_RIGHT])
        car.accelerate(pressed[pygame.K_UP], pressed[pygame.K_DOWN])
        # The update method actually moves the car (using speed and rotspeed),
        # returning the car image rotated to the correct angle.
        car_rect = car.update(screen.width, screen.height)

        for element in track.get_elements_between(previntpos, car.intpos):
            part, i = element
            if part == "wall":
                car.x, car.y = prevpos
                car.speed = 0
                car.rotspeed = 0
            elif part == "checkpoint":
                if not track.checkpoints_touched[i]:
                    print(f"Checkpoint {i} touched!")
                    track.checkpoints_touched[i] = True
            elif part == "slowdown":
                car.slowdown()
            elif part == "finish":
                if all(track.checkpoints_touched):
                    return car.finish()
                else:
                    print("You must touch all checkpoints before the finish line!")

        # draw the car
        screen.screen.blit(car_rect, car.rect)

        # update the screen
        pygame.display.flip()

        # tick the pygame clock
        clock.tick(30)
