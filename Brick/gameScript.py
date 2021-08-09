import random
import time
from csv import *
from pygame_functions import *

class blocks:

    def __init__(self, WIDTH, HEIGHT, SB_WIDTH, SB_HEIGHT, NUM_ENEMIES, DELAY_SIZE, SIDE_STEP, SPEED, RED, BG_COLOR, BLUE, YELLOW, SCORE_COLOR, background, player_size, player_pos, enemy_size, enemy_pos, score, speed):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.SB_WIDTH = SB_WIDTH
        self.SB_HEIGHT = SB_HEIGHT
        self.NUM_ENEMIES = NUM_ENEMIES
        self.DELAY_SIZE = DELAY_SIZE
        self.SIDE_STEP = SIDE_STEP
        self.SPEED = SPEED
        self.RED = RED
        self.BG_COLOR = BG_COLOR
        self.BLUE = BLUE
        self.YELLOW = YELLOW
        self.SCORE_COLOR = SCORE_COLOR
        self.background = background
        self.player_size = player_size
        self.player_pos = player_pos
        self.enemy_size = enemy_size
        self.enemy_pos = enemy_pos
        self.enemy_list = [enemy_pos]
        self.myFont = pygame.font.SysFont("monospace", 25)
        self.myFont1 = pygame.font.SysFont("comicsansms", 35)
        self.myFont2 = pygame.font.SysFont("monospace", 65)
        self.buttFont = pygame.font.SysFont("monospace", 15)
        self.score = score
        self.SPEED = speed
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # changes speed of blocks based off of current speed
    def set_level(self):
        if self.score < 15:
            self.SPEED = self.SPEED
        elif self.score < 40:
            self.SPEED = 9
        elif self.score < 60:
            self.SPEED = 11
        else:
            self.SPEED = 13


    # drops enemies based off of whats on the screen
    def drop_enemies(self):
        delay = random.random()
        if len(self.enemy_list) < self.NUM_ENEMIES and delay < self.DELAY_SIZE:
            x_pos = random.randint(0, self.WIDTH - self.enemy_size)
            y_pos = 0
            self.enemy_list.append([x_pos, y_pos])


    # create enemy squares
    def draw_enemies(self):
        for enemy_pos in self.enemy_list:
            pygame.draw.rect(self.screen, self.BLUE, (enemy_pos[0], enemy_pos[1], self.enemy_size, self.enemy_size))


    # Update new position of enemy
    def update_enemy_pos(self):
        for idx, enemy_pos in enumerate(self.enemy_list):
            if enemy_pos[1] >= 0 and enemy_pos[1] < self.HEIGHT:
                enemy_pos[1] += self.SPEED
            else:
                self.enemy_list.pop(idx)
                self.score += 1


    # return true if collision is detected
    def collision_check(self):
        for enemy_pos in self.enemy_list:
            if self.detect_collision(enemy_pos, self.player_pos):
                return True
        return False


    # detect collision
    def detect_collision(self, enemy_pos, player_pos):
        p_x = player_pos[0]
        p_y = player_pos[1]

        e_x = enemy_pos[0]
        e_y = enemy_pos[1]

        # x coordinate
        if ((e_x >= p_x) and (e_x < p_x + self.player_size)) or ((p_x >= e_x) and (p_x < (e_x + self.enemy_size))):
            # y coordinate
            if ((p_y <= e_y) and (e_y < (p_y + self.player_size))) or ((p_y >= e_y) and (p_y < (e_y + self.enemy_size))):
                return True
        return False


    def get_HS(self):
        f = open("HighScore.txt", 'r')
        HSstr = f.read()
        f.close()
        print("\n \nCURRENT HIGH SCORE: " + HSstr)
        return HSstr



    def game_loop(self):
        self.screen.fill(self.BG_COLOR)
        # Initialize boolean and clock
        game_over = False
        newHigh = False
        clock = pygame.time.Clock()

        HS = self.get_HS()

        # game loop
        while not game_over:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    x = self.player_pos[0]
                    y = self.player_pos[1]

                    if event.key == pygame.K_LEFT:
                        x -= self.SIDE_STEP
                    elif event.key == pygame.K_RIGHT:
                        x += self.SIDE_STEP
                    self.player_pos = [x, y]

            self.screen.fill(self.BG_COLOR)
            self.drop_enemies()
            self.update_enemy_pos()
            self.set_level()
            # put score on the screen
            text = "Score: " + str(self.score)
            scorelabel = self.myFont.render(text, True, self.YELLOW)
            self.screen.blit(scorelabel, (self.WIDTH - 150, self.HEIGHT - 25))
            # put high score on the screen
            text1 = "HS: " + HS
            highscorelabel = self.myFont.render(text1, True, self.YELLOW)
            self.screen.blit(highscorelabel, (self.WIDTH - 150, self.HEIGHT - 50))

            if self.collision_check():
                print("SCORE: " + str(self.score))

                if self.score > int(HS):  # new high score
                    newHigh = True

                    text2 = "NEW HIGH SCORE!"
                    newhighlabel = self.myFont2.render(text2, True, self.YELLOW)
                    self.screen.blit(newhighlabel, ((self.WIDTH/2)-320, (self.HEIGHT/2)-50))
                    pygame.display.update()
                    time.sleep(3)
                    HSstr = str(self.score)
                    f = open("HighScore.txt", 'r+')
                    f.truncate(0)
                    f.write(HSstr)
                    f.close()
                    print("CONGRATS! YOU NOW HAVE THE NEW HIGH SCORE!")
                    print("HIGH SCORE: " + str(self.score) + "\n")
                else:  # lost
                    text3 = "SORRY! TRY AGAIN."
                    loselabel = self.myFont2.render(text3, True, self.YELLOW)
                    self.screen.blit(loselabel, ((self.WIDTH/2)-320, (self.HEIGHT/2)-50))
                    pygame.display.update()
                    time.sleep(3)
                    print("SORRY, TRY AGAIN NEXT TIME")
                    print("HIGH SCORE: " + HS + "\n")
                break

            self.draw_enemies()
            pygame.draw.rect(self.screen, self.RED, (self.player_pos[0], self.player_pos[1], self.player_size, self.player_size))
            clock.tick(30)
            pygame.display.update()
        pygame.display.quit()

        pygame.init()
        if newHigh:
            screenSize(300, 150)
            instructionLabel = makeLabel("ENTER NAME", 40, 55, 25, "blue", "Agency FB", "white")
            showLabel(instructionLabel)

            wordBox = makeTextBox(30, 80, 240, 2, "Enter text here", 0, 24)
            showTextBox(wordBox)
            name = textBoxInput(wordBox)

        # screen 2
        screen2 = pygame.display.set_mode((self.SB_WIDTH, self.SB_HEIGHT))
        screen2.fill("white")
        pygame.display.update()

        game_over1 = False

        leaders = {}

        with open('scoreboard.txt', 'r') as read_obj:
            csv_dict_reader = DictReader(read_obj)
            for row in csv_dict_reader:
                leaders[row['name']] = int(row['score'])

        # old name input
        if newHigh:
            leaders[name] = self.score

        sorted_leaders = sorted(leaders.items(), key=lambda x: x[1], reverse=True)

        if len(sorted_leaders) == 11:
            sorted_leaders.pop()

        f = open('scoreboard.txt', 'w+')
        f.write("name,score\n")
        with f:
            write = writer(f)
            write.writerows(sorted_leaders)
        f.close()


        while not game_over1:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    game_over1 = True

            mouse = pygame.mouse.get_pos()

            SB_TEXT = "SCOREBOARD"
            scoreboardlabel = self.myFont.render(SB_TEXT, True, self.BLUE)
            click = pygame.mouse.get_pressed()
            screen2.blit(scoreboardlabel, ((self.SB_WIDTH/2)-90, 20))
            pygame.display.update()

            for idx, i in enumerate(sorted_leaders):
                (name, score) = sorted_leaders[idx]
                Name = str(idx+1) + ". " + name + ": " + str(score)
                namelabel = self.myFont.render(Name, True, self.BLUE)
                screen2.blit(namelabel, ((self.SB_WIDTH/2)-105, 70 + (idx*40)))
                pygame.display.update()

            pygame.draw.rect(screen2, (200, 0, 0), (75, 500, 100, 50))
            pygame.display.update()

            pygame.draw.rect(screen2, (0, 200, 0), (300, 500, 100, 50))
            pygame.display.update()

            if (75 < mouse[0] < 175) and (500 < mouse[1] < 550):
                pygame.draw.rect(screen2, (255, 0, 0), (75, 500, 100, 50))
                pygame.display.update()
                if click[0] == 1:
                    print("CLOSE")
                    break

            if (300 < mouse[0] < 400) and (500 < mouse[1] < 550):
                pygame.draw.rect(screen2, (0, 255, 0), (300, 500, 100, 50))
                pygame.display.update()
                if click[0] == 1:
                    print("REPLAY")
                    g = blocks(1200, 800, 500, 600, 30, 0.25, 43, 8, (255, 0, 0), (30, 30, 30), (0, 0, 255),
                               (255, 255, 0), (10, 0, 100), (255, 255, 255), 50, [600, 700], 50,
                               [random.randint(0, 750), 0], 0, 8)
                    g.game_loop()

            textSurf = self.buttFont.render("CLOSE", True, (255, 255, 255))
            textRect = (100, 515)
            screen2.blit(textSurf, textRect)
            pygame.display.update()

            textSurf2 = self.buttFont.render("REPLAY", True, (255, 255, 255))
            textRect2 = (325, 515)
            screen2.blit(textSurf2, textRect2)
            pygame.display.update()
        pygame.quit()


g = blocks(1200, 800, 500, 600, 30, 0.25, 43, 8, (255, 0, 0), (30, 30, 30), (0, 0, 255), (255, 255, 0), (10, 0, 100), (255, 255, 255), 50, [600, 700], 50, [random.randint(0, 750), 0], 0, 8)
g.game_loop()