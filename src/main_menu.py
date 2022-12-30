import pygame

from track import MAPS_DIR, MAPS_JSON
from ui import Screen

pygame.font.init()

tit = pygame.font.SysFont("Arial", 50, bold=True)
sub = pygame.font.SysFont("Arial", 30, bold=True)
fnt = pygame.font.SysFont("Arial", 25)
ita = pygame.font.SysFont("Arial", 25, italic=True)


def main_menu(screen: Screen) -> str:
    clock = pygame.time.Clock()

    showing_map = None
    prev_shown_map = None

    # main menu
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        # show title
        title = tit.render("TopView Racer", True, (255, 255, 255))
        screen.draw(title, (screen.width / 2 - title.get_width() / 2, 40))

        # load all maps
        maps = {m["name"]: m for m in MAPS_JSON["maps"]}

        # show all maps
        select_map = sub.render("Select a map", True, (255, 255, 255))
        screen.draw(select_map, (100, 150))

        mapname_rects = {}
        curry = 200
        for mapname, mapdata in maps.items():
            # show the name of the map
            name = fnt.render(mapname, True, (255, 255, 255))
            screen.draw(name, (100, curry))
            mapname_rects[mapname] = name.get_rect(topleft=(100, curry))
            # show the author of the map
            author = ita.render(f"by {mapdata['author']}", True, (155, 155, 155))
            screen.draw(author, (250, curry))
            # update the y position for the next map
            curry += 30

        # check if mouse is over a map
        mouse = pygame.mouse.get_pos()
        for mapname, rect in mapname_rects.items():
            if rect.collidepoint(mouse):
                showing_map = mapname
                if pygame.mouse.get_pressed()[0]:
                    return mapname
                break

        # show the map
        if showing_map != prev_shown_map:
            mapdata = maps[showing_map]
            map_img = pygame.image.load(MAPS_DIR / mapdata["img"])
            map_w, map_h = map_img.get_size()

            print(f"Map size: {map_w}x{map_h}")

            thumbsize_max = (600, 500)
            thumb_w: float = map_w
            thumb_h: float = map_h
            if thumb_w > thumbsize_max[0]:
                thumb_w = thumbsize_max[0]
                thumb_h = thumb_h / thumb_w * thumbsize_max[0]
            if thumb_h > thumbsize_max[1]:
                thumb_h = thumbsize_max[1]
                thumb_w = thumb_w / thumb_h * thumbsize_max[1]

            thumb_size = (int(thumb_w), int(thumb_h))

            map_thumb = pygame.transform.scale(map_img, thumb_size)
            border = pygame.Surface((thumb_size[0] + 10, thumb_size[1] + 10))
            border.fill((100, 100, 100))
            screen.draw(border, (395, 195))

            screen.draw(map_thumb, (400, 200))

            prev_shown_map = showing_map

        pygame.display.flip()
        clock.tick(30)
