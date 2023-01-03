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
        prevpos = (car.x, car.y)
        previntpos = car.intpos
        car.turn(pressed[pygame.K_LEFT], pressed[pygame.K_RIGHT])
        car.accelerate(pressed[pygame.K_UP], pressed[pygame.K_DOWN])
        car_rect = car.update(screen.width, screen.height)

        if element := track.get_element_at(car.intpos, previntpos):
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

        # draw the car
        screen.screen.blit(car_rect, car.rect)

        # update the screen
        pygame.display.flip()

        # tick the pygame clock
        clock.tick(30)
