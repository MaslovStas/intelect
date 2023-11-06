import pygame

from swarm.pso import Swarm
from swarm.utils import get_odds_for_linear_function

pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
running = True

swarm = Swarm(inertia=0.4,
              cognitive_const=0.5,
              social_const=0.5,
              number_of_particles=15,
              number_of_iterations=50,
              value_limit=(-5, 5))

a, b = get_odds_for_linear_function(*swarm.value_limit, 0, 255)

MIN = (3, 2), (-2.8, 3.13), (-3.78, -3.28), (3.58, -1.85)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for x, y in MIN:
        pygame.draw.circle(screen, 'yellow', (a * x + b, a * y + b), 5)

    for particle in swarm:
        x, y = particle.location.x, particle.location.y
        pygame.draw.circle(screen, 'purple', (a * x + b, a * y + b), 2)

    pygame.display.flip()
    screen.fill('black')
    clock.tick(2)

    swarm.move()

pygame.quit()
