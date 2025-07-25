import pygame
import math

# Initialize pygame
pygame.init()

# Screen Settings
WIDTH, HEIGHT = 800, 600
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sensor-Based Car Simulation")

# Load and scale car image
car_image = pygame.image.load("car.jpg")
car_image = pygame.transform.scale(car_image, (40, 20))

# Create track
track = pygame.Surface((WIDTH, HEIGHT))
track.fill(BLACK)
pygame.draw.rect(track, GRAY, (100, 100, 600, 400))  # Outer boundary
pygame.draw.rect(track, BLACK, (200, 200, 400, 200))  # Inner hole

class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 2
        self.sensors = []
        self.sensor_points = []

    def draw(self):
        rotated_car = pygame.transform.rotate(car_image, -self.angle)
        rect = rotated_car.get_rect(center=(self.x, self.y))
        screen.blit(rotated_car, rect.topleft)

        # Draw sensors
        for p in self.sensor_points:
            pygame.draw.line(screen, RED, (self.x, self.y), p, 1)
            pygame.draw.circle(screen, RED, (int(p[0]), int(p[1])), 2)

    def move(self):
        rad = math.radians(self.angle)
        self.x += self.speed * math.cos(rad)
        self.y += self.speed * math.sin(rad)

    def detect_sensors(self):
        self.sensors = []
        self.sensor_points = []
        angles = [-60, -30, 0, 30, 60]
        for a in angles:
            sensor_x, sensor_y = self.x, self.y
            for _ in range(60):
                sensor_x += math.cos(math.radians(self.angle + a))
                sensor_y += math.sin(math.radians(self.angle + a))
                if 0 <= int(sensor_x) < WIDTH and 0 <= int(sensor_y) < HEIGHT:
                    if track.get_at((int(sensor_x), int(sensor_y))) == BLACK:
                        break
                else:
                    break
            self.sensors.append(math.dist((self.x, self.y), (sensor_x, sensor_y)))
            self.sensor_points.append((sensor_x, sensor_y))

    def auto_drive(self):
        if len(self.sensors) < 5:
            return

        left_far, left_near, front, right_near, right_far = self.sensors

        # If all sensors are very short, spin
        if all(s < 10 for s in self.sensors):
            self.angle += 10
            self.speed = 1
            return

        # If front is blocked, turn to side with more space
        if front < 25:
            self.speed = 1
            if left_far > right_far:
                self.angle += 6
            else:
                self.angle -= 6
        else:
            # Smooth steer based on side balance
            balance = (right_near + right_far) - (left_near + left_far)
            self.angle += balance * 0.03
            self.speed = 2

# Create the car
car = Car(150, 150)

# Main loop
running = True
while running:
    screen.fill(BLACK)
    screen.blit(track, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    car.detect_sensors()
    car.auto_drive()
    car.move()
    car.draw()

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
