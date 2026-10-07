"""방향키로 소년을 이동시키는 pico2d 프로그램."""


from math import hypot
from pathlib import Path
from time import perf_counter

import pico2d as p

WIDTH, HEIGHT = 800, 600
RESOURCE_DIR = Path(__file__).resolve().parent


FRAME_SIZE = 100
FRAME_COUNT = 8
ANIMATION_FPS = 8.0
IDLE_ROWS = {1: 300, -1: 200}
WALK_ROWS = {1: 100, -1: 0}
MOVE_SPEED = 10.0
ARROW_KEYS = {p.SDLK_RIGHT, p.SDLK_LEFT, p.SDLK_UP, p.SDLK_DOWN}


class Character:
    def __init__(self):
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.facing = 1
        self.frame = 0
        self.animation_time = 0.0
        self.state = 'IDLE'

    def update(self, dt, keys):
        dx = int(p.SDLK_RIGHT in keys) - int(p.SDLK_LEFT in keys)
        dy = int(p.SDLK_UP in keys) - int(p.SDLK_DOWN in keys)
        previous_state = self.state
        self.state = 'WALK' if dx or dy else 'IDLE'
        entered_idle = self.state == 'IDLE' and previous_state != 'IDLE'
        if entered_idle:
            self.frame = 0
            self.animation_time = 0.0
        new_facing = (-1 if dx < 0 else 1) if dx else self.facing
        direction_changed = self.state == 'WALK' and new_facing != self.facing
        entered_walk = self.state == 'WALK' and previous_state != 'WALK'
        if entered_walk or direction_changed:
            self.facing = new_facing
            self.frame = 0
            self.animation_time = 0.0
        length = hypot(dx, dy)
        if length:
            dx /= length
            dy /= length
        if not entered_idle and not entered_walk and not direction_changed:
            self.animation_time += dt
            self.frame = int(self.animation_time * ANIMATION_FPS) % FRAME_COUNT
        self.x += dx * MOVE_SPEED * dt
        self.y += dy * MOVE_SPEED * dt
        self.x = min(WIDTH - FRAME_SIZE / 2, max(FRAME_SIZE / 2, self.x))

    def draw(self, sheet):
        rows = IDLE_ROWS if self.state == 'IDLE' else WALK_ROWS
        sheet.clip_draw(self.frame * FRAME_SIZE, rows[self.facing], FRAME_SIZE, FRAME_SIZE,
                        self.x, self.y)


def main():
    p.open_canvas(WIDTH, HEIGHT)
    ground = sheet = None
    try:
        ground = p.load_image(str(RESOURCE_DIR / 'TUK_GROUND.png'))
        sheet = p.load_image(str(RESOURCE_DIR / 'animation_sheet.png'))
        character = Character()
        keys = set()
        previous_time = perf_counter()
        running = True
        while running:
            for event in p.get_events():
                if event.type == p.SDL_QUIT:
                    running = False
                elif event.type == p.SDL_KEYDOWN and event.key in ARROW_KEYS:
                    keys.add(event.key)
                elif event.type == p.SDL_KEYUP and event.key in ARROW_KEYS:
                    keys.discard(event.key)
            now = perf_counter()
            dt = now - previous_time
            previous_time = now
            character.update(dt, keys)
            p.clear_canvas()
            ground.draw(WIDTH / 2, HEIGHT / 2, WIDTH, HEIGHT)
            character.draw(sheet)
            p.update_canvas()
            p.delay(0.01)
    finally:
        ground = sheet = None
        p.close_canvas()


if __name__ == '__main__':
    main()
