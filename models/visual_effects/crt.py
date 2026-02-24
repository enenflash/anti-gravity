import random, pygame as pg
from src.settings import *

# SEE MORE AT https://dev.to/chrisgreening/simulating-simple-crt-and-glitch-effects-in-pygame-1mf1

SCAN_IMG = pg.Surface((SCREEN_W, SCREEN_H), pg.SRCALPHA)
for y in range(0, SCREEN_H, 4):
    pg.draw.line(SCAN_IMG, (0, 0, 0, 60), (0, y), (SCREEN_W,  y))

def _apply_flicker(screen):
    if random.randint(0, 20) == 0:
        flicker_surface = pg.Surface(screen.get_size(), pg.SRCALPHA)
        flicker_surface.fill((255, 255, 255, 5))
        screen.blit(flicker_surface, (0, 0))

def _apply_glow(screen):
    width, height = screen.get_size()
    glow_surf = pg.transform.smoothscale(screen, (width // 10, height // 10))
    glow_surf = pg.transform.smoothscale(glow_surf, (width, height))
    glow_surf.set_alpha(80)
    screen.blit(glow_surf, (0, 0))

def _add_glitch_effect(height, width, glitch_surface, intensity):
    shift_amount = {"minimum": 10, "medium": 20, "maximum": 40}.get(intensity, 20)
    if random.random() < 0.06:
        y_start = random.randint(0, height - 20)
        slice_height = random.randint(5, 20)
        offset = random.randint(-shift_amount, shift_amount)

        slice_area = pg.Rect(0, y_start, width, slice_height)
        slice_copy = glitch_surface.subsurface(slice_area).copy()
        glitch_surface.blit(slice_copy, (offset, y_start))

def _add_color_separation(screen, glitch_surface, intensity):
    color_shift = {"minimum": 2, "medium": 6, "maximum": 10}.get(intensity, 4)
    if random.random() < 0.05:
        for i in range(3):
            x_offset = random.randint(-color_shift, color_shift)
            y_offset = random.randint(-color_shift, color_shift)
            color_shift_surface = glitch_surface.copy()
            color_shift_surface.fill((0, 0, 0))
            color_shift_surface.blit(glitch_surface, (x_offset, y_offset))
            screen.blit(color_shift_surface, (0, 0), special_flags=pg.BLEND_ADD)

def _add_rolling_static(screen, height, width, intensity):
    static_chance = {"minimum": 0.1, "medium": 0.3, "maximum": 0.8}.get(intensity, 0.2)
    static_surface = pg.Surface((width, height), pg.SRCALPHA)

    for y in range(0, height, 8):
        if random.random() < static_chance:
            pg.draw.line(static_surface, (255, 255, 255, random.randint(30, 80)), (0, y), (width, y))

    screen.blit(static_surface, (0, 0), special_flags=pg.BLEND_ADD)

def apply_crt(surface:pg.Surface):
    surface.blit(SCAN_IMG, (0, 0))
    _apply_glow(surface)

    glitch_surf = surface.copy()
    for _ in range(4):
        _add_glitch_effect(SCREEN_H, SCREEN_W, glitch_surf, "medium")
    _add_color_separation(surface, glitch_surf, "medium")
    # add_rolling_static(surface, SCREEN_H, SCREEN_W, "medium")

    surface.blit(glitch_surf, (0, 0))