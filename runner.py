import pygame

from sim_config import Config

from world import World
import layouts
from bird import Bird
import intruder
from tracer import Tracer
import numpy as np

from pygame.locals import (
    K_s,
    K_t,
    KEYDOWN,
    QUIT,
    K_SPACE,
    MOUSEBUTTONDOWN,
)

width = 1200
height = 700
data_height = 200

good_count = 50
bad_count = 10
bird_count = good_count + bad_count

chart = True

w = layouts.HourGlass(width, height, good_count, bad_count, p_std=10, v_std=0.4, intruder_type=intruder.NonFlocker)

screen = pygame.display.set_mode((width, height+data_height))
data_screen = screen.subsurface(pygame.Rect(0, height, width, data_height))


charter = Tracer(width, data_height, 100, good_count, bad_count)

pygame.init()
fixed_wing_img = pygame.transform.scale(pygame.image.load('version_1.0/images/fixed_wing.png'), (20, 20))
bad_img = pygame.transform.scale(pygame.image.load('version_1.0/images/bad.png'), (20, 20))
target_img = pygame.transform.scale(pygame.image.load('version_1.0/images/flag.png'), (20, 20))

font = pygame.font.SysFont(None, 72)

iteration_count = 0

def main():
    running = True
    t = 0
    config = Config()
    avg_fr = 0
    count = 0
    total = 0

    while running:
        # calculate delta t (time since last frame)
        # variable frame-rate is useful for visualization
        # for pure simulation (no graphics), this is irrelevant

        (dt, count, total, avg_fr, t) = get_dt(count, total, avg_fr, t)

        # print(dt)
        # ignore frames that are too 'long'
        # if not, birds may suddenly 'skip' long distances
        # if dt > 50:
        #     print('whoops. That frame took ' + str(dt) + ' ms')
        # continue

        # the exit event is needed to stop this while loop
        # all other events are handled in handle_event() for cleaner code
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            else:
                handle_event(event, w, config)

        # make world update itself one time-step
        if not config.pause:
            w.update(1)
            config.iteration_count += 1
            distances = np.sort(w.distances, axis=0)
            # print(distances[1:6][:])
            print(np.sum(distances[1:7][:])/(bird_count*5))

        if chart and not config.pause:
            charter.track(w)

        # draw new frame
        draw(screen, w, avg_fr, config)

        if config.iteration_count == 2000:
            config.pause = True


def set_target(m_pos, w):
    w.targets.append(pygame.Vector2(int(m_pos[0]), int(m_pos[1])))


def draw_groups(screen, world):
    for bird in world.birds:
        for n in bird.neighbours:
            neighbor = world.birds[n]

            edge_color = 0
            pygame.draw.line(screen, (edge_color, edge_color, edge_color), bird.p, neighbor.p, int(1))


def handle_event(e, w, c):
    m_pos = pygame.mouse.get_pos()

    if e.type == MOUSEBUTTONDOWN:
        if e.button == 1:
            set_target(m_pos, w)

    elif e.type == KEYDOWN:
        if e.key == K_s:
            c.draw_groups = not c.draw_groups
        elif e.key == K_SPACE:
            c.pause = not c.pause
            if charter.TP + charter.FN > 0:
                P = charter.TP + charter.FN
                N = charter.TN + charter.FP
                print(c.iteration_count, charter.TP / P, charter.FP / N, charter.TP, charter.FP, charter.TN, charter.FN)
        elif e.key == K_t:
            charter.reset_confusion_matrix()


def draw_target(surface, t):
    pos = (int(t[0]), int(t[1]))
    surface.blit(target_img, (int(t[0])-10, int(t[1])-10))
    pygame.draw.circle(surface, (0, 0, 0), pos, int(World.target_range), 1)


# this function outlines the task of drawing
def draw(surface, w, dt, config):
    # fill the screen with white
    surface.fill((250, 250, 250))
    delta_text = font.render(str(dt), True, (0, 0, 0))
    surface.blit(delta_text, (10, w.height - 50))

    if config.draw_groups:
        draw_groups(surface, w)

    # draw each bird
    for bird in w.birds:
        draw_bird(surface, bird)

    for t in w.targets:
        draw_target(surface, t)

    if chart:
        charter.draw(data_screen)

    # finished drawing
    pygame.display.flip()

def draw_bird(surface, bird):
    img = fixed_wing_img
    # if not type(bird) == Bird:
    #     img = bad_img
    if bird.marked:
        pygame.draw.circle(surface, (255, 0, 0), (int(bird.p.x), int(bird.p.y)), 20, 1)
    if type(bird) != Bird:
        img = bad_img

    surface.blit(pygame.transform.rotate(img, bird.v.angle_to((0, -1))), (int(bird.p.x) - 10, int(bird.p.y) - 10))


def get_dt(count, total, avg_fr, t):
    new_t = pygame.time.get_ticks()
    dt = new_t - t
    t = new_t

    total += dt
    count += 1
    if count == 5:
        avg_fr = total/count
        count = 0
        total = 0
    return dt, count, total, avg_fr, t

# necessary to keep the application running in a thread (I think)
if __name__ == '__main__':
    main()
