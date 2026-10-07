"""방향키로 소년을 이동시키는 pico2d 프로그램."""


import pico2d as p

WIDTH, HEIGHT = 800, 600


def main():
    p.open_canvas(WIDTH, HEIGHT)
    try:
        running = True
        while running:
            for event in p.get_events():
                if event.type == p.SDL_QUIT:
                    running = False
            p.delay(0.01)
    finally:
        p.close_canvas()


if __name__ == '__main__':
    main()
