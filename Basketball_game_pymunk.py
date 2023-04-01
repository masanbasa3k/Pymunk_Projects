import pygame
import pymunk
import pymunk.pygame_util
import math

pygame.init()
global ball
ball = None

global score
score = 0

WIDTH, HEIGHT = 1200,800
window = pygame.display.set_mode((WIDTH, HEIGHT))

STAT_FONT = pygame.font.SysFont("comicsans", 50)

def calculate_distance(p1, p2):
    return math.sqrt((p2[1] - p1[1])**2 + (p2[0] - p1[0])**2)

def calculate_angle(p1, p2):
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])

def draw(window, space, draw_options, line, score):
    window.fill("white")

    text = STAT_FONT.render("Score: " + str(score), 1, (85,0,0))
    window.blit(text, ((WIDTH/2) - text.get_width(), 10))

    if line:
        pygame.draw.line(window, "black", line[0], line[1], 3)

    space.debug_draw(draw_options)

    pygame.display.update()

def create_boundaries(space, width, height, group):
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
        shape = pymunk.Poly.create_box(body, size, radius=1)
        # for bounce
        shape.elasticity = 0.4
        shape.friction = 0.5
        space.add(body, shape)

def create_scructure(space, width, height, group):
    BLUE = (113, 164, 164, 100)
    NOC = (0, 0, 0, 10)
    rects = [
        [(900, height - 450), (10, 200), BLUE, 100],
        [(750, height - 400), (10, 20), BLUE, 150],
        [(950, height - 400), (100, 20), BLUE, 150],
        [(1000, height - 220), (20, 400), BLUE, 150]
    ]

    for pos, size, color, mass in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size, radius=1)
        shape.filter = pymunk.ShapeFilter(group=group)
        shape.color = color
        shape.mass = mass
        shape.elasticity = 0.4
        shape.friction = 0.4
        space.add(body, shape)

def create_pota(space, width, height, group):
    NOC = (0, 0, 0, 10)
    rects = [
        [(825, height - 400), (150, 5), NOC, 150]
    ]

    for pos, size, color, mass in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size, radius=1)
        shape.filter = pymunk.ShapeFilter(group=group)
        shape.collision_type = 2
        shape.color = color
        shape.mass = mass
        shape.elasticity = 0.4
        shape.friction = 0.4
        space.add(body, shape)

class Ball:
    def __init__(self, space, radius, mass, pos, group):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = pos
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.mass = mass
        self.shape.filter = pymunk.ShapeFilter(group=group)
        self.shape.collision_type = 1
        # for bounce
        self.shape.elasticity = 1
        self.shape.friction = 0.4
        self.shape.color = (250, 131, 32 , 100)#rgb and alpha
        space.add(self.body, self.shape)

    def remove(self, space):
        space.remove(self.body, self.shape)


def collision(arbiter, space, data):
    global ball
    global score

    ball.remove(space)
    ball = None

    score += 1

    return True

def run(window, width, height):
    run = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1 / fps # delta_time

    space = pymunk.Space()
    space.gravity = (0, 981)

    # ball = create_ball(space, 30, 10)
    create_boundaries(space, width, height, 2)
    create_scructure(space, width, height, 2)
    pota = create_pota(space, width, height, 2)

    handler = space.add_collision_handler(1, 2)
    handler.begin = collision
    
    draw_options = pymunk.pygame_util.DrawOptions(window)

    pressed_pos = None

    global ball
    ball = None

    global score
    score = 0

    while run:
        line = None
        if ball:
            if pressed_pos:
                line = [pressed_pos, pygame.mouse.get_pos()]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not ball:
                    pressed_pos = (200,600)
                    ball = Ball(space, 25, 10, pressed_pos, 1)
                elif pressed_pos:
                    ball.body.body_type = pymunk.Body.DYNAMIC
                    angle = calculate_angle(*line)
                    force = calculate_distance(*line) * 40
                    fx = math.cos(angle) * force
                    fy = math.sin(angle) * force
                    ball.body.apply_impulse_at_local_point((fx, fy), (0, 0))
                    pressed_pos = None
                else:
                    ball.remove(space)
                    ball = None

        draw(window, space, draw_options, line, score)
        space.step(dt)
        clock.tick(fps)

    pygame.quit()

if __name__ == "__main__":
    run(window,WIDTH,HEIGHT)
