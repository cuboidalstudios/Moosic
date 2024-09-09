# Use time in the volume calculations

import sys
import math
import pygame
from PIL import Image

# initialization
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((1000, 750))
pygame.display.set_caption("Moosic")

iconPIL = Image.open("icon.png").resize((32, 32))
icon = (pygame.image.fromstring(iconPIL.tobytes(), iconPIL.size, iconPIL.mode))
pygame.display.set_icon(icon)

# image loading
playSprite = []
rewindSprite = []
skipSprite = []
lofiSprite = []
jazzSprite = []
dialSprite = []

for i in range(1, 6):
    temp1 = Image.open(f"resources/frames PausePlay/000{i}.png").resize((59, 60))
    playSprite.append(pygame.image.fromstring(temp1.tobytes(), temp1.size, temp1.mode))

    temp2 = Image.open(f"resources/frames rewind/000{i}.png").resize((59, 60))
    rewindSprite.append(pygame.image.fromstring(temp2.tobytes(), temp2.size, temp2.mode))

    temp3 = Image.open(f"resources/frame skip/000{i}.png").resize((59, 60))
    skipSprite.append(pygame.image.fromstring(temp3.tobytes(), temp3.size, temp3.mode))

    temp4 = Image.open(f"resources/frames lofi/000{i}.png").resize((59, 60))
    lofiSprite.append(pygame.image.fromstring(temp4.tobytes(), temp4.size, temp4.mode))

    temp5 = Image.open(f"resources/frames jazz/000{i}.png").resize((59, 60))
    jazzSprite.append(pygame.image.fromstring(temp5.tobytes(), temp5.size, temp5.mode))

for i in range(1, 61):
    if i < 10:
        i = "0" + str(i)

    temp6 = Image.open(f"resources/frames dial/00{i}.png").resize((211, 183))
    dialSprite.append(pygame.image.fromstring(temp6.tobytes(), temp6.size, temp6.mode))

mainImage = Image.open("resources/mainFrame.png").resize((1000, 750))
mainSprite = pygame.image.fromstring(mainImage.tobytes(), mainImage.size, mainImage.mode)

# defaults
playImage = playSprite[0]
rewindImage = rewindSprite[0]
skipImage = skipSprite[0]
lofiImage = lofiSprite[0]
jazzImage = jazzSprite[0]

playAnim = False
rewindAnim = False
skipAnim = False
lofiAnim = False
jazzAnim = False

aTick = 0
buttonTick = True
volume = 0  # 1-59
volumeChange = 0
dialFrame = 0
startPos = (0, 0)
endPos = (0, 0)

clicked = False

JCover = []
songsJ = []
mainCover = []

footerImage = pygame.image.load("resources/footer.png")

for i in range(1, 21):
    songsJ.append(f"audio/jazz songs/J{i}.mp3")
    tempImg = Image.open(f"resources/frames Screen/J{i}.png").resize((372, 218))
    JCover.append(pygame.image.fromstring(tempImg.tobytes(), tempImg.size, tempImg.mode))

for i in range(1, 3):
    temp7 = Image.open(f"resources/frames Screen/P{i}.png").resize((372, 218))
    mainCover.append(pygame.image.fromstring(temp7.tobytes(), temp7.size, temp7.mode))

currentSong = 0
currentScreen = "main"
paused = False
rtick = 0


# Action SubFunctions
def PlayPauseAction():
    global playAnim
    playAnim = True
    global paused
    global currentSong
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        paused = True
    else:
        pygame.mixer.music.unpause()
        paused = False


def RewindAction():
    global rewindAnim
    rewindAnim = True
    global currentScreen
    global currentSong
    if currentScreen == "jazz":
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("audio/click sfx.mp3")
            currentSong -= 1
            pygame.mixer.music.queue(songsJ[currentSong])
            pygame.mixer.music.play()
            global paused
            paused = False
        except IndexError:
            pygame.mixer.music.load(songsJ[19])
            currentSong = 19
            pygame.mixer.music.play()


def SkipAction():
    global skipAnim
    skipAnim = True
    global currentScreen
    global currentSong
    if currentScreen == "jazz":
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("audio/click sfx.mp3")
            currentSong += 1
            pygame.mixer.music.queue(songsJ[currentSong])
            pygame.mixer.music.play()
            global paused
            paused = False
        except IndexError:
            pygame.mixer.music.load(songsJ[0])
            currentSong = 0
            pygame.mixer.music.play()


def LofiAction():
    global lofiAnim
    lofiAnim = True
    pygame.mixer.music.stop()
    pygame.mixer.music.load("audio/click sfx.mp3")
    pygame.mixer.music.play()
    global currentScreen
    currentScreen = "main"
    global paused
    paused = False


def JazzAction():
    global jazzAnim
    jazzAnim = True
    global currentSong
    pygame.mixer.music.stop()
    pygame.mixer.music.load("audio/click sfx.mp3")
    global currentScreen
    currentScreen = "jazz"
    pygame.mixer.music.queue(songsJ[currentSong])
    pygame.mixer.music.play()
    global paused
    paused = False


