"""방향키로 소년을 이동시키는 pico2d 프로그램."""


from pathlib import Path

import pico2d as p

WIDTH, HEIGHT = 800, 600
RESOURCE_DIR = Path(__file__).resolve().parent


def main():
    p.open_canvas(WIDTH, HEIGHT)
    ground = None
    try:
        ground = p.load_image(str(RESOURCE_DIR / 'TUK_GROUND.png'))
        running = True
        while running:
            for event in p.get_events():
                if event.type == p.SDL_QUIT:
                    running = False
            p.clear_canvas()
            p.update_canvas()
            p.delay(0.01)
    finally:
        ground = None
        p.close_canvas()


if __name__ == '__main__':
    main()
