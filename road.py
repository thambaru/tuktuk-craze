import pygame
import helpers

class Road:
    def __init__(self, scale=2):
        self.image = pygame.image.load(f"{helpers.IMAGES_DIR}/road.png").convert_alpha()
        self.image = helpers.get_scaled_image(self.image, scale)
        self.scale = scale

    def draw(self):
        img_x = (helpers.SCREEN_CENTER) - (self.image.get_width() * self.scale // 2)
        img_y = 0
        for i in range(helpers.SCREEN_HEIGHT // self.image.get_height() + 1):
            img_y = i * self.image.get_height()
            helpers.screen.blit(
                helpers.get_scaled_image(self.image, self.scale), (img_x, img_y)
            )