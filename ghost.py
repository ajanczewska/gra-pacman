import pygame
import random
from settings import *
vec = pygame.math.Vector2

class Ghost:
    def __init__(self, app, pos, color):
        self.app = app
        self.color = color
        self.grid_pos = pos
        self.pix_pos = vec(self.grid_pos.x*(self.app.cell_width)+self.app.cell_width//2,
        self.grid_pos.y*(self.app.cell_height)+self.app.cell_height//2
        +top_bottom_buffer)
        self.able_to_move = True
        self.personality = self.set_personality()
        self.direction = vec(0, 0)
        self.speed = self.set_speed()

    def update(self):
        """Metoda zmieniająca pozycję wroga, kiedy jest to możliwe."""
        if self.able_to_move:
            self.pix_pos += self.direction*self.speed 

        if self.able_to_change_dir():
            self.grid_pos[0] = (self.pix_pos[0]-self.app.cell_width//2)//(self.app.cell_width)
            self.grid_pos[1] = (self.pix_pos[1]-top_bottom_buffer-self.app.cell_height//2)//self.app.cell_height
            self.direction = self.move()
            self.able_to_move = self.can_move()

    def set_speed(self):
        """Metoda zwraca szybkość poruszania się ducha."""
        if self.personality == 'followed':
            self.speed = 1
        else:
            self.speed = 1
        return self.speed   

    def draw(self):
        """Metoda rysuje"""
        pygame.draw.circle(self.app.screen, self.color, [int(self.pix_pos.x),
        int(self.pix_pos.y)],
        round(self.app.cell_width/2))

    def set_personality(self):
        """Metoda zwracającąca (w zależności od koloru obiktu)'followed' lub 'random'"""
        if self.color == ENEMY_COLORS_LIST[0] or  self.color == ENEMY_COLORS_LIST[1] or  self.color == ENEMY_COLORS_LIST[2]:
            return 'followed'
        elif self.color == ENEMY_COLORS_LIST[3]:
            return 'random'

    def move(self):
        """Metoda zwracająca kieunek ruchu wroga."""
        if self.personality == 'followed':
            self.direction = self.created_path()
            return self.direction
        elif self.personality == 'random':
            self.direction = random.choice([vec(1,0), vec(-1,0), vec(0,1), vec(0,-1)])
            return self.direction

    def created_path(self):
        """Metoda optymalizująca ścieżkę ruchu i zwracająca wektor, w kierunkuktórego będzie się poruszał duch"""
        #celem jest gracz
        target = self.app.player.grid_pos 
        #maps tworzy 'siatkę' ruchu
        maps = [[0 for x in range(28)] for y in range(31)]
        for cell in self.app.walls:
            maps[int(cell.y)][int(cell.x)] = 1
        queue = [self.grid_pos]
        path = []
        visited  = []
        #pętla działa dopóki tablica queue nie jest pusta
        while queue:
            current = queue[0]
            queue.remove(current)
            visited.append(current)
            #jeśli duch jest na pozycji gracza przerywa działanie
            if current == target:
                break
            else:
                options = [vec(1, 0), vec(0, 1), vec(0, -1), vec(-1, 0)]
                #sprawdza każdą opcję ruchu
                for option in options:
                    next_cell = current + option
                    #odpowida za to, żeby obiekt się nie cofał i nie znalazł się na ścianie
                    if next_cell not in visited:
                        if maps[int(next_cell.y)][int(next_cell.x)] != 1:
                            queue.append(next_cell)
                            path.append({'current':current, 'next':next_cell})
        #szukamy optymalnego kierunku ruchu
        shortest_path = [target]
        while target != self.grid_pos:
            for step in path:
                if step['next'] == target:
                    target = step['current']
                    shortest_path.insert(0, step['current'])
        if len(shortest_path) >= 2:
            return shortest_path[1] - self.grid_pos
        else:
            return vec(0,0)
   

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
        """Metoda sprawdzająca czy kolejne położenie ducha jest ścianą, jeśli tak zwraca False, w przeciwnym wypadku True"""
        for wall in self.app.walls:
            if vec(self.grid_pos+self.direction) == wall:
                return False
        return True
    def set_start_enemy_pos(self):
        """Metoda zwracająca początkowe położenie wroga"""
        if self.color == ENEMY_COLORS_LIST[0]:
            return self.app.enemies_positions[0]
        elif self.color == ENEMY_COLORS_LIST[1]:
            return self.app.enemies_positions[1]
        elif self.color == ENEMY_COLORS_LIST[2]:
            return self.app.enemies_positions[2]
        elif self.color == ENEMY_COLORS_LIST[3]:
            return self.app.enemies_positions[3]
