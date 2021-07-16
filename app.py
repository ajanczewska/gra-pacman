import pygame
from pygame import mixer
from pygame.locals import *
from settings import *
from pacman_player import *
from pygame.math import Vector2 as vec
from ghost import *

pygame.init()

class App:
    def __init__(self):
        """Metoda definiująca zmienne używane w klasie"""
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        self.cell_width = maze_width//COLUMNS
        self.cell_height = maze_height//ROWS
        self.player_start_position = None
    
        self.walls = []
        self.coins = []
        self.enemies = []
        self.enemies_positions = []
        self.load()
        self.create_enemies()
        self.player = Player(self, self.player_start_position)
        self.the_best_scores = [0]

    def run(self):
        """Metoda wywołująca główną pętlę aplikacji i w zależności od jej 'statusu' odpowiednie metody"""
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_draw()

            if self.state == 'menu_highscores':
                self.menu_events()
                self.draw_table()

            if self.state == 'menu_rules':
                self.menu_events()
                self.draw_rules()

            if self.state == 'menu_author':
                self.menu_events()
                self.draw_about_author()
            
            if self.state == 'playing':
                self.playing_events()
                self.playing_updates()
                self.playing_draw()

            if self.state == 'game over':
                self.game_over_events()
                self.game_over_draw()

            if self.state == 'win':
                self.win_events()
                self.win_draw()

            self.clock.tick(fps)
        pygame.quit()
    
    def draw_text(self, text, screen, position, color, font_name, font_size, center=True):
        """Metoda odpowiadająca za generowanie tekstu"""
        font = pygame.font.SysFont(font_name, font_size)
        text = font.render(text, False, color)
        if center:
            position[0] = position[0] - text.get_size()[0]/2
            position[1] = position[1]
        screen.blit(text, position)

    def load(self):
        """
        Metoda tworząca tło gry(labirynt)
        Wpisująca do list(walls, coins, enemies_positions) wektory na podstawie mapy z pliku tekstowego
        Przypisująca do zmiennej player_start_position wektor na podstawie mapy z pliku tekstowego
        """
        self.maze = pygame.image.load('background.png')
        self.maze = pygame.transform.scale(self.maze, (maze_width, maze_height))
        with open ('walls.txt', 'r') as file:
            for yindx, line in enumerate(file):
                for xindx, char in enumerate(line):
                    if char == '1':
                        self.walls.append(vec(xindx, yindx))
                    elif char == '0':
                        self.coins.append(vec(xindx, yindx))
                    elif char == 'S':
                        self.player_start_position = vec(xindx, yindx)
                    elif char in ['P', 'B', 'C', 'I']:
                        self.enemies_positions.append(vec(xindx, yindx))
        file.close()          
    def create_enemies(self):
        """Metoda tworząca duchy i zapisująca te obiekty do tablicy przypisanej do zmiennej enemies"""
        for indx, pos in enumerate(self.enemies_positions):
            self.enemies.append(Ghost(self, pos, ENEMY_COLORS_LIST[indx]))

    def draw_coins(self):
        """Metoda odpowidająca za rysowanie jedzonka(w kształcie koła) na planszy gry"""
        for coin in self.coins:
            pygame.draw.circle(self.screen, ORANGE_FOR_COINS, [int(coin.x*self.cell_width+self.cell_width//2),
            int(coin.y*self.cell_height+self.cell_height//2+top_bottom_buffer)], int(self.cell_width//5))

    def restart(self):
        """
        Metoda resetująca ustawienia aplikacji na początkowe
        Zmieniająca status gry na 'playing'
        """
        self.player.lifes = 3
        self.player.score = 0
        self.coins = []
        self.player.grid_pos = vec(13, 23)
        self.player.pix_pos = vec(self.player.grid_pos.x*(self.cell_width)+self.cell_width//2,
        self.player.grid_pos.y*(self.cell_height)+self.cell_height//2
        +top_bottom_buffer)
        self.player.direction = vec(0, 0)
        self.player.stored_dir = None
        self.player.score = 0
        self.enemies = []
        self.enemies_positions = [vec(12, 15), vec(13, 15), vec(14, 15), vec(15, 15)]
        self.create_enemies()
        with open ('walls.txt', 'r') as file:
            for yindx, line in enumerate(file):
                for xindx, char in enumerate(line):
                    if char == '0':
                        self.coins.append(vec(xindx, yindx))
        file.close()      
        self.state = 'playing'

    def saved_score(self):
        """Metoda zapisująca wynik gracza do pliku tekstowego"""
        with open('highscores.txt', 'a') as file:
            file.write(str(self.player.score) + '\n')
        file.close()
        
    def display_scores(self):
        """
        Metoda zwracająca tablicę z 10 najlepszymi wynikami
        W przypadku gdy w pliku jest zapisane mniejsza liczba wyników zwraca tablicę ze wszystkimi wynikami
        Jeżeli w pliku nie ma zapisanych żadnych wyników zwraca jednoelementową tablicę z wartością 0
        """
        tab = []
        with open('highscores.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.rstrip('\n')
                tab.append(int(line))
        file.close 
        if tab != []:
            tab.sort(reverse=True)
            if len(tab) > 10:
                return tab[0:10]
            return tab
        else:
            return [0]
    ########## MENU ###########         
    def menu_events(self):
        """
        Metoda przypisująca do zmiennej state staus 'start'
        lub kończąca działanie programu, w zależności od wyłapanego zdarzenia
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if  event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = 'start'
    ########## MENU SCORES FUNCTIONS ########### 
    def draw_table(self):
        """Metoda odpowiadająca za wyświetlanie w oknie aplikacji 10 najlepszych wyników"""
        self.screen.fill(BLACK)
        self.draw_text("THE BEST SCORES:", self.screen, [0, 10], WHITE, 'Arial black', 20, center=False)
        scores = self.display_scores()
        for i in range(len(scores)):
            self.draw_text("{}".format(i+1)+": "+"{}".format(scores[i]), self.screen,
                [0, (i+1)*height//11], WHITE, 'Arial black', 16, center=False)
        pygame.display.update()
    ########## MENU RULES FUNCTIONS ########### 
    def draw_rules(self):
        """Metoda odpowiadająca za wyświetlanie w oknie aplikacji zasad gry"""
        self.screen.fill(BLACK)
        self.draw_text("ZASADY:", self.screen, [10, height//11], WHITE, "Arial black", 20, center=False)
        self.draw_text("Poruszaj się żółtą kulką (Pac-Manem),", self.screen, [10, height//11+30], WHITE, "Arial black", 16, center=False)
        self.draw_text("jedz małe kulki i unikaj dużych kulek(duszków),", self.screen, [10, height//11+50], WHITE, "Arial black", 16, center=False)
        self.draw_text("trafienie na duszka oznacza utratę 1 z 3 żyć.", self.screen, [10, height//11+70], WHITE, "Arial black", 16, center=False)
        self.draw_text("Po utracie wszystkich żyć przegrywasz.", self.screen, [10, height//11+90], WHITE, "Arial black", 16, center=False)
        self.draw_text("Gra kończy się zwycięstwem po zjedzeniu",self.screen, [10, height//11+110], WHITE, "Arial black", 16, center=False)
        self.draw_text("wszystkich małych kulek,", self.screen, [10, height//11+130], WHITE, "Arial black", 16, center=False)
        self.draw_text("zanim stracisz życia.",self.screen, [10, height//11+150], WHITE, "Arial black", 16, center=False)
        pygame.display.update()
     ########## MENU RULES FUNCTIONS ########### 
    def draw_about_author(self):
        """Metoda odpowidająca za wyświetlanie w oknie aplikacji informacji o autorze"""
        self.screen.fill(BLACK)
        self.draw_text(AUTHOR, self.screen, [10, height//11], WHITE, "Arial black", 20, center=False)
        pygame.display.update()
    ########## START FUNCTIONS ########### 
    def start_events(self):
        """
        Metoda przypisująca do zmiennej state odpowiedni status aplikacji
        lub kończąca działanie programu, w zależności od wyłapanego zdarzenia
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if  event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.state = 'playing'
                if event.key == pygame.K_t:
                    self.state = 'menu_highscores'
                if event.key == pygame.K_r:
                    self.state = 'menu_rules'
                if event.key == pygame.K_a:
                    self.state = 'menu_author'
                if event.key == pygame.K_ESCAPE:
                    self.running = False  

    def start_draw(self):
        """Metoda odpowiadająca za wyświetlanie elementów w menu głównym"""
        self.screen.fill(BLACK)
        self.draw_text("HIGH SCORE: {}".format(self.display_scores()[0]), self.screen, [0, 0], WHITE, 'Arial black', 16, center=False)
        self.draw_text("START (press 'space')", self.screen, [width//2, height//2-50], YELLOW_FOR_MENU, 'Arial black', 16)
        self.draw_text("RULES (press 'r button')", self.screen, [width//2, height//2+50], YELLOW_FOR_MENU, 'Arial black', 16)
        self.draw_text("ABOUT AUTHOR (press 'a button')", self.screen, [width//2, height//2+100], YELLOW_FOR_MENU, 'Arial black', 16)
        self.draw_text("TOP 10 SCORES (press 't button')", self.screen, [width//2, height//2], YELLOW_FOR_MENU, 'Arial black', 16)
        self.draw_text("QUIT (press 'esc button')", self.screen, [width//2, height//2+170], YELLOW_FOR_MENU, 'Arial black', 16)
        pygame.display.update()

    ########## PLAYING FUNCTIONS ###########
    def playing_events(self):
        """
        Metoda wywołująca na klasie gracza metodę move z argumentem, który jest wektorem, przechowującym kierunek ruchu gracza
        lub kończąca działanie programu, w zależności od wyłapanego zdarzenia
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1, 0))
                if event.key == pygame.K_UP:
                    self.player.move(vec(0, -1))
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0, 1))

    def playing_updates(self):
        """
        Metoda wywołująca metody odpowidające za aktualizację ruchu gracza oraz duchów
        Sprawdzająca czy pozycja gracza i duchów pokrywają się
        Aktualizująca za sprawdzenie czy gracza wygrał
        """
        self.player.update()
        for enemy in self.enemies:
            enemy.update()
        for enemy in self.enemies:
            if enemy.grid_pos == self.player.grid_pos:
                mixer.music.load('pacman_dead.wav')
                mixer.music.play()
                pygame.time.wait(2000)
                self.player_killed()
        if self.player.score == coins_count:
            self.saved_score()
            mixer.music.load('win.wav')
            mixer.music.play()
            self.state = 'win'

    def playing_draw(self):
        """Metoda odpowidająca za wyświetlanie w głównym oknie elementów gry"""
        self.screen.fill(BLACK)
        self.screen.blit(self.maze, (0, top_bottom_buffer))
        self.draw_coins()
        self.draw_text('CURRENT SCORE: {}'.format(self.player.score),
        self.screen, [25, 3], WHITE, 'Arial black', 14, center=False)
        self.draw_text('HIGH SCORE: {}'.format(self.display_scores()[0])
        , self.screen, [width/2+25, 3], WHITE, 'Arial black', 14, center=False)
        
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        pygame.display.update()

    def player_killed(self):
        """
        Metoda odpowidająca za usuwanie życia gracza
        Zmieniająca położenie duchów i gracza na początkowe
        Generująca dżwięk i zmieniająca status gry na 'game over' w przypadku braku żyć
        """
        self.player.lifes -= 1
        self.enemies = []
        self.enemies_positions = [vec(12, 15), vec(13, 15), vec(14, 15), vec(15, 15)]
        if self.player.lifes <= 0:
            mixer.music.load('game_over.wav')
            mixer.music.play()
            self.saved_score()
            self.state = 'game over'

        else:
            self.player.direction = vec(0, 0)
            self.player.grid_pos = vec(13, 23)
            self.player.pix_pos = vec(self.player.grid_pos.x*(self.cell_width)+self.cell_width//2,
            self.player.grid_pos.y*(self.cell_height)+self.cell_height//2
            +top_bottom_buffer)
            self.create_enemies()
            
     ########## GAME OVER FUNCTIONS ###########
    def game_over_events(self):
        """Metoda kończąca działanie programu lub wywołująca metodę restart w zależności od wyłapanego zdarzenia"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_SPACE:
                    self.restart()
                
    def game_over_draw(self):
        """Metoda odpowiadająca za wyświetlanie elementów w głównym oknie po przegraniu gry"""
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER!", self.screen, [width//2, height//3], RED_FOR_LOSER, 'Arial black', 18)
        self.draw_text("PRESS 'SPACE' TO PLAY AGAIN", self.screen, [width//2, height//3+100],  YELLOW_FOR_MENU, 'Arial black', 16)
        self.draw_text("PRESS 'ESC' TO QUIT", self.screen, [width//2, height//3+150],  YELLOW_FOR_MENU, 'Arial black', 16)
        pygame.display.update()

    ########## WIN FUNCTIONS ###########
    def win_events(self):
        """Metoda kończąca program lub wywołująca metodę restart w zależności od wyłapanego zdarzenia"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_SPACE:
                    self.restart()
    
    def win_draw(self):
        """Metoda odpowidająca za wyświetlanie elementów w głównym oknie po wygraniu gry"""
        self.screen.fill(BLACK)
        self.draw_text("WIN!", self.screen, [width//2, height//3], BLUE_FOR_WINNER, 'Arial black', 20)
        self.draw_text("PRESS 'SPACE' TO PLAY AGAIN", self.screen, [width//2, height//3+100],  YELLOW_FOR_MENU, 'Arial black', 16)
        self.draw_text("PRESS 'ESC' TO QUIT", self.screen, [width//2, height//3+150],  YELLOW_FOR_MENU, 'Arial black', 16)
        pygame.display.update()