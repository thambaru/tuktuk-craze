import pygame
import helpers


def show_intro():
    helpers.screen.fill(helpers.BLACK)
    img = pygame.image.load(f"{helpers.IMAGES_DIR}/intro-screen.jpg")
    img = pygame.transform.scale(img, (helpers.SCREEN_WIDTH, helpers.SCREEN_HEIGHT))
    helpers.screen.blit(img, (0, 0))
    helpers.drawTextWithBg(
        "Press ENTER to start",
        helpers.SCREEN_CENTER - 100,
        helpers.SCREEN_CENTER - 175,
        helpers.WHITE,
        helpers.BLACK,
    )
    credits_font = pygame.font.SysFont("Courier New", 15)
    helpers.drawText("Created by: Group 06 - American Corner, Matara", helpers.GRAY, 20, helpers.SCREEN_HEIGHT - 50, credits_font)
    helpers.drawText("Copyright 2024 | All Rights Reserved.", helpers.GRAY, 20, helpers.SCREEN_HEIGHT - 30, credits_font)
    pygame.display.update()
