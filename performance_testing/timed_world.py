import time
from world import World

class TimedWorld(World):


    def update(self, dt):
        t_start = time.thread_time_ns()

        self.calculate_distances()

        t_distances = time.thread_time_ns() - t_start

        update_neighbor_t = 0
        update_measurements_t = 0

        current_t = time.thread_time_ns()

        for bird in self.birds:
            bird.update_neighbours(self)
            new_t = time.thread_time_ns()
            update_neighbor_t += new_t - current_t

            current_t = new_t

            bird.update_measurements(self)
            new_t = time.thread_time_ns()
            update_measurements_t += new_t - current_t
            current_t = new_t

            bird.old_v = bird.v

        t_update_birds = time.thread_time_ns() - t_start - t_distances

        for bird in self.birds:
            bird.v = bird.calculate_v(self)

        t_update_vs = time.thread_time_ns() - t_start - t_distances-t_update_birds

        for bird in self.birds:
            bird.update_p(dt)
        t_update_ps = time.thread_time_ns() - t_start - t_distances - t_update_birds - t_update_vs

        return [t_distances, t_update_birds, t_update_vs, t_update_ps, update_neighbor_t, update_measurements_t]

