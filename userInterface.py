import pygame
import random
import sys
import time

pygame.init()  # pylint: disable=no-member

gray = (51, 51, 51)
white = (255, 255, 255)
darkWhite = (255, 222, 173)

FPS = 15
X = 800
Y = 600


gameExit = False
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 50)
fontInst = pygame.font.SysFont("Arial", 20)
fontLarge = pygame.font.SysFont("Arial", 100)


def startGame():
    gameExit = True  # pylint: disable=unused-variable
    pygame.quit()  # pylint: disable=no-member
    game()
    sys.exit()


def game():
    pass


def button(x, y, width, height, inactive, active, action=None):
    cur = pygame.mouse.get_pos()

    click = pygame.mouse.get_pressed()

    if x + width > cur[0] > x and y + height > cur[1] > y:
        pygame.draw.rect(gameDisplay, inactive, (x, y, width, height))
        if click[0] == 1 and action != None:
            if action == "startGame":
                startGame()
    else:
        pygame.draw.rect(gameDisplay, active, (x, y, width, height))


def LoadScreen():
    global gameDisplay
    gameDisplay = pygame.display.set_mode((X, Y))
    pygame.display.set_caption("The Random Game")

    pygame.display.update()
    # Text
    Instructions = "Welcome to the text-based game, where absolutely everything that happends is randomised."
    InstructionsTwo = "Yes including the damage you deal and the health you have."
    text = font.render("The Random Game", True, white)
    inst = fontInst.render(Instructions, True, white)
    instTwo = fontInst.render(InstructionsTwo, False, white)
    textRect = text.get_rect()
    textRect.center = (X//2, Y//2.5)
    InstRect = inst.get_rect()
    InstRect.center = (X//2, Y//2)
    InstRectTwo = instTwo.get_rect()
    InstRectTwo.center = (X//2, Y//2+50)

    global gameExit
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # pylint: disable=no-member
                gameExit = True

        gameDisplay.fill(gray)
        gameDisplay.blit(text, textRect)
        gameDisplay.blit(inst, InstRect)
        gameDisplay.blit(instTwo, InstRectTwo)

        button(350, Y//1.5, 100, 50, darkWhite, white, action="startGame")
        btn_text = fontInst.render("Start", True, gray)
        btnRect = btn_text.get_rect()
        btnRect.center = (X//2, Y//1.5+25)
        gameDisplay.blit(btn_text, btnRect)
        pygame.display.update()

        clock.tick(FPS)


def DeathScreen():
    global gameDisplay

    gameDisplay = pygame.display.set_mode((X, Y))
    pygame.display.set_caption("The Random Game | You have Died")

    pygame.display.update()
    mainText = "You have Died"
    score = "Score: "
    title = font.render(mainText, True, white)
    titleRect = title.get_rect()
    titleRect.center = (X//2, Y//2.5)
    ScoreText = font.render(score, True, white)
    ScoreRect = ScoreText.get_rect()
    ScoreRect.center = (X // 2, Y//1.5 - 60)

    deathExit = False
    while not deathExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # pylint: disable=no-member
                deathExit = True

        gameDisplay.fill(gray)
        gameDisplay.blit(title, titleRect)
        gameDisplay.blit(ScoreText, ScoreRect)

        button(350, Y//1.5, 100, 50, darkWhite, white, action="startGame")
        btn_text = fontInst.render("Retry", True, gray)
        btnRect = btn_text.get_rect()
        btnRect.center = (X//2, Y//1.5+25)
        gameDisplay.blit(btn_text, btnRect)

        pygame.display.update()
        clock.tick(FPS)


def victoryScreen():
    global gameDisplay

    gameDisplay = pygame.display.set_mode((X, Y))
    pygame.display.set_caption("The Random Game")

    pygame.display.update()
    mainText = "Congratulations"
    score = "Score: "
    message = "You have just completed the very randomised game which I doubted was possible."
    extra = "You either had imense luck! or you took the easy route?"
    title = fontLarge.render(mainText, True, white)
    titleRect = title.get_rect()
    titleRect.center = (X//2, Y//2.5 - 180)
    ScoreText = font.render(score, True, white)
    ScoreRect = ScoreText.get_rect()
    ScoreRect.center = (X // 2, Y//1.5 - 60)
    messageText = fontInst.render(message, True, white)
    extraText = fontInst.render(extra, True, white)
    messageRect = messageText.get_rect()
    extraRect = extraText.get_rect()
    messageRect.center = (X // 2, Y//1.5 - 150)
    extraRect.center = (X // 2, Y//1.5 - 200)

    deathExit = False
    while not deathExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # pylint: disable=no-member
                deathExit = True

        gameDisplay.fill(gray)
        gameDisplay.blit(title, titleRect)
        gameDisplay.blit(ScoreText, ScoreRect)
        gameDisplay.blit(messageText, messageRect)
        gameDisplay.blit(extraText, extraRect)

        button(350, Y//1.5, 100, 50, darkWhite, white, action="startGame")
        btn_text = fontInst.render("Retry", True, gray)
        btnRect = btn_text.get_rect()
        btnRect.center = (X//2, Y//1.5+25)
        gameDisplay.blit(btn_text, btnRect)

        pygame.display.update()
        clock.tick(FPS)


victoryScreen()
DeathScreen()
LoadScreen()
pygame.quit()  # pylint: disable=no-member
quit()
