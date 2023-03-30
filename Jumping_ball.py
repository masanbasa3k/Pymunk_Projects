import pygame
import pymunk
import pymunk.pygame_util
import math

pygame.init()

WIDTH, HEIGHT = 1000,800
window = pygame.display.set_mode((WIDTH, HEIGHT))

def draw(window, space, draw_options):
    window.fill("white")
    space.debug_draw(draw_options)
    pygame.display.update()

def create_boundaries(space, width, height):
    rects = [
        [(width/2, height - 10), (width, 20)],
        [(width/2, 10), (width, 20)],
        [(10, height/2), (20, height)],
        [(width - 10, height/2), (20, height)]
             ]
    
    for pos, size in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)# make it static
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        # for bounce
        shape.elasticity = 0.4
        shape.friction = 0.5
        space.add(body, shape)


def create_ball(space, radius, mass):
    body = pymunk.Body()
    body.position = (300, 300)
    shape = pymunk.Circle(body, radius)
    shape.mass = mass
    # for bounce
    shape.elasticity = 0.9
    shape.friction = 0.4
    shape.color = (255, 0, 0 , 100)#rgb and alpha
    space.add(body, shape)

    return shape

def run(window, width, height):
    run = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1 / fps # delta_time

    space = pymunk.Space()
    space.gravity = (0, 981)

    ball = create_ball(space, 30, 10)
    create_boundaries(space, WIDTH, HEIGHT)

    draw_options = pymunk.pygame_util.DrawOptions(window)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            ball.body.apply_force_at_local_point((-1000, 0))
        elif keys[pygame.K_a]:
            ball.body.apply_force_at_local_point((1000, 0))
        elif keys[pygame.K_SPACE] and ball.body.velocity.y == 0:
            ball.body.apply_impulse_at_local_point((0, -10000))


        draw(window, space, draw_options)
        space.step(dt)
        clock.tick(fps)

    pygame.quit()

if __name__ == "__main__":
    run(window,WIDTH,HEIGHT)