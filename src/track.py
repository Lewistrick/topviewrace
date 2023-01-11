import json
from collections import defaultdict
from pathlib import Path
from typing import Generator

import pygame
from scipy.ndimage import label
from skimage.draw import line_aa

MAPS_DIR = Path("maps")
MAPS_JSON = json.load((MAPS_DIR / "maps.json").open())

Color = tuple[int, int, int] | list[int, int, int]
Element = tuple[str, int]
Pos = tuple[int, int]
Blob = set[Pos]


class MapLoadingError(ValueError):
    pass


class Track:
    default_colors = {
        "wall": (0, 0, 0),
        "checkpoint": (0, 255, 0),
        "finish": (0, 0, 255),
        "slowdown": (255, 0, 0),
    }

    def __init__(self, name):
        self.name = name
        # find the map
        mapfinder = [m for m in MAPS_JSON["maps"] if m.get("name", "") == self.name]
        if not mapfinder:
            raise MapLoadingError(f"Map {name} not found")

        self.data = mapfinder[0]

        # load the data
        self.author = self.data.get("author", "Unknown")
        self.img = self.data.get("img")
        if not self.img:
            raise MapLoadingError(f"Map {self.name} has no image")
        self.map = pygame.image.load(MAPS_DIR / f"{self.img}")

        # size is determined by the image
        self.width, self.height = self.map.get_size()
        self.rect = self.map.get_rect()

        # initial car position
        if start := self.data.get("start"):
            self.startx, self.starty = start
        else:
            self.startx, self.starty = 20, 20

        # initial car rotation
        self.rotation = self.data.get("rotation", 90)

        # colors for the map elements
        self.colors = {}
        self.elements: dict[str, list[Blob]] = {}
        self.pixel_maps: dict[Pos, Element] = {}
        override_colors: dict[str, Color] = self.data.get("colors", {})
        for element in ("wall", "checkpoint", "finish", "slowdown"):
            if override_color := override_colors.get(element):
                self.colors[element] = override_color
            else:
                self.colors[element] = self.default_colors[element]

            blobs = self.find_element_by_color(element)
            if element == "finish":
                if len(blobs) > 1:
                    raise MapLoadingError(f"Map {self.name} has multiple finishes")
                elif len(blobs) == 0:
                    raise MapLoadingError(f"Map {self.name} has no finish line")

            self.elements[element] = blobs

        self.checkpoints_touched = [False] * len(self.elements["checkpoint"])

    def find_element_by_color(self, element: str) -> list[Blob]:
        """Find all blobs of a certain color on the map."""
        color = self.colors[element]
        # convert the map to a numpy array
        # this is much faster than using get_at()
        arr = pygame.surfarray.array3d(self.map)
        # find all pixels that match the color
        inds = (arr == color).all(axis=2)

        # find all blobs of the color
        labels, n = label(inds)

        # find coordinates of all blobs
        blobs = []
        for i in range(1, n + 1):
            pixels = set(zip(*(labels == i).nonzero()))
            blobs.append(pixels)
            for pixel in pixels:
                self.pixel_maps[pixel] = (element, i - 1)

        return blobs

    def get_elements_between(
        self,
        prevpos: Pos,
        pos: Pos,
        threshold: float = 0.5,
    ) -> Generator[Element, None, None]:
        """Get elements crossed when moving from `prevpos` to `pos`.

        Args:
            prevpos (Pos): Previous position
            pos (Pos): New position

        Returns:
            Generator[Element, None, None]: Generator of elements crossed.
                Elements are (str,int) tuples indicating the element type and the blob
                number to differentiate between multiple elements of the same type.
        """
        # get all pixels crossed when going from prevpos to pos
        rr, cc, vals = line_aa(*prevpos, *pos)

        crossed_totals: dict[Element, float] = defaultdict(float)
        for r, c, v in zip(rr, cc, vals):
            element = self.pixel_maps.get((r, c))
            if not element or crossed_totals[element] > 0.5:
                continue
            crossed_totals[element] += v
            if crossed_totals[element] > 0.5:
                yield element


if __name__ == "__main__":
    testmap = Track("Example map")
