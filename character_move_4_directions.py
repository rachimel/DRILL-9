"""방향키로 소년을 이동시키는 pico2d 프로그램."""


from pathlib import Path

import pico2d as p

WIDTH, HEIGHT = 800, 600
RESOURCE_DIR = Path(__file__).resolve().parent


def main():
    p.open_canvas(WIDTH, HEIGHT)
    ground = sheet = None
    try:
        ground = p.load_image(str(RESOURCE_DIR / 'TUK_GROUND.png'))
        sheet = p.load_image(str(RESOURCE_DIR / 'animation_sheet.png'))
        running = True
        while running:
            for event in p.get_events():
                if event.type == p.SDL_QUIT:
                    running = False
            p.clear_canvas()
            ground.draw(WIDTH / 2, HEIGHT / 2, WIDTH, HEIGHT)
            p.update_canvas()
            p.delay(0.01)
    finally:
        ground = sheet = None
        p.close_canvas()


if __name__ == '__main__':
    main()
