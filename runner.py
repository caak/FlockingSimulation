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
    K_a,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    KEYDOWN,
    QUIT,
    K_SPACE,
    MOUSEBUTTONDOWN,
)

width = 1200
height = 1000
data_height = 200

good_count = 50
bad_count = 10
bird_count = good_count + bad_count

chart = True

# w = layouts.HourGlass(width, height, good_count, bad_count, p_std=2.0, v_std=0.02, intruder_type=intruder.NonFlocker)
w = layouts.HourGlass(width, height, good_count, bad_count, 1.0, 0.01, intruder.NonFlocker, y_max_distance=1000+(200*9))
# w = layouts.Formation(width, height, 100)
# w = layouts.EmptyWorld(width, height, 0)

w.positions = [pygame.Vector2(0,0)]*bird_count
w.equilibrium = [0.0]*100

screen = pygame.display.set_mode((width, height+data_height))
data_screen = screen.subsurface(pygame.Rect(0, height, width, data_height))


charter = Tracer(width, 200, 100, good_count, bad_count)

pygame.init()
bird_width = 40
fixed_wing_img = pygame.transform.scale(pygame.image.load('images/fixed_wing.png'), (bird_width, bird_width))
bad_img = pygame.transform.scale(pygame.image.load('images/bad.png'), (bird_width, bird_width))
target_img = pygame.transform.scale(pygame.image.load('images/flag.png'), (20, 20))

font = pygame.font.SysFont(None, 72)


def main():
    iteration_count = 0
    running = True
    t = 0
    config = Config()
    avg_fr = 0
    count = 0
    total = 0

    predicted_d = Bird.avoid_range-(Bird.attraction_weight / (Bird.avoidance_weight * Bird.neighborhood_size))
    bird_count = len(w.birds)
    config.target = pygame.Vector2(0.0, -1.0)
    config.camera_offset = pygame.Vector2(600, 600)

    w.target = config.target
    w.update(1)

    while running:
        bird_count = len(w.birds)

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

        handle_inputs(config)

        # make world update itself one time-step
        if not config.pause:
            w.target = config.target

            w.update(1)
            # w.update(0.5)

            config.iteration_count += 1
            distances = np.sort(w.distances, axis=0)
            if len(w.birds) > 1:
                print(
                    np.sum(distances[:][1:Bird.neighborhood_size+1])/(len(w.birds)*Bird.neighborhood_size),    # avg distance between neighbors
                    predicted_d,                                                        # predicted distance between neighbors
                    Bird.alignment_sum / bird_count,                                    # avg alignment force
                    Bird.attraction_sum/bird_count,                                     # avg attraction force
                    Bird.avoidance_sum/bird_count,                                      # avg avoidance force
                    Bird.target_sum/bird_count                                          # avg target force
                )
            Bird.equilibrium = 0.0
        config.flock_center = pygame.Vector2(0.0,0.0)
        for p in w.positions:
            config.flock_center += p
        if len(w.birds) > 0:
            config.flock_center /= len(w.birds)
            config.avg_velocity = (w.v_sum/len(w.birds))/Bird.max_speed
            # print(config.avg_velocity)
        config.camera = config.flock_center - config.camera_offset

        # print(config.camera.y)
        # print(Bird.attraction_sum, Bird.alignment_sum, Bird.avoidance_sum, Bird.target_sum)
        Bird.reset_force_sums()
        if chart and not config.pause:
            charter.track(w)

        # draw new frame
        draw(screen, w, avg_fr, config)
        iteration_count += 1
        # print(iteration_count)



def set_target(m_pos, w):
    w.targets.append(pygame.Vector2(int(m_pos[0]), int(m_pos[1])))


def draw_groups(screen, world, config):
    for bird in world.birds:
        if type(bird) != Bird:
            continue
        for n in bird.neighbours:
            neighbor = world.birds[n]

            distance = (neighbor.p - bird.p)
            b_p = pygame.Vector2(bird.p.x, bird.p.y)
            # if int(bird.p.x /width) == int(neighbor.p.x /width) and int(bird.p.y / height) == int(neighbor.p.y / height):
            n_p = b_p+distance
            # else:
            #     n_p = neighbor.p

            edge_color = 0
            pygame.draw.line(screen, (edge_color, edge_color, edge_color), b_p-config.camera, n_p-config.camera, int(1))

def handle_inputs(config):
    if pygame.mouse.get_pressed()[0]:
        compass_dir = (pygame.mouse.get_pos() - config.compass_pos)
        if compass_dir.length() < config.compass_radius:
            config.target = (compass_dir / config.compass_radius) * Bird.max_speed
    camera_speed = 5
    if pygame.key.get_pressed()[K_UP]:
        config.camera_offset.y += camera_speed
    if pygame.key.get_pressed()[K_DOWN]:
        config.camera_offset.y -= camera_speed
    if pygame.key.get_pressed()[K_LEFT]:
        config.camera_offset.x += camera_speed
    if pygame.key.get_pressed()[K_RIGHT]:
        config.camera_offset.x -= camera_speed


