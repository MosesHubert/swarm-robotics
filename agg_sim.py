import pygame
from tools import *
from matrix import *
from random import uniform

class Simulator:
    def __init__(self):
        self.position = Vector()
        self.velocity = Vector()
        self.acceleration = Vector()
        self.angle = 0

        self.color1 = (255, 255, 255)
        self.color2 = (  0,   0,   0)
        self.color3 = (255,   0,   0)
        self.color4 = (  0, 255,   0)
        self.stroke = 5

        self.max_speed = 1
        self.max_length = 1

        self.size = 20
        self.lowlim = 40
        self.uplim = 60

        self.values = {"separation" : 0.05,
                       "alignment"  : 0.05,
                       "cohesion"   : 0.05,
                       "separation_alignment" : 0.05,
                       "separation_cohesion"  : 0.05,
                       "alignment_cohesion"   : 0.05,
                       "separation_alignment_cohesion" : 0.05}

        self.state = 0
        self.new_state = 0
        self.reward = 0
        self.action = 0

        self.learning_rate = 0.5
        self.discount = 0.8
        self.epsilon = 0.1

        self.actions = ['separation', 
                        'alignment', 
                        'cohesion',
                        'separation_alignment',
                        'separation_cohesion',
                        'alignment_cohesion',
                        'separation_alignment, cohesion']
        self.iter = 0
    
    def start(self, x, y):
        self.position = Vector(x, y)

        vec_x = uniform(-1, 1)
        vec_y = uniform(-1, 1)
        self.velocity = Vector(vec_x, vec_y)
        self.velocity.normalize()
        self.velocity = self.velocity * uniform(1, 3)

        self.iter = 1

    def limits(self, width, height):
        total = 0
        steering = Vector()
        
        if self.position.x >= width - 50:
            if self.velocity.x >= 0:
                vel = SubVectorsX(steering, self.velocity)
                steering.add(vel)
                total += 1
        elif self.position.x <= 50:
            if self.velocity.x <= 0:
                vel = SubVectorsX(steering, self.velocity)
                steering.add(vel)
                total += 1

        if self.position.y >= height - 50:
            if self.velocity.y >= 0:
                vel = SubVectorsY(steering, self.velocity)
                steering.add(vel)
                total += 1
        elif self.position.y <= 50:
            if self.velocity.y <= 0:
                vel = SubVectorsY(steering, self.velocity)
                steering.add(vel)
                total += 1

        if total > 0:
            steering = steering
            steering.normalize()
            steering = steering * self.max_speed
            steering = steering - self.velocity.Normalize()
            steering.limit(self.max_length)
        return steering

    def separation(self, flockMates):
        total = 0
        steering = Vector()

        for mate in flockMates:
            dist = getDistance(self.position, mate.position)
            if mate is not self:
                temp = SubVectors(self.position, mate.position)
                temp = temp / (dist ** 2)
                steering.add(temp)
                total += 1

        if total > 0:
            steering = steering / total
            steering.normalize()
            steering = steering * self.max_speed
            steering = steering - self.velocity.Normalize()
            steering.limit(self.max_length)
        
        return steering

    def alignment(self, flockMates):
        total = 0
        steering = Vector()
        
        for mate in flockMates:
            dist = getDistance(self.position, mate.position)
            if mate is not self:
                vel = mate.velocity.Normalize()
                vel = vel / (dist ** 2)
                steering.add(vel)
                total += 1

        if total > 0:
            steering = steering / total
            steering.normalize()
            steering = steering * self.max_speed
            steering = steering - self.velocity.Normalize()
            steering.limit(self.max_length)

        return steering

    def cohesion(self, flockMates):
        total = 0
        steering = Vector()
        min_dist = 1000

        for mate in flockMates:
            dist = getDistance(self.position, mate.position)
            if mate is not self:
                if dist < min_dist:
                    min_dist = dist
                    coh = mate.position
                    total += 1
        
        steering.add(coh)

        if total > 0:
            steering = steering - self.position
            steering.normalize()
            steering = steering * self.max_speed
            steering = steering - self.velocity.Normalize()
            steering.limit(self.max_length)

        return steering

    def separation_alignment(self, flockMates):
        total = 0
        steering = Vector()

        for mate in flockMates:
            dist = getDistance(self.position, mate.position)
            if mate is not self:
                temp = SubVectors(self.position, mate.position)
                temp = temp / (dist ** 2)
                vel = mate.velocity.Normalize()
                vel = vel / (dist ** 2)
                steering.add(temp)
                steering.add(vel)
                total += 1

        if total > 0:
            steering = steering / total
            steering.normalize()
            steering = steering * self.max_speed
            steering = steering - self.velocity.Normalize()
            steering.limit(self.max_length)
        
        return steering

    def separation_cohesion(self, flockMates):
        total = 0
        steering = Vector()
        min_dist = 1000

        for mate in flockMates:
            dist = getDistance(self.position, mate.position)
            if mate is not self:
                if dist < min_dist:
                    min_dist = dist
                    coh = mate.position
                temp = SubVectors(self.position, mate.position)
                temp = temp / (dist ** 2)
                steering.add(temp)
                total += 1

        steering.add(coh)

        if total > 0:
            steering = steering / total
            steering = steering - self.position
            steering.normalize()
            steering = steering * self.max_speed
            steering = steering - self.velocity.Normalize()
            steering.limit(self.max_length)

        return steering

    def alignment_cohesion(self, flockMates):
        total = 0
        steering = Vector()
        min_dist = 1000

        for mate in flockMates:
            dist = getDistance(self.position, mate.position)
            if mate is not self:
                if dist < min_dist:
                    min_dist = dist
                    coh = mate.position
                vel = mate.velocity.Normalize()
                vel = vel / (dist ** 2)
                steering.add(vel)
                total += 1

        steering.add(coh)

        if total > 0:
            steering = steering / total
            steering = steering - self.position
            steering.normalize()
            steering = steering * self.max_speed
            steering = steering - self.velocity.Normalize()
            steering.limit(self.max_length)

        return steering

    def separation_alignment_cohesion(self, flockMates):
        total = 0
        steering = Vector()
        min_dist = 1000

        for mate in flockMates:
            dist = getDistance(self.position, mate.position)
            if mate is not self:
                if dist < min_dist:
                    min_dist = dist
                    coh = mate.position
                vel = mate.velocity.Normalize()
                vel = vel / (dist ** 2)
                temp = SubVectors(self.position, mate.position)
                temp = temp / (dist ** 2)
                steering.add(temp)
                steering.add(vel)
                total += 1

        steering.add(coh)

        if total > 0:
            steering = steering / total
            steering = steering - self.position
            steering.normalize()
            steering = steering * self.max_speed
            steering = steering - self.velocity.Normalize()
            steering.limit(self.max_length)

        return steering

    def behaviour(self, width, height):
        self.acceleration.reset()

        wander = self.limits(width, height)
        wander = wander * 3
        self.acceleration.add(wander)

    def update(self):
        self.position += self.velocity
        self.velocity += self.acceleration
        self.velocity.limit(self.max_speed)
        self.angle = self.velocity.heading() + np.pi/2
        print(self.acceleration)
    
    def Draw(self, screen, distance=5, scale=2):
        ps = []
        points = [None for _ in range(3)]
        
        points[0] = [[0],[-self.size],[0]]
        points[1] = [[self.size//2],[self.size//2],[0]]
        points[2] = [[-self.size//2],[self.size//2],[0]]
        
        for point in points:
            rotated = matrix_multiplication(rotationZ(self.angle) , point)
            z = 1/(distance - rotated[2][0])
            
            projection_matrix = [[z, 0, 0], [0, z, 0]]
            projected_2d = matrix_multiplication(projection_matrix, rotated)
            
            x = int(projected_2d[0][0] * scale) + self.position.x
            y = int(projected_2d[1][0] * scale) + self.position.y
            ps.append((x, y))
        
        pygame.draw.circle(screen, self.color4, (self.position.x, self.position.y), self.uplim, width=1)
        pygame.draw.circle(screen, self.color3, (self.position.x, self.position.y), self.lowlim, width=1)
        pygame.draw.circle(screen, self.color1, (self.position.x, self.position.y), self.size)
        pygame.draw.polygon(screen, self.color2, ps, self.stroke)

    def alone(self, flockMates):
        total = 0
        
        for mate in flockMates:
            dist = getDistance(self.position, mate.position)
            if mate is not self and dist > self.uplim:
                total += 1
        
        if total == len(flockMates)-1:
            self.state = 0
    
    def next_alone(self, flockMates):
        total = 0
        
        for mate in flockMates:
            dist = getDistance(self.position, mate.position)
            if mate is not self and dist > self.uplim:
                total += 1
        
        if total == len(flockMates)-1:
            self.new_state = 0
            self.reward = 0
    
    def nearby(self, flockMates):
        total = 0

        for mate in flockMates:
            dist = getDistance(self.position, mate.position)
            if mate is not self:
                if dist >= self.lowlim and dist <= self.uplim:
                    total += 1

        if total > 0:
            self.state = 1
    
    def next_nearby(self, flockMates):
        total = 0

        for mate in flockMates:
            dist = getDistance(self.position, mate.position)
            if mate is not self:
                if dist >= self.lowlim and dist <= self.uplim:
                    total += 1

        if total > 0:
            self.new_state = 1
            self.reward = 1

    def lost(self, width, height):
        total = 0

        if self.position.x >= width or self.position.x <= 0:
            total += 1
        if self.position.y >= height or self.position.y <= 0:
            total += 1

        if total > 0:
            self.state = 2

    def next_lost(self, width, height):
        total = 0

        if self.position.x >= width or self.position.x <= 0:
            total += 1
        if self.position.y >= height or self.position.y <= 0:
            total += 1

        if total > 0:
            self.new_state = 2
            self.reward = -1
    
    def crash(self, flockMates):
        total = 0

        for mate in flockMates:
            dist = getDistance(self.position, mate.position)
            if mate is not self and dist <= 2 * self.size:
                total += 1

        if total > 0:
            self.state = 3

    def next_crash(self, flockMates):
        total = 0

        for mate in flockMates:
            dist = getDistance(self.position, mate.position)
            if mate is not self and dist <= 2 * self.size:
                total += 1

        if total > 0:
            self.new_state = 3
            self.reward = -1

    def close(self, flockMates):
        total = 0

        for mate in flockMates:
            dist = getDistance(self.position, mate.position)
            if mate is not self:
                if dist > 2 * self.size and dist < self.lowlim:
                    total += 1
        
        if total > 0:
            self.state = 4

    def next_close(self, flockMates):
        total = 0

        for mate in flockMates:
            dist = getDistance(self.position, mate.position)
            if mate is not self:
                if dist > 2 * self.size and dist < self.lowlim:
                    total += 1
        
        if total > 0:
            self.new_state = 4
            self.reward = 0

    def create_Q(self, n_state=5):
        self.Q_values = []
        for i in range(0, n_state * 7, 7):
            row = []
            for j in range(i, i + 7, 1):
                row.append(float(uniform(-2,2)))
            self.Q_values.append(row)
        self.Q_values = np.array(self.Q_values,dtype=float).reshape(n_state, 7)

    def current_state(self, flock, width, height):
        self.alone(flock)
        self.nearby(flock)
        self.lost(width, height)
        self.crash(flock)
        self.close(flock)

    def next_state(self, flock, width, height):
        self.next_alone(flock)
        self.next_nearby(flock)
        self.next_lost(width, height)
        self.next_crash(flock)
        self.close(flock)

    def get_next_action(self):
        if np.random.random() > self.epsilon:
            self.action = np.argmax(self.Q_values[self.state])
        else:
            self.action = np.random.randint(7)

    def update_action(self, flock):
        if self.actions[self.action] == 'separation' and self.state == 0:
            avoid = self.separation(flock)
            avoid = avoid * self.values["separation"]
            self.acceleration.add(avoid)
        elif self.actions[self.action] == 'separation' and self.state == 1:
            avoid = self.separation(flock)
            avoid = avoid * self.values["separation"]
            self.acceleration.add(avoid)
        elif self.actions[self.action] == 'separation' and self.state == 2:
            avoid = self.separation(flock)
            avoid = avoid * self.values["separation"]
            self.acceleration.add(avoid)
        elif self.actions[self.action] == 'separation' and self.state == 3:
            avoid = self.separation(flock)
            avoid = avoid * self.values["separation"]
            self.acceleration.add(avoid)
        elif self.actions[self.action] == 'separation' and self.state == 4:
            avoid = self.separation(flock)
            avoid = avoid * self.values["separation"]
            self.acceleration.add(avoid)
        elif self.actions[self.action] == 'alignment' and self.state == 0:
            align = self.alignment(flock)
            align = align * self.values["alignment"]
            self.acceleration.add(align)
        elif self.actions[self.action] == 'alignment' and self.state == 1:
            align = self.alignment(flock)
            align = align * self.values["alignment"]
            self.acceleration.add(align)
        elif self.actions[self.action] == 'alignment' and self.state == 2:
            align = self.alignment(flock)
            align = align * self.values["alignment"]
            self.acceleration.add(align)
        elif self.actions[self.action] == 'alignment' and self.state == 3:
            align = self.alignment(flock)
            align = align * self.values["alignment"]
            self.acceleration.add(align)
        elif self.actions[self.action] == 'alignment' and self.state == 4:
            align = self.alignment(flock)
            align = align * self.values["alignment"]
            self.acceleration.add(align)     
        elif self.actions[self.action] == 'cohesion' and self.state == 0:
            gather = self.cohesion(flock)
            gather = gather * self.values["cohesion"]
            self.acceleration.add(gather)
        elif self.actions[self.action] == 'cohesion' and self.state == 1:
            gather = self.cohesion(flock)
            gather = gather * self.values["cohesion"]
            self.acceleration.add(gather)
        elif self.actions[self.action] == 'cohesion' and self.state == 2:
            gather = self.cohesion(flock)
            gather = gather * self.values["cohesion"]
            self.acceleration.add(gather)
        elif self.actions[self.action] == 'cohesion' and self.state == 3:
            gather = self.cohesion(flock)
            gather = gather * self.values["cohesion"]
            self.acceleration.add(gather)
        elif self.actions[self.action] == 'cohesion' and self.state == 4:
            gather = self.cohesion(flock)
            gather = gather * self.values["cohesion"]
            self.acceleration.add(gather)
        elif self.actions[self.action] == 'separation_alignment' and self.state == 0:
            sep_al = self.separation_alignment(flock)
            sep_al = sep_al * self.values["separation_alignment"]
            self.acceleration.add(sep_al)
        elif self.actions[self.action] == 'separation_alignment' and self.state == 1:
            sep_al = self.separation_alignment(flock)
            sep_al = sep_al * self.values["separation_alignment"]
            self.acceleration.add(sep_al)
        elif self.actions[self.action] == 'separation_alignment' and self.state == 2:
            sep_al = self.separation_alignment(flock)
            sep_al = sep_al * self.values["separation_alignment"]
            self.acceleration.add(sep_al)
        elif self.actions[self.action] == 'separation_alignment' and self.state == 3:
            sep_al = self.separation_alignment(flock)
            sep_al = sep_al * self.values["separation_alignment"]
            self.acceleration.add(sep_al)
        elif self.actions[self.action] == 'separation_alignment' and self.state == 4:
            sep_al = self.separation_alignment(flock)
            sep_al = sep_al * self.values["separation_alignment"]
            self.acceleration.add(sep_al)
        elif self.actions[self.action] == 'separation_cohesion' and self.state == 0:
            sep_coh = self.separation_cohesion(flock)
            sep_coh = sep_coh * self.values["separation_cohesion"]
            self.acceleration.add(sep_coh)
        elif self.actions[self.action] == 'separation_cohesion' and self.state == 1:
            sep_coh = self.separation_cohesion(flock)
            sep_coh = sep_coh * self.values["separation_cohesion"]
            self.acceleration.add(sep_coh)
        elif self.actions[self.action] == 'separation_cohesion' and self.state == 2:
            sep_coh = self.separation_cohesion(flock)
            sep_coh = sep_coh * self.values["separation_cohesion"]
            self.acceleration.add(sep_coh)
        elif self.actions[self.action] == 'separation_cohesion' and self.state == 3:
            sep_coh = self.separation_cohesion(flock)
            sep_coh = sep_coh * self.values["separation_cohesion"]
            self.acceleration.add(sep_coh)
        elif self.actions[self.action] == 'separation_cohesion' and self.state == 4:
            sep_coh = self.separation_cohesion(flock)
            sep_coh = sep_coh * self.values["separation_cohesion"]
            self.acceleration.add(sep_coh)
        elif self.actions[self.action] == 'alignment_cohesion' and self.state == 0:
            al_coh = self.alignment_cohesion(flock)
            al_coh = al_coh * self.values["alignment_cohesion"]
            self.acceleration.add(al_coh)
        elif self.actions[self.action] == 'alignment_cohesion' and self.state == 1:
            al_coh = self.alignment_cohesion(flock)
            al_coh = al_coh * self.values["alignment_cohesion"]
            self.acceleration.add(al_coh)
        elif self.actions[self.action] == 'alignment_cohesion' and self.state == 2:
            al_coh = self.alignment_cohesion(flock)
            al_coh = al_coh * self.values["alignment_cohesion"]
            self.acceleration.add(al_coh)
        elif self.actions[self.action] == 'alignment_cohesion' and self.state == 3:
            al_coh = self.alignment_cohesion(flock)
            al_coh = al_coh * self.values["alignment_cohesion"]
            self.acceleration.add(al_coh)
        elif self.actions[self.action] == 'alignment_cohesion' and self.state == 4:
            al_coh = self.alignment_cohesion(flock)
            al_coh = al_coh * self.values["alignment_cohesion"]
            self.acceleration.add(al_coh)
        elif self.actions[self.action] == 'separation_alignment_cohesion' and self.state == 0:
            sep_al_coh = self.separation_alignment_cohesion(flock)
            sep_al_coh = sep_al_coh * self.values["separation_alignment_cohesion"]
            self.acceleration.add(sep_al_coh)
        elif self.actions[self.action] == 'separation_alignment_cohesion' and self.state == 1:
            sep_al_coh = self.separation_alignment_cohesion(flock)
            sep_al_coh = sep_al_coh * self.values["separation_alignment_cohesion"]
            self.acceleration.add(sep_al_coh)
        elif self.actions[self.action] == 'separation_alignment_cohesion' and self.state == 2:
            sep_al_coh = self.separation_alignment_cohesion(flock)
            sep_al_coh = sep_al_coh * self.values["separation_alignment_cohesion"]
            self.acceleration.add(sep_al_coh)
        elif self.actions[self.action] == 'separation_alignment_cohesion' and self.state == 3:
            sep_al_coh = self.separation_alignment_cohesion(flock)
            sep_al_coh = sep_al_coh * self.values["separation_alignment_cohesion"]
            self.acceleration.add(sep_al_coh)
        elif self.actions[self.action] == 'separation_alignment_cohesion' and self.state == 4:
            sep_al_coh = self.separation_alignment_cohesion(flock)
            sep_al_coh = sep_al_coh * self.values["separation_alignment_cohesion"]
            self.acceleration.add(sep_al_coh)

    def is_terminal_state(self, flockMates):
        total = 0

        for mate in flockMates:
            dist = getDistance(self.position, mate.position)
            if mate is not self:
                if dist >= self.lowlim and dist <= self.uplim:
                    total += 1

        if total == 3:
            return 1
        else:
            return 0

    def is_state_change(self):
        if self.new_state != self.state:
            return True
        else:
            return False

    def update_Q(self):
        if self.new_state != self.state:
            old_q_value = self.Q_values[self.state][self.action]
            temporal_difference = self.reward + (self.discount * np.max(self.Q_values[self.new_state])) - old_q_value
            new_q_value = old_q_value + (self.learning_rate * temporal_difference)
            self.Q_values[self.state][self.action] = new_q_value
        else:
            self.Q_values = self.Q_values
        
        print('Iterasi ke-{}'.format(self.iter))
        self.iter += 1
        return self.Q_values

    def crashing(self, flockMates):
        for mate in flockMates:
            dist = getDistance(self.position, mate.position)
            if mate is not self and dist <= 2 * self.size:
                self.velocity = Vector()
                self.acceleration = Vector()