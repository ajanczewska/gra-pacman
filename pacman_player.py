import pygame
from settings import *
from pygame import mixer
class Player:
    def __init__(self, app, pos):
        """
        Metoda definiująca zmienne określające położenie gracza, kierunek ruchu, zdolność do poruszania się,
        punkty oraz życia gracza.
        """
        self.app = app
        self.grid_pos = pos
        self.pix_pos = vec(self.grid_pos.x*(self.app.cell_width)+self.app.cell_width//2,
        self.grid_pos.y*(self.app.cell_height)+self.app.cell_height//2
        +top_bottom_buffer)

        self.direction = vec(0, 0)
        self.stored_dir = None
        self.able_to_move = True
        self.score = 0
        self.lifes = 3

    def update(self):
        """Metoda aktualizująca pozycję gracza, kiedy jest to możliwe odpowiada również za dodawanie punktów gracza"""
        if self.able_to_move:
            self.pix_pos += self.direction
        if self.able_to_change_dir():
            self.grid_pos[0] = (self.pix_pos[0]-self.app.cell_width//2)//(self.app.cell_width)
            self.grid_pos[1] = (self.pix_pos[1]-top_bottom_buffer-self.app.cell_height//2)//self.app.cell_height
            if self.stored_dir != None:
                self.direction = self.stored_dir
            self.able_to_move = self.can_move()
        if self.on_coin():
            self.eat()

    def draw(self):
        """Metoda rysująca (w formie kół) gracza oraz posiadane przez niego życia."""
        pygame.draw.circle(self.app.screen, player_color, [int(self.pix_pos.x),
        int(self.pix_pos.y)],
        round(self.app.cell_width/2))

        for i in range(int(self.lifes)):
            pygame.draw.circle(self.app.screen, player_color, [int((i+1)*width//28+(i*2)), 560], int(self.app.cell_width//2))
    
    def on_coin(self):
        """Metoda zwracająca True, jeśli gracz znajduje się na polu z jedzonkiem, w przeciwnym wypadku False"""
        if self.grid_pos in self.app.coins:
            return True
        return False

    def eat(self):
        """
        Metoda generująca dźwięk, kiedy gracz jest na polu z jedzonkiem
        Usuwąca jedzonko
        Dodająca 1 do zmiennej score
        """
        mixer.music.load('eat.wav')
        mixer.music.play()
        self.app.coins.remove(self.grid_pos)
        self.score += 1

    def move(self, direction):
        """Metoda zmieniąca wartość zmiennej stored_dir na kierunek ruchu gracza"""
        self.stored_dir = direction

    def able_to_change_dir(self):
        """Metoda zwracająca True, kiedy gracz może zostać zmienić kieunek (jest w środku komórki), w przeciwnym wypadku False"""
        if int((self.pix_pos.x-self.app.cell_width//2) % self.app.cell_width) == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int((self.pix_pos.y-top_bottom_buffer-self.app.cell_height//2) % self.app.cell_height) == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True
        return False

    def can_move(self):
        """Metoda sprawdzajaca czy kolejne położenie gracza jest ścianą, jeśli tak zwraca False, w przeciwnym wypadku True"""
        for wall in self.app.walls:
            if vec(self.grid_pos+self.direction) == wall:
                return False
        return True
     
       