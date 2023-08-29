import pygame
import sys
import random
import os

# Inicializace Pygame
pygame.init()

# Nastavení obrazovky
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Hra s animací")

assets_path = "./assets/"


def load_asset(asset_path):
    path = os.path.join(assets_path, asset_path)
    return pygame.image.load(path)


# Třída hráče
class Player:
    def __init__(self):
        self.x = 400
        self.y = 550
        self.width = 64
        self.height = 64
        self.speed = 2
        self.image_index = 0
        self.images_run = [
            load_asset(f"run/Run{i}.png") for i in range(1, 9)
        ]
        self.images_run_left = [
            load_asset(f"run/Run{i}L.png") for i in range(1, 9)
        ]
        self.image_idle = pygame.transform.scale(load_asset("run/Idle.png"), (self.width, self.height))
        self.image = self.image_idle
        self.animation_counter = 0
        self.facing_right = True

    def move_left(self):
        self.facing_right = False

        if self.x + self.width <= 0:
            self.x = screen.get_width()
        else:
            self.x -= self.speed

        self.animate_run()

    def move_right(self):
        self.facing_right = True

        if self.x - self.width >= screen.get_width():
            self.x = 0
        else:
            self.x += self.speed

        self.animate_run()

    def move_up(self):
        if self.y + self.height <= 0:
            self.y = screen.get_height()
        else:
            self.y -= self.speed

        self.animate_run()

    def move_down(self):
        if self.y - self.height >= screen.get_height():
            self.y = 0
        else:
            self.y += self.speed

        self.animate_run()

    def animate_run(self):
        if self.facing_right and self.speed != 0:
            self.animation_counter += 1
            if self.animation_counter > 2:
                self.animation_counter = 0
                self.image_index = (self.image_index + 1) % len(self.images_run)
                self.image = self.images_run[self.image_index]
        elif not self.facing_right and self.speed != 0:
            self.animation_counter += 1
            if self.animation_counter > 2:
                self.animation_counter = 0
                self.image_index = (self.image_index + 1) % len(self.images_run_left)
                self.image = self.images_run_left[self.image_index]

    def shoot(self):
        return Bullet(self.x + self.width // 2, self.y)

    def remove(self):
        self.x = screen.get_width() / 2
        self.y = screen.get_height() / 2


# Třída střely
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 3
        self.speed = 30

    def move(self):
        self.y -= self.speed

    def check_collision(self, enemy):
        distance = ((self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2) ** 0.5
        if distance < self.radius + enemy.width / 2:
            return True
        return False


# Třída nepřítele
class Enemy:
    def __init__(self, x):
        self.x = x
        self.y = 0
        self.width = 64
        self.height = 64
        self.speed = 1  # Zpomalil jsem rychlost nepřítele
        self.image_index = 0
        self.images_walk = [
            load_asset(f"zwalk/Walk{i}.png") for i in range(1, 7)
        ]
        self.image = self.images_walk[self.image_index]
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.animation_counter = 0

    def move(self):
        self.y += self.speed
        self.animate_walk()

    def animate_walk(self):
        self.animation_counter += 1
        if self.animation_counter > 5:
            self.animation_counter = 0
            self.image_index = (self.image_index + 1) % len(self.images_walk)
            self.image = self.images_walk[self.image_index]


# Hlavní smyčka hry
def main():
    clock = pygame.time.Clock()
    player = Player()
    bullets = []
    enemies = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append(player.shoot())

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.move_left()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.move_right()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player.move_up()
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player.move_down()

        screen.fill((155, 155, 155))

        for bullet in bullets:
            bullet.move()
            pygame.draw.circle(screen, (0, 0, 0), (bullet.x, bullet.y), bullet.radius)

            # Detekce kolize střely s nepřáteli
            for enemy in enemies:
                if bullet.check_collision(enemy):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    break  # Pokud nastane kolize, nemusíme kontrolovat další nepřátele

        for enemy in enemies:
            enemy.move()
            screen.blit(enemy.image, (enemy.x, enemy.y))

        if random.randint(0, 100) < 2:
            enemies.append(Enemy(random.randint(0, 800)))

        screen.blit(player.image, (player.x, player.y))
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