def handle_event(e, w, c):
    m_pos = pygame.mouse.get_pos()
    w_pos = m_pos + c.camera
    if e.type == MOUSEBUTTONDOWN:
        if e.button == 1:
            compass_dir = (m_pos - c.compass_pos)
            if compass_dir.length() > c.compass_radius:
                w.addBird(Bird(w_pos.x, w_pos.y, 0))

            # set_target(m_pos+c.camera, w)
    elif e.type == KEYDOWN:
        if e.key == K_s:
            c.draw_groups = not c.draw_groups
        elif e.key == K_SPACE:
            c.pause = not c.pause
        elif e.key == K_a:
            intruder.createAttackFormation(w, c.camera+pygame.Vector2(width/2, height), c)
            # if charter.TP + charter.FN > 0:
            #     P = charter.TP + charter.FN
            #     N = charter.TN + charter.FP
            #     print(c.iteration_count, charter.TP / P, charter.FP / N, charter.TP, charter.FP, charter.TN, charter.FN)
        # elif e.key == K_t:
        #     charter.reset_confusion_matrix()


def draw_target(surface, t, config):
    pos = (int(t[0] - config.camera.x), int(t[1] - config.camera.y))
    surface.blit(target_img, (pos[0]-10, pos[1]-10))
    pygame.draw.circle(surface, (0, 0, 0), pos, int(World.target_range), 1)

#draws a background to show the movement of birds
def draw_background(surface, config):
    linewidth = 400
    lineheight = 400

    start_pos = -pygame.Vector2(config.camera)
    start_pos.x = 0
    end_pos = -pygame.Vector2(config.camera)
    end_pos.x = surface.get_width()

    # start_pos.x = (start_pos.x % (surface.get_width()*2)) - surface.get_width()
    # end_pos.x = start_pos.x + surface.get_width()*2
    for i in range(0, 10):
        start_pos.y = start_pos.y % surface.get_height()
        end_pos.y = end_pos.y % surface.get_height()

        #multicolor: (255*((i % 3)==0), 255*(((i+1) % 3)==0), 255*(((i+2) % 3)==0))
        pygame.draw.line(surface, (0, 0, 0), start_pos, end_pos, 1)
        start_pos.y += lineheight
        end_pos.y += lineheight

    start_pos.x = -config.camera.x
    start_pos.y = 0
    end_pos = -pygame.Vector2(config.camera)
    end_pos.y = surface.get_height()

    # start_pos.y = ((start_pos.y - surface.get_height())% (surface.get_height()*2))
    # end_pos.y = start_pos.y + surface.get_height()*2
    for i in range(0, 10):
        start_pos.x = start_pos.x % surface.get_width()
        end_pos.x = end_pos.x % surface.get_width()

        pygame.draw.line(surface, (0, 0, 0), start_pos, end_pos, 1)
        start_pos.x += linewidth
        end_pos.x += linewidth


# this function outlines the task of drawing
def draw(surface, w, dt, config):
    # fill the screen with white
    # surface.fill((25, 150, 25))
    surface.fill((255, 255, 255))

    draw_background(surface, config)

    delta_text = font.render(str(dt), True, (0, 0, 0))
    surface.blit(delta_text, (10, w.height - 50))

    if config.draw_groups:
        draw_groups(surface, w, config)

    # draw each bird
    for bird in w.birds:
        draw_bird(surface, bird, config)

    for t in w.targets:
        draw_target(surface, t, config)

    drawCompass(surface, config)
    if chart:
        charter.draw(data_screen)

    # finished drawing
    pygame.display.flip()

def draw_bird(surface, bird, config):
    img = fixed_wing_img
    # if not type(bird) == Bird:
    #     img = bad_img
    # if bird.marked:
    #     pygame.draw.circle(surface, (255, 0, 0), (int(bird.p.x - config.camera.x), int(bird.p.y - config.camera.y)), 20, 1)
    if type(bird) != Bird:
        img = bad_img

    # surface.blit(pygame.transform.rotate(img, bird.v.angle_to((0, -1))), (int(bird.p.x%width) - 10, int(bird.p.y%height) - 10))
    surface.blit(pygame.transform.rotate(img, bird.v.angle_to((0, -1))), (int(bird.p.x - config.camera.x) - bird_width/2, int(bird.p.y - config.camera.y) - bird_width/2))


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

def drawCompass(surface, config):
    radius = config.compass_radius
    center = config.compass_pos
    vel = center + (config.avg_velocity*radius)
    target = center + (config.target/Bird.max_speed*radius)
    pygame.draw.circle(surface, (0, 0, 0), center, radius, 2)
    pygame.draw.line(surface, (0, 0, 0), center, vel, 2)
    pygame.draw.line(surface, (0, 0, 0), center, target, 1)

# necessary to keep the application running in a thread (I think)
if __name__ == '__main__':
    main()
