import pygame
import random
import os
import helpers
import road


def draw_bg():
    helpers.screen.fill(helpers.BG)
    road.Road().draw()
    helpers.drawTextWithBg(f"SCORE: {player.score}", 20, 20)


def play_background_music():
    if player.alive and helpers.game_background_sound.get_num_channels() == 0:
        helpers.game_background_sound.play(-1)
        helpers.game_background_sound.set_volume(0.5)
        helpers.tuktuk_running_sound.play(-1)


class Car(pygame.sprite.Sprite):
    def __init__(self, char_type, x=0, y=0, scale=0.8, speed=5):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.speed = speed
        self.scale = scale
        self.lives = 1
        self.alive = True
        self.score = 0
        self.death_animation_list = []
        self.death_animation_frame_index = 1
        self.death_animation_repitition = 0
        self.update_time = pygame.time.get_ticks()
        self.isGoodDriver = random.choice([True, False])

        self.image = self.get_alive_image()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        num_of_frames = len(os.listdir(f"{helpers.IMAGES_DIR}/death"))
        for i in range(1, num_of_frames):
            img = pygame.image.load(
                f"{helpers.IMAGES_DIR}/death/exp{i}.png"
            ).convert_alpha()
            self.death_animation_list.append(img)

    def get_alive_image(self):
        img = pygame.image.load(
            f"{helpers.IMAGES_DIR}/{self.char_type}.png"
        ).convert_alpha()
        return helpers.get_scaled_image(img, self.scale)

    def draw(self):
        helpers.screen.blit(self.image, self.rect)

    def explode(self):
        if self.death_animation_repitition >= len(self.death_animation_list) * 3:
            self.kill()

            helpers.drawTextWithBg(
                "GAME OVER!",
                (helpers.SCREEN_CENTER - 150),
                (helpers.SCREEN_HEIGHT // 2) - 50,
                helpers.game_over_font,
                helpers.WHITE,
                helpers.BLACK,
            )
            helpers.drawTextWithBg(
                "Press any key to restart",
                (helpers.SCREEN_CENTER - 100),
                (helpers.SCREEN_HEIGHT - 50),
            )

            return

        ANIMATION_COOLDOWN = 100

        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.death_animation_frame_index += 1

        if self.death_animation_frame_index >= len(self.death_animation_list):
            self.death_animation_frame_index = 0

        self.image = self.death_animation_list[self.death_animation_frame_index]

        if self.death_animation_frame_index == len(self.death_animation_list) - 1:
            self.death_animation_repitition += 1

    def update(self):
        dx = 0
        dy = 0

        if self.char_type == "player":
            if not self.alive:
                self.explode()
                return

            # Player controls
            if helpers.moving_up and self.rect.y > 0:
                dy = self.speed * -1
            if (
                helpers.moving_down
                and self.rect.y < helpers.SCREEN_HEIGHT - self.image.get_height()
            ):
                dy = self.speed * 1
            if (
                helpers.moving_left
                and self.rect.x > (helpers.SCREEN_CENTER - self.image.get_width()) - 125
            ):
                dx = self.speed * -1
            if (
                helpers.moving_right
                and self.rect.x < (helpers.SCREEN_CENTER + self.image.get_width()) + 75
            ):
                dx = self.speed * 1

            if self.rect.y > helpers.SCREEN_HEIGHT:
                self.rect.y = 0
                self.rect.x = random.randint(
                    helpers.SCREEN_CENTER - 100, helpers.SCREEN_CENTER + 100
                )

            # Check collision with enemies
            self.check_collision()

        else:
            dy = self.speed * 1

            self.curse()

            if self.rect.y > helpers.SCREEN_HEIGHT:
                self.kill()
                player.addScore()

        self.rect.x += dx
        self.rect.y += dy

    def addScore(self, score=5):
        if not self.alive:
            return

        self.score += score

    def reset(self):
        self.image = self.get_alive_image()
        self.rect.y = helpers.SCREEN_HEIGHT - self.image.get_height()
        self.rect.x = helpers.SCREEN_CENTER
        self.alive = True
        self.death_animation_repitition = 0
        player.lives = 2
        player.score = 0
        play_background_music()
        helpers.enemy_group.empty()
        helpers.set_initial_values()

    def check_collision(self):
        if pygame.sprite.spritecollide(self, helpers.enemy_group, False):
            self.alive = False
            self.lives -= 1
            
            if helpers.game_over_sound.get_num_channels() == 0:
                helpers.tuktuk_running_sound.stop()
                helpers.game_background_sound.stop()
                helpers.game_over_sound.play()

    def curse(self):
        if self.isGoodDriver:
            return

        if not hasattr(self, "curseChoice"):
            self.curseChoice = random.choices(helpers.curses)[0]

        self.vision = pygame.Rect(0, 0, 150, self.rect.h)
        self.vision.center = (self.rect.x + 10, self.rect.y + 100)

        # draw vision to see the collision
        # pygame.draw.rect(screen, (255, 0, 0), self.vision)

        if self.vision.colliderect(player.rect):
            helpers.drawText(
                self.curseChoice, helpers.WHITE, self.rect.x, self.rect.y - 25
            )
            if helpers.car_horn_sound.get_num_channels() == 0:
                helpers.car_horn_sound.play()


def create_enemies():
    if player.score != 0 and player.score % 100 == 0:
        helpers.enemy_speed += 0.01
        helpers.enemy_cooldown_reducing_val += 0.01
        for enemy in helpers.enemy_group:
            enemy.speed += 0.01

    if helpers.enemy_cooldown <= 0:
        helpers.enemy_group.add(
            Car(
                "enemy-%s" % random.randint(0, 4),
                random.randint(
                    helpers.SCREEN_CENTER - 150, helpers.SCREEN_CENTER + 150
                ),
                -80,
                0.6,
                helpers.enemy_speed,
            )
        )
        helpers.enemy_cooldown = 80
    else:
        helpers.enemy_cooldown -= helpers.enemy_cooldown_reducing_val


player = Car("player", helpers.SCREEN_CENTER, helpers.SCREEN_HEIGHT - 70, 0.8, 5)


def execute_game():
    draw_bg()
    play_background_music()

    player.update()
    player.draw()

    if player.alive:
        create_enemies()
        helpers.enemy_group.update()
        helpers.enemy_group.draw(helpers.screen)

    for event in pygame.event.get():
        if not player.alive:
            helpers.moving_up = helpers.moving_down = helpers.moving_left = (
                helpers.moving_right
            ) = False

            if event.type == pygame.KEYDOWN and event.key != pygame.K_ESCAPE:
                player.reset()

            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                helpers.run = False
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                helpers.moving_up = True
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                helpers.moving_left = True
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                helpers.moving_down = True
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                helpers.moving_right = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                helpers.moving_up = False
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                helpers.moving_left = False
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                helpers.moving_down = False
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                helpers.moving_right = False

    pygame.display.update()
