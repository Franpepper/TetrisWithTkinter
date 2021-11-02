from pygame import mixer

class Audio:
    def __init__(self): 
        mixer.init()
        self.gameover_sound = mixer.Sound('src/audio/gameover.mp3')
        self.land_sound = mixer.Sound('src/audio/land.mp3')
        self.line_sound = mixer.Sound('src/audio/line.mp3')
        self.move_sound = mixer.Sound('src/audio/move.mp3')
        self.rotate_sound = mixer.Sound('src/audio/rotate.mp3')
        self.tetris_sound = mixer.Sound('src/audio/tetris.mp3')
        self.level_sound = mixer.Sound('src/audio/level.mp3')
        self.pause_sound = mixer.Sound('src/audio/pause.mp3')

    def play_music(self):
        
        mixer.music.load('src/audio/theme.mp3')
        mixer.music.play(-1)
        mixer.music.set_volume(0.1)
    
    def stop_music(self):
        
        mixer.music.stop()
   
    def play_sound(self, sound):
        
        mixer.Sound.play(sound)
    