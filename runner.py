import pygame

from sim_config import Config

from world import World
import world_configs
from bird import Bird
import faulty_bird
from data_analyzer import DataAnalyzer

from pygame.locals import (
    K_s,
    K_r,
    KEYDOWN,
    QUIT,
    K_SPACE,
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
)

width = 1200
height = 700
data_height = 200

bird_count = 50

w = world_configs.HourGlass(width, height, bird_count)
w.birds.append(faulty_bird.NonFlocker(200, 1000, bird_count))
# w.birds.append(faulty_bird.NonFlocker(500, 100, 51))

# for i in range(0, 5):
#     interval = 50 * 50.0 / 3
    # w.birds.append(faulty_bird.NonFlocker(200 + (i % 2), 100 + (interval * i), len(w.birds)))
    # w.birds.append(faulty_bird.FaultyBird(200 + (i % 2), 100 + (interval * i), len(w.birds), 1000, 1))

screen = pygame.display.set_mode((width, height+data_height))
data_screen = screen.subsurface(pygame.Rect(0, height, width, data_height))

charter = DataAnalyzer(width, data_height, 100, [5, 40])

pygame.init()
fixed_wing_img = pygame.transform.scale(pygame.image.load('fixed_wing.png'), (20, 20))
bad_img = pygame.transform.scale(pygame.image.load('bad.png'), (20, 20))
target_img = pygame.transform.scale(pygame.image.load('flag.png'), (20, 20))

font = pygame.font.SysFont(None, 72)



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

        # ignore frames that are too 'long'
        # if not, birds may suddenly 'skip' long distances
        if dt > 50:
            print('whoops. That frame took ' + str(dt) + ' ms')
            continue

        # the exit event is needed to stop this while loop
        # all other events are handled in handle_event() for cleaner code
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            else:
                handle_event(event, w, config)

        # make world update itself one time-step
        w.update(dt)

        charter.track(w)

        # draw new frame
        draw(screen, w, avg_fr, config)


def set_target(m_pos, w):
    w.targets.append(pygame.Vector2(int(m_pos[0]), int(m_pos[1])))


def draw_groups(screen, world):
    for bird in world.birds:
        for n in bird.neighbours:
            neighbor = world.birds[n]
            difference = neighbor.v - bird.v
            difference = difference.length()
            # print(difference)
            # intensity = (difference/max_difference_length_squared)

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

    charter.draw(data_screen)

    # finished drawing
    pygame.display.flip()

def draw_bird(surface, bird):
    img = fixed_wing_img
    if not type(bird) == Bird:
        img = bad_img
    surface.blit(pygame.transform.rotate(img, bird.v.angle_to((0, -1))),
                     (int(bird.p.x) - 10, int(bird.p.y) - 10))


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
