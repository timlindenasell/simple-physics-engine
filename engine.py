from pyglet.window import mouse
from configparser import ConfigParser
from core import Environment
from components import Rectangle
from vector import Vector

import pyglet

# TODO: OPTIMIZE physics calculations to only occur if necessary e.g. when colliding


def setup_window():
    # Get values from 'config.ini'
    config = ConfigParser()
    config.read('config.ini')
    win_width = int(config['Window']['Width'])
    win_height = int(config['Window']['Height'])

    # setup window
    window = pyglet.window.Window(width=win_width, height=win_height)

    return window


def update(frame_dt, dt):
    Environment.update(dt)


def create_batch():
    batch = pyglet.graphics.Batch()
    for po in Environment.physics_objects:
        batch.add(*po())

    return batch


def run():
    rect_one = Rectangle(Vector(500, 500), 1000, 100, 200)
    rect_two = Rectangle(Vector(450, 100), 100, 100, 100, v=Vector(0,40))
    rect_two = Rectangle(Vector(900, 100), 100, 100, 100, v=Vector(-40,40))


    window = setup_window()

    # Move rect_one to left mouse-click position
    @window.event
    def on_mouse_press(x, y, button, modifiers):
        if button == mouse.LEFT:
            print(x, y)
            # rect_one.pos.x = x
            # rect_one.pos.y = y

    @window.event
    def on_draw():
        window.clear()
        batch = create_batch()
        batch.draw()

    dt = 1/60.0
    frame_dt = 1/60.0
    pyglet.clock.schedule_interval(update, frame_dt, dt)
    pyglet.app.run()


if __name__ == '__main__':
    run()