# Mainloop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                PlayPauseAction()
            if event.key == pygame.K_q:
                RewindAction()
            if event.key == pygame.K_e:
                SkipAction()
            if event.key == pygame.K_1:
                LofiAction()
            if event.key == pygame.K_2:
                JazzAction()

    #  volume dial
    if volume > 59:
        volume = 59
    elif volume < 0:
        volume = 0

    for i in range(2):
        if dialFrame < volume:
            dialFrame += 1
        if dialFrame > volume:
            dialFrame -= 1

    try:
        dialImage = dialSprite[dialFrame]
    except IndexError:
        dialImage = dialSprite[volume]
        dialFrame = volume

    if buttonTick is True:
        if aTick == 4:
            aTick = 0
            buttonTick = False
            playAnim = False
            playImage = playSprite[0]
            rewindAnim = False
            rewindImage = rewindSprite[0]
            skipAnim = False
            skipImage = skipSprite[0]
            lofiAnim = False
            lofiImage = lofiSprite[0]
            jazzAnim = False
            jazzImage = jazzSprite[0]
        else:
            aTick += 1

    if playAnim is True:
        buttonTick = True
        playImage = playSprite[aTick]

    if rewindAnim is True:
        buttonTick = True
        rewindImage = rewindSprite[aTick]

    if skipAnim is True:
        buttonTick = True
        skipImage = skipSprite[aTick]

    if lofiAnim is True:
        buttonTick = True
        lofiImage = lofiSprite[aTick]

    if jazzAnim is True:
        buttonTick = True
        jazzImage = jazzSprite[aTick]

    # positioning

    screen.blit(mainSprite, (0, 0))
    screen.blit(playImage, (212, 435))
    screen.blit(rewindImage, (293, 435))
    screen.blit(skipImage, (372, 435))
    screen.blit(lofiImage, (453, 435))
    screen.blit(jazzImage, (529, 435))
    screen.blit(dialImage, (594, 192))
    screen.blit(footerImage, (0, 626))

    pos = pygame.mouse.get_pos()
    if pos[0] >= 212 and pos[1] >= 435 and pos[0] <= 270 and pos[1] <= 500:
        if pygame.mouse.get_pressed()[0] == 1 and clicked is False:
            clicked = True
            PlayPauseAction()
        if pygame.mouse.get_pressed()[0] == 0 and clicked is True:
            clicked = False

    elif pos[0] >= 293 and pos[1] >= 435 and pos[0] <= 350 and pos[1] <= 500:
        if pygame.mouse.get_pressed()[0] == 1 and clicked is False:
            clicked = True
            RewindAction()
        if pygame.mouse.get_pressed()[0] == 0 and clicked is True:
            clicked = False

    elif pos[0] >= 372 and pos[1] >= 435 and pos[0] <= 432 and pos[1] <= 500:
        if pygame.mouse.get_pressed()[0] == 1 and clicked is False:
            clicked = True
            SkipAction()
        if pygame.mouse.get_pressed()[0] == 0 and clicked is True:
            clicked = False

    elif pos[0] >= 453 and pos[1] >= 435 and pos[0] <= 512 and pos[1] <= 500:
        if pygame.mouse.get_pressed()[0] == 1 and clicked is False:
            clicked = True
            LofiAction()
        if pygame.mouse.get_pressed()[0] == 0 and clicked is True:
            clicked = False

    elif pos[0] >= 529 and pos[1] >= 435 and pos[0] <= 589 and pos[1] <= 500:
        if pygame.mouse.get_pressed()[0] == 1 and clicked is False:
            clicked = True
            JazzAction()
        if pygame.mouse.get_pressed()[0] == 0 and clicked is True:
            clicked = False

    elif pos[0] >= 529 and pos[1] >= 435 and pos[0] <= 589 and pos[1] <= 500:
        if pygame.mouse.get_pressed()[0] == 1 and clicked is False:
            clicked = True
            JazzAction()
        if pygame.mouse.get_pressed()[0] == 0 and clicked is True:
            clicked = False

    # dial / volume
    elif pos[0] >= 340 and pos[1] >= 205 and pos[0] <= 998 and pos[1] <= 368:
        if pygame.mouse.get_pressed()[0] == 1 and clicked is False:
            clicked = True
            startPos = pos
        if pygame.mouse.get_pressed()[0] == 0 and clicked is True:
            clicked = False
            endPos = pos
            volumeChange = (endPos[0] - startPos[0]) ** 2 / 5000
            if endPos[0] - startPos[0] < 0:
                volumeChange *= -1
                volume += int(math.floor(volumeChange))
            else:
                volume += int(math.ceil(volumeChange))
            volumeChange = 0

    if pygame.mixer.music.get_busy() is False and paused is False and currentScreen in ["jazz", "lofi"]:
        try:
            currentSong += 1
            pygame.mixer.music.load(songsJ[currentSong])
            pygame.mixer.music.play()
        except IndexError:
            pygame.mixer.music.load(songsJ[0])
            currentSong = 0
            pygame.mixer.music.play()

    if currentScreen == "jazz":
        screen.blit(JCover[currentSong], (219, 168))
    elif currentScreen == "lofi":
        pass
    else:
        screen.blit(mainCover[round((rtick % 30 / 29))], (219, 168))

    rtick += 1
    if rtick > 60:
        rtick = 0

    # update
    clock.tick(24)
    pygame.display.update()
