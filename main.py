import pygame

imagePath = '/data/data/com.mikupiku.mikupikugame1/files/app/'

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("MikuPikuRPG")
# Картинки
icon = pygame.image.load('images/icon.png').convert_alpha()
backgroundMain = pygame.image.load('images/bgmain.png').convert_alpha()
playerImgMain = pygame.image.load('images/ленабаза.png').convert_alpha()
backgroundStage1 = pygame.image.load('images/bgstage1.png').convert_alpha()
playerImgStatic = pygame.image.load('images/player.png').convert_alpha()
enemy1 = pygame.image.load('images/mikuenemy.png').convert_alpha()
kunai = pygame.image.load('images/kunai.png').convert_alpha()
runLeft = [
    pygame.image.load('images/playerleft8.png').convert_alpha(),
    pygame.image.load('images/playerleft7.png').convert_alpha(),
    pygame.image.load('images/playerleft6.png').convert_alpha(),
    pygame.image.load('images/playerleft5.png').convert_alpha(),
    pygame.image.load('images/playerleft4.png').convert_alpha(),
    pygame.image.load('images/playerleft3.png').convert_alpha(),
    pygame.image.load('images/playerleft2.png').convert_alpha(),
    pygame.image.load('images/playerleft1.png').convert_alpha(),
]
runRight = [
    pygame.image.load('images/playerright1.png').convert_alpha(),
    pygame.image.load('images/playerright2.png').convert_alpha(),
    pygame.image.load('images/playerright3.png').convert_alpha(),
    pygame.image.load('images/playerright4.png').convert_alpha(),
    pygame.image.load('images/playerright5.png').convert_alpha(),
    pygame.image.load('images/playerright6.png').convert_alpha(),
    pygame.image.load('images/playerright7.png').convert_alpha(),
    pygame.image.load('images/playerright8.png').convert_alpha(),
]

pygame.display.set_icon(icon)
# Шрифты и текст
myFont = pygame.font.Font('fonts/Roboto-Black.ttf', 48)
textSurfaceMain = myFont.render('MikuPikuRPG', True, 'Black')
textSurfaceStart = myFont.render('Нажми пробел', True, 'White')
textSurfaceLose = myFont.render('Ты проиграл!', True, 'White')
loseRestart = myFont.render('Попробовать еще раз', True, 'Red')
restartButtonRect = loseRestart.get_rect(topleft=(425, 425))

playerAnimCount = 0
backgroundAnimX = 0
# Звуки и Музыка
backgroundSound1 = pygame.mixer.Sound('sounds/MikuRealHero.mp3')
backgroundSound2 = pygame.mixer.Sound('sounds/Hard Drive.mp3')
jumpSound = pygame.mixer.Sound('sounds/Alert.mp3')
# Параметры игрока
playerSpeed = 8
playerX = 50
playerY = 640
# Параметры противников
enemyY = 640
enemyListInGame = []
# Кунай(снаряд)
kunaiLeft = 5
kunaiSpeed = 9
kunais = []

isJump = False
jumpCount = 8

backgroundSound1.play()

enemyTimer = pygame.USEREVENT + 1
pygame.time.set_timer(enemyTimer, 2600)

gameplay = True

running = True

while running:

    screen.blit(backgroundStage1, (backgroundAnimX, 0))
    screen.blit(backgroundStage1, (backgroundAnimX + 1280, 0))

    if gameplay:

        playerHitBox = playerImgStatic.get_rect(topleft=(playerX, playerY))

        if enemyListInGame:
            for (i, el) in enumerate(enemyListInGame):
                screen.blit(enemy1, el)
                el.x -= 8

                if el.x < -10:
                    enemyListInGame.pop(i)

                if playerHitBox.colliderect(el):
                    screen.blit(textSurfaceLose, (525, 325))
                    jumpSound.play()
                    gameplay = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            screen.blit(runRight[playerAnimCount], (playerX, playerY))
        elif keys[pygame.K_LEFT]:
            screen.blit(runLeft[playerAnimCount], (playerX, playerY))
        else:
            screen.blit(playerImgStatic, (playerX, playerY))

        if keys[pygame.K_LEFT] and playerX > 0:
            playerX -= playerSpeed
        elif keys[pygame.K_RIGHT] and playerX < 1215:
            playerX += playerSpeed

        if not isJump:
            if keys[pygame.K_SPACE]:
                isJump = True
        else:
            if jumpCount >= -8:
                if jumpCount > 0:
                    playerY -= (jumpCount ** 2) / 2
                else:
                    playerY += (jumpCount ** 2) / 2
                jumpCount -= 1
            else:
                isJump = False
                jumpCount = 8

        if playerAnimCount == 7:
            playerAnimCount = 0
        else:
            playerAnimCount += 1

        backgroundAnimX -= 4
        if backgroundAnimX == -1280:
            backgroundAnimX = 0

        if kunais:
            for (i, el) in enumerate(kunais):
                screen.blit(kunai, (el.x, el.y))
                el.x += kunaiSpeed

                if el.x > 1280:
                    kunais.pop(i)

                if enemyListInGame:
                    for (index, enemy1El) in enumerate(enemyListInGame):
                        if el.colliderect(enemy1El):
                            enemyListInGame.pop(index)
                            kunais.pop(i)

    else:
        screen.blit(backgroundMain, (0, 0))
        screen.blit(textSurfaceLose, (525, 325))
        screen.blit(loseRestart, restartButtonRect)

        mouse = pygame.mouse.get_pos()
        if restartButtonRect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            playerX = 50
            enemyListInGame.clear()
            kunais.clear()
            kunaiLeft = 5

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == enemyTimer:
            enemyListInGame.append(enemy1.get_rect(topleft=(1280, 640)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_f and kunaiLeft > 0:
            kunais.append(kunai.get_rect(topleft=(playerX + 10, playerY + 10)))
            kunaiLeft -= 1

    clock.tick(18)