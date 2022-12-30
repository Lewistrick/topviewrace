import pygame

from track import Track


class Screen:
    def __init__(
        self,
        width,
        height,
        bgcolor=(0, 0, 0),
        bgimage: pygame.Surface | None = None,
    ):
        self.width = width
        self.height = height
        self.bgcolor = bgcolor
        self.bgimage = bgimage
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.update()

    @classmethod
    def from_track(cls, track: Track):
        return cls(track.width, track.height, bgimage=track.map)

    def draw(self, image, pos):
        """Draw something to the screen on a given position.

        Args:
            image (pygame.Surface): The element (image, text, shape) to draw.
            pos (tuple[int, int]): The position to draw the element.
        """
        self.screen.blit(image, pos)

    def update(self):
        """Update the screen."""
        self.screen.fill(self.bgcolor)

        # background image (if given, should be a pygame.image)
        if self.bgimage:
            self.screen.blit(self.bgimage, (0, 0))


class Button:
    def __init__(self, x, y, width, height, text, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.SysFont("Arial", 30)
        text = font.render(self.text, True, (0, 0, 0))
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
