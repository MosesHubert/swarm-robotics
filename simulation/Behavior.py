from simulation.Vector import *

class Behavior:
    def __init__(self, target, width, height, max_speed, max_length, inner, outer, obstacle):
        self.target = target
        self.width = width
        self.height = height
        self.max_speed = max_speed
        self.max_length = max_length
        self.inner = inner
        self.outer = outer
        self.obstacle = obstacle

    def frame_boundaries(self, position, velocity):
        # total = 0
        steering = Vector()
        
        if position.x >= self.width - 50:
            if velocity.x >= 0:
                vn = SubVectorsX(steering, velocity)
                vn.normalize()
                steering.add(vn)
        elif position.x <= 50:
            if velocity.x <= 0:
                vn = SubVectorsX(steering, velocity)
                vn.normalize()
                steering.add(vn)

        if position.y >= self.height - 50:
            if velocity.y >= 0:
                vn = SubVectorsY(steering, velocity)
                vn.normalize()
                steering.add(vn)
        elif position.y <= 50:
            if velocity.y <= 0:
                vn = SubVectorsY(steering, velocity)
                vn.normalize()
                steering.add(vn)

        steering = steering * self.max_speed
        steering.limit(self.max_length)

        return steering

    def avoid_obstacle(self, position, velocity, obstacle_position):
        steering = Vector()
        center = Vector(obstacle_position[0], obstacle_position[1])
        dist = getDistance(center, position)

        if dist <= self.outer + self.obstacle and dist > self.obstacle:
            vn = SubVectors(position, center)
            vn.normalize
            vn = vn / dist
            steering.add(vn)

        steering = steering * self.max_speed
        steering.limit(self.max_length)

        return steering

    def target_force(self, position, velocity):
        steering = Vector()

        vn = SubVectors(self.target, position)
        steering.add(vn)

        steering = steering * self.max_speed
        steering.limit(self.max_length)

        return steering

    def update_behavior(self, position, velocity, obstacle_position, wander_magnitude, avoid_magnitude, target_magnitude):
        steering = Vector()

        wander = self.frame_boundaries(position, velocity)
        wander = wander * wander_magnitude
        steering.add(wander)

        avoid = self.avoid_obstacle(position, velocity, obstacle_position)
        avoid = avoid * avoid_magnitude
        steering.add(avoid)

        target = self.target_force(position, velocity)
        target = target * target_magnitude
        steering.add(target)

        return steering