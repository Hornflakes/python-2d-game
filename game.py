import pygame
import random

pygame.init()
window = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("ULTIMATE GHOST FIGHT 9000")


class player:
    def __init__(
        self,
        x,
        y,
        width,
        height,
        ghostLeft,
        ghostRight,
        ghostCrouchLeft,
        ghostCrouchRight,
        ball,
        left,
        right,
        balls,
        ghostShootLeft,
        ghostShootRight,
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 6
        self.jumps = False
        self.jumpPhase = -25
        self.crouch = False
        self.right = right
        self.left = left
        self.ghostLeft = ghostLeft
        self.ghostRight = ghostRight
        self.ghostCrouchLeft = ghostCrouchLeft
        self.ghostCrouchRight = ghostCrouchRight
        self.ball = ball
        self.balls = balls
        self.health = 10
        self.shootPhase = -1
        self.lastShot = 0
        self.ballLoad = 5
        self.ballReload = 0
        self.ghostShootLeft = ghostShootLeft
        self.ghostShootRight = ghostShootRight
        self.gravity = 5
        self.floatPhase = 0
        self.float = 0
        self.score = 0
        self.crouchTime = 3


def objectRender(objects):
    for object in objects:
        window.blit(object.image, (object.x, object.y))
    window.blit(
        pygame.font.SysFont("comicsansms", 100).render(
            str(player1.score), 1, (255, 180, 22)
        ),
        (30, 0),
    )
    window.blit(
        pygame.font.SysFont("comicsansms", 100).render(
            str(player2.score), 1, (255, 180, 22)
        ),
        (
            1890
            - (
                pygame.font.SysFont("comicsansms", 100)
                .render(str(player2.score), 1, (255, 180, 22))
                .get_width()
            ),
            0,
        ),
    )


def movementDrawShoot(player, left, right, jump, crouch, shoot, objects):
    if player.ballLoad < 5:
        player.ballReload += 1
        if player.ballReload % 75 == 0:
            player.ballLoad += 1
    else:
        player.ballReload = 0
    global hearts
    for heart in hearts:
        if (
            heart.x <= player.x + player.width
            and heart.x + heart.width >= player.x
            and player.health < 10
            and heart.y >= player.y
            and heart.y <= player.y + player.height
        ):
            hearts.pop(hearts.index(heart))
            if player.health > 5:
                player.health += 10 - player.health
            else:
                player.health += 5
    if player.crouchTime > 3 and player.crouch is False:
        player.crouchTime -= 1
    player.floatPhase += 1
    if player.floatPhase % 30 == 0 and player.float == 0 and player.jumps is False:
        player.y += 8
        player.float = 1
    elif player.floatPhase % 30 == 0 and player.float == 1 and player.jumps is False:
        player.y -= 8
        player.float = 0
    player.y += player.gravity
    player.gravity = 5
    for object in objects:
        if (
            player.y + player.height >= object.y
            and player.y + player.height <= object.y + object.height / 5
            and player.x > object.x - player.width / 2
            and player.x < object.x + object.width - player.width / 2
        ):
            player.gravity = 0
            if player.jumps and player.y + player.height > object.y:
                player.y = object.y - player.height
                player.jumps = False
                player.jumpPhase = -25
    for ball in player.balls:
        if ball.x > 0 and ball.x < 1920:
            ball.x += ball.velocity
        else:
            player.balls.pop(player.balls.index(ball))
    if player.y > 1080:
        player.health = 0
    if player.health > 0:
        if shoot and player.crouch is False and player.ballLoad > 0:
            player.shootPhase += 1
            if player.left is True and player.shootPhase % 15 == 0:
                player.ballLoad -= 1
                facing = -1
                player.balls.append(
                    projectile(player.x + 56, player.y + 28, 12, player.ball, facing)
                )
            elif player.right is True and player.shootPhase % 15 == 0:
                player.ballLoad -= 1
                facing = 1
                player.balls.append(
                    projectile(player.x + 56, player.y + 28, 12, player.ball, facing)
                )
        elif player.shootPhase != -1:
            player.lastShot += 1
            if player.lastShot == 15:
                player.shootPhase == -1
        if left and player.x > 0:
            player.x -= player.velocity
            player.left = True
            player.right = False
        if right and player.x + player.width < 1920:
            player.x += player.velocity
            player.right = True
            player.left = False
        if not (player.jumps):
            if crouch and player.crouch is False and player.crouchTime == 3:
                player.y = player.y + 50
                player.height = 70
                player.crouch = True
            if not crouch and player.crouch is True or player.crouchTime >= 296:
                player.y = player.y - 50
                player.height = 120
                player.crouch = False
            for object in objects:
                if (
                    jump
                    and player.crouch is False
                    and player.y + player.height >= object.y
                    and player.y + player.height <= object.y + object.height / 5
                    and player.x > object.x - player.width / 2
                    and player.x < object.x + object.width - player.width / 2
                ):
                    player.jumps = True
        else:
            if player.jumpPhase <= 25:
                player.y += player.jumpPhase
                player.jumpPhase += 1
            else:
                player.jumps = False
                player.jumpPhase = -25
        if shoot and not crouch and player.ballLoad > 0:
            if player.left is True and left and not right:
                window.blit(player.ghostShootLeft, (player.x, player.y))
            elif player.right is True and right and not left:
                window.blit(player.ghostShootRight, (player.x, player.y))
            elif player.left is True:
                window.blit(player.ghostShootLeft, (player.x, player.y))
            elif player.right is True:
                window.blit(player.ghostShootRight, (player.x, player.y))
        elif player.crouch is True:
            if player.left is True and left and not right:
                player.crouchTime += 1
                window.blit(player.ghostCrouchLeft, (player.x, player.y))
            elif player.right is True and right and not left:
                player.crouchTime += 1
                window.blit(player.ghostCrouchRight, (player.x, player.y))
            elif player.left is True:
                player.crouchTime += 1
                window.blit(player.ghostCrouchLeft, (player.x, player.y))
            elif player.right is True:
                player.crouchTime += 1
                window.blit(player.ghostCrouchRight, (player.x, player.y))
        else:
            if player.left is True and left and not right:
                window.blit(player.ghostLeft, (player.x, player.y))
            elif player.right is True and right and not left:
                window.blit(player.ghostRight, (player.x, player.y))
            elif player.left is True:
                window.blit(player.ghostLeft, (player.x, player.y))
            elif player.right is True:
                window.blit(player.ghostRight, (player.x, player.y))
        for ball in player.balls:
            window.blit(ball.image, (ball.x, ball.y))
        pygame.draw.rect(window, (255, 255, 255), (player.x, player.y - 28, 100, 19))
        pygame.draw.rect(
            window,
            (255, 0, 0),
            (player.x + 1, player.y - 18, 10 * player.health - 2, 8),
        )
        pygame.draw.rect(
            window,
            (0, 0, 255),
            (player.x + 1, player.y - 27, (299 - player.crouchTime) // 3, 8),
        )
        for i in range(0, player.ballLoad):
            pygame.draw.rect(
                window, (255, 255, 255), (player.x + i * 10, player.y - 40, 8, 8)
            )
    else:
        if player1.health == 0:
            player2.score += 1
            window.blit(
                pygame.font.SysFont("comicsansms", 100).render(
                    "black ghost wins", 1, (255, 180, 22)
                ),
                (
                    960
                    - pygame.font.SysFont("comicsansms", 100)
                    .render("black ghost wins", 1, (255, 180, 22))
                    .get_width()
                    / 2,
                    540
                    - pygame.font.SysFont("comicsansms", 100)
                    .render("black ghost wins", 1, (255, 180, 22))
                    .get_height()
                    / 2,
                ),
            )
        elif player2.health == 0:
            player1.score += 1
            window.blit(
                pygame.font.SysFont("comicsansms", 100).render(
                    "white ghost wins", 1, (255, 180, 22)
                ),
                (
                    960
                    - pygame.font.SysFont("comicsansms", 100)
                    .render("white ghost wins", 1, (255, 180, 22))
                    .get_width()
                    / 2,
                    540
                    - pygame.font.SysFont("comicsansms", 100)
                    .render("white ghost wins", 1, (255, 180, 22))
                    .get_height()
                    / 2,
                ),
            )
        pygame.mixer.music.stop()
        music = pygame.mixer.music.load("media/music.mp3")
        pygame.mixer.music.play()
        pygame.display.update()
        player1.x = 150
        player1.y = 400
        player2.x = 1670
        player2.y = 400
        player1.left = False
        player1.right = True
        player2.left = True
        player2.right = False
        player1.health = 10
        player2.health = 10
        hearts = []
        player1.balls = []
        player2.balls = []
        player1.ballLoad = 5
        player1.ballReload = 0
        player1.lastShot = 0
        player2.ballLoad = 5
        player2.ballReload = 0
        player2.lastShot = 0
        lifeCount = 1
        pygame.time.delay(2000)


def hit(player, enemy, objects):
    for ball in player.balls:
        for object in objects:
            if (
                ball.y - ball.radius < object.y + object.height
                and ball.y + ball.radius > object.y
                and ball.x + ball.radius > object.x
                and ball.x - ball.radius < object.x + object.width
            ):
                player.balls.pop(player.balls.index(ball))
        if (
            ball.y - ball.radius < enemy.y + enemy.height
            and ball.y + ball.radius > enemy.y
        ):
            if (
                ball.x + ball.radius > enemy.x
                and ball.x - ball.radius < enemy.x + enemy.width
            ):
                player.balls.pop(player.balls.index(ball))
                enemy.health -= 1


class projectile:
    def __init__(self, x, y, radius, image, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.image = image
        self.facing = facing
        self.velocity = 8 * facing


class object:
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image


class life:
    def __init__(self, x):
        self.x = x
        self.y = 494
        self.width = 36
        self.height = 36
        self.image = pygame.image.load("media/life.png").convert_alpha()
        self.floatPhase = 0
        self.float = 0


background = pygame.image.load("media/background.jpg").convert_alpha()


class title:
    def __init__(self, image):
        self.image = image
        self.x = background.get_width() / 2 - self.image.get_width() / 2
        self.y = 340
        self.float = 0
        self.floatPhase = 0


def lifeGeneration():
    global lifeCount
    lifeCount += 1
    if lifeCount % 700 == 0:
        heart = life(random.choice([182, 1702]))
        hearts.append(heart)
        if len(hearts) > 1:
            hearts.pop(hearts.index(hearts[0]))
    for heart in hearts:
        heart.floatPhase += 1
        if heart.floatPhase % 20 == 0 and heart.float == 0:
            heart.y -= 8
            heart.float = 1
        elif heart.floatPhase % 20 == 0 and heart.float == 1:
            heart.y += 8
            heart.float = 0
        window.blit(heart.image, (heart.x, heart.y))


def titleRender(title):
    title.floatPhase += 1
    if title.floatPhase % 80 == 0 and title.float == 0:
        title.y -= 8
        title.float = 1
    elif title.floatPhase % 80 == 0 and title.float == 1:
        title.y += 8
        title.float = 0
    window.blit(title.image, (title.x, title.y))


title = title(pygame.image.load("media/title.png").convert_alpha())
music = pygame.mixer.music.load("media/music.mp3")
player1 = player(
    150,
    400,
    108,
    120,
    pygame.image.load("media/whiteghostleft.png").convert_alpha(),
    pygame.image.load("media/whiteghostright.png").convert_alpha(),
    pygame.image.load("media/whiteghostcrouchleft.png").convert_alpha(),
    pygame.image.load("media/whiteghostcrouchright.png").convert_alpha(),
    pygame.image.load("media/whiteball.png").convert_alpha(),
    False,
    True,
    [],
    pygame.image.load("media/whiteghostshootleft.png").convert_alpha(),
    pygame.image.load("media/whiteghostshootright.png").convert_alpha(),
)
player2 = player(
    1670,
    400,
    108,
    120,
    pygame.image.load("media/blackghostleft.png").convert_alpha(),
    pygame.image.load("media/blackghostright.png").convert_alpha(),
    pygame.image.load("media/blackghostcrouchleft.png").convert_alpha(),
    pygame.image.load("media/blackghostcrouchright.png").convert_alpha(),
    pygame.image.load("media/blackball.png").convert_alpha(),
    True,
    False,
    [],
    pygame.image.load("media/blackghostshootleft.png").convert_alpha(),
    pygame.image.load("media/blackghostshootright.png").convert_alpha(),
)
objects = []
platform1 = object(
    100, 540, 200, 100, pygame.image.load("media/cloud.png").convert_alpha()
)
objects.append(platform1)
platform2 = object(
    1620, 540, 200, 100, pygame.image.load("media/cloud.png").convert_alpha()
)
objects.append(platform2)
platform3 = object(
    450, 540, 1020, 100, pygame.image.load("media/longcloud.png").convert_alpha()
)
objects.append(platform3)
platform4 = object(
    660, 340, 600, 90, pygame.image.load("media/shortcloud.png").convert_alpha()
)
objects.append(platform4)
lifeCount = 1
hearts = []
menu = True
while menu:
    pygame.time.delay(5)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu = False
            play = False
    window.fill((0, 0, 0))
    titleRender(title)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        menu = False
        play = True
    pygame.display.update()
pygame.mixer.music.play()
while play:
    pygame.time.delay(5)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
    window.blit(background, (0, 0))
    keys = pygame.key.get_pressed()
    objectRender(objects)
    lifeGeneration()
    movementDrawShoot(
        player1,
        keys[pygame.K_a],
        keys[pygame.K_d],
        keys[pygame.K_w],
        keys[pygame.K_s],
        keys[pygame.K_SPACE],
        objects,
    )
    movementDrawShoot(
        player2,
        keys[pygame.K_LEFT],
        keys[pygame.K_RIGHT],
        keys[pygame.K_UP],
        keys[pygame.K_DOWN],
        keys[pygame.K_KP0],
        objects,
    )
    hit(player1, player2, objects)
    hit(player2, player1, objects)
    pygame.display.update()
pygame.quit()
