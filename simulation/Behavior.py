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
        total = 0
        steering = Vector()
        
        if position.x >= self.width - 50:
            if velocity.x >= 0:
                vel = SubVectorsX(steering, velocity)
                steering.add(vel)
                total += 1
        elif position.x <= 50:
            if velocity.x <= 0:
                vel = SubVectorsX(steering, velocity)
                steering.add(vel)
                total += 1

        if position.y >= self.height - 50:
            if velocity.y >= 0:
                vel = SubVectorsY(steering, velocity)
                steering.add(vel)
                total += 1
        elif position.y <= 50:
            if velocity.y <= 0:
                vel = SubVectorsY(steering, velocity)
                steering.add(vel)
                total += 1

        if total > 0:
            steering.normalize()
            steering = steering * self.max_speed
            steering = steering - velocity
            steering.limit(self.max_length)

        return steering

    def avoid_obstacle(self, position, velocity, obstacle_position):
        steering = Vector()
        center = Vector(obstacle_position[0], obstacle_position[1])
        dist = getDistance(center, position)

        if dist <= self.outer and dist > self.obstacle:
            temp = SubVectors(position, center)
            steering.add(temp)

        steering.normalize()
        steering = steering * self.max_speed
        steering = steering - velocity
        steering.limit(self.max_length)

        return steering

    def target_force(self, position, velocity):
        total = 0
        steering = Vector()

        dist = getDistance(self.target, position)
        if dist != 0:
            orient = SubVectors(self.target, position)
            steering.add(orient)
            total += 1

        if total > 0:
            steering.normalize()
            steering = steering * self.max_speed
            steering = steering - velocity
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