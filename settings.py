from pygame.math import Vector2 as vec
#screen settings
width, height = 448, 576
ROWS = 31
COLUMNS = 28

top_bottom_buffer = 48
down_bottom_buffer = 32
maze_width, maze_height = width, height-top_bottom_buffer-down_bottom_buffer


fps = 200
#color settings
WHITE = (250, 250, 250)
BLACK = (0, 0, 0)
RED = (254, 35, 28)
BLUE= (17, 227, 233)
PINK = (251, 166, 211)
ORANGE = (255, 193, 131)
grey = (100, 100, 100)
ORANGE_FOR_COINS = (254, 172, 28)
RED_FOR_LOSER = (240, 30, 5)
BLUE_FOR_WINNER = (119, 240, 240)
YELLOW_FOR_MENU = (170, 132, 58)
ENEMY_COLORS_LIST = [BLUE, PINK, ORANGE, RED]
player_color = (254, 254, 28)
#enemy position settings
START_ENEMY_POSITIONS = [vec(13, 15), vec(14, 15), vec(15, 15), vec(16, 15)]
#coins count
coins_count = 287
#rules
RULES = "Poruszaj się żółtą kulką (Pac-Manem),\njedz małe kulki i unikaj dużych kulek(duszków),\ntrafienie na duszka oznacza utratę jednego z trzech żyć.\nPo utracie wszystkich żyć przegrywasz.\nGra kończy się zwycięstwem po zjedzeniu wszystkich małych kulek\nzanim stracisz życia."
AUTHOR = "Aleksandra Janczewska"