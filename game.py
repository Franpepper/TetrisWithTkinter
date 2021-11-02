import random
import audio
from threading import Lock

class Tetris:
    
    WIDTH = 10
    HEIGHT = 20
    SIZE = 30
    COLORS = ['#000000', '#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#00FFFF', '#FF00FF']
    TETROMINOS = [
        [(0, 0), (0, 1), (1, 0), (1,1)], # O
        [(0, 0), (0, 1), (1, 1), (2,1)], # L
        [(0, 1), (1, 1), (2, 1), (2,0)], # J 
        [(0, 1), (1, 0), (1, 1), (2,0)], # Z
        [(0, 1), (1, 0), (1, 1), (2,1)], # T
        [(0, 0), (1, 0), (1, 1), (2,1)], # S
        [(0, 1), (1, 1), (2, 1), (3,1)], # I
    ]
    
    SCORE = (0, 25, 50, 100, 500)   
    

    def __init__(self):
        self.field = [[0 for c in range(Tetris.WIDTH)] for r in range(Tetris.HEIGHT)]
        self.score = 0
        self.level = 0
        self.control = 0
        self.total_lines = 0
        self.reset = False
        self.game_over = False
        self.locked = Lock()
        self.reset_tetromino()
        self.audio = audio.Audio()

    
    def reset_tetromino(self):
        self.tetromino = random.choice(Tetris.TETROMINOS)[:]
        self.tetromino_color = random.randint(1, len(Tetris.COLORS)-1)
        self.tetromino_offset = [-2, Tetris.WIDTH//2]
        self.game_over = any(not self.cell_free(r, c) for (r, c) in self.tetromino_coord())

    
    def tetromino_coord(self):
        return [(r+self.tetromino_offset[0], c + self.tetromino_offset[1]) for (r, c) in self.tetromino]

    
    def apply_tetromino(self):
        self.audio.play_sound(self.audio.land_sound)
        for (r, c) in self.tetromino_coord():
            self.field[r][c] = self.tetromino_color
        nfield = [row for row in self.field if any(tile == 0 for tile in row)] 
        lines = len(self.field)-len(nfield) 
        self.total_lines += lines
        if lines >= 1 and lines <= 3:
            self.audio.play_sound(self.audio.line_sound)
        elif lines == 4:
            self.audio.play_sound(self.audio.tetris_sound)
        self.field = [[0]*Tetris.WIDTH for x in range(lines)] + nfield
        self.score += Tetris.SCORE[lines] * (self.level + 1) 
        self.level = self.total_lines // 10 
        if self.control != self.level: 
            self.audio.play_sound(self.audio.level_sound)
            self.control = self.level

        self.reset_tetromino() 

    
    def get_color(self, r, c):
        return self.tetromino_color if (r, c) in self.tetromino_coord() else self.field[r][c]
    
    def cell_free(self, r, c):
        return r < Tetris.HEIGHT and 0 <= c < Tetris.WIDTH and (r < 0 or self.field[r][c] == 0)
   
    def move(self, dr, dc):
        with self.locked:
            if self.game_over:
                return 

            if all(self.cell_free(r + dr, c + dc) for (r, c) in self.tetromino_coord()):
                self.tetromino_offset = [self.tetromino_offset[0] + dr, self.tetromino_offset[1] + dc]
            elif dr == 1 and dc == 0:
                self.game_over = any(r < 0 for (r, c) in self.tetromino_coord())
                if not self.game_over:
                    self.apply_tetromino() 
    
    def rotate(self):
        with self.locked:
            if self.game_over: 
                self.__init__()
                self.audio.play_music()
                return
        
        ys = [r for (r, c) in self.tetromino]
        xs = [c for (r, c) in self.tetromino]
        size = max(max(ys) - min(ys), max(xs)-min(xs))
        rotated = [(c, size-r) for (r, c) in self.tetromino]
        wall_offset = self.tetromino_offset[:]
        tetromino_coord = [(r+wall_offset[0], c + wall_offset[1]) for (r,c) in rotated]
        min_x = min(c for r, c in tetromino_coord)
        max_x = max(c for r, c in tetromino_coord)
        max_y = max(r for r, c in tetromino_coord)
        wall_offset[1] -= min(0, min_x)
        wall_offset[1] += min(0, Tetris.WIDTH - (1 + max_x))
        wall_offset[0] += min(0, Tetris.HEIGHT - (1 + max_y))

        tetromino_coord = [(r+wall_offset[0], c+wall_offset[1]) for (r, c) in rotated]
        if all(self.cell_free(r, c) for (r, c) in tetromino_coord):
            self.tetromino, self.tetromino_offset = rotated, wall_offset
