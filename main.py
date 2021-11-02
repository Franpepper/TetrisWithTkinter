# Tetris

from pygame.mixer import pause
import game
import tkinter as tk
import audio

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.tetris = game.Tetris()
        self.audio = audio.Audio()
        self.pack()
        self.pause = False
        self.game_window()
        self.game_clock()
        self.onetime = False
        

    
    def game_clock(self):
        if self.pause is False:
            self.tetris.move(1, 0) 
            self.updates()
            self.master.after(int(1000*(0.66**self.tetris.level)), self.game_clock)
        elif self.pause is True:
            self.pause_label = tk.Label(self, text="PAUSA", font=("Arial", 20), fg="red")
    
    def set_pause(self):
        if self.pause is False:
            self.pause = True
        elif self.pause is True:
            self.pause = False
            self.game_clock()

    
    def game_window(self):
        self.audio.play_music() 
        self.winfo_toplevel().title("Tetris") 
        self.canvas = tk.Canvas(self, height=self.tetris.SIZE * self.tetris.HEIGHT,             
                                width=self.tetris.SIZE * self.tetris.WIDTH, bg='white', bd=0)                                        
        self.canvas.bind('<Left>', lambda _: (self.tetris.move(0, -1),self.audio.play_sound(self.audio.move_sound), self.updates())) 
        self.canvas.bind('<Right>', lambda _: (self.tetris.move(0, 1),self.audio.play_sound(self.audio.move_sound), self.updates())) 
        self.canvas.bind('<Down>', lambda _: (self.tetris.move(1, 0), self.updates()))                                               
        self.canvas.bind('<space>', lambda _: (self.tetris.rotate(),self.audio.play_sound(self.audio.rotate_sound), self.updates())) 
        self.canvas.bind('<Escape>', lambda _: self.master.destroy())                                                                                                            
        self.canvas.bind('<p>', lambda _: (self.set_pause(), self.audio.play_sound(self.audio.pause_sound),self.updates()))                                                                         #Pausar juego
        self.canvas.focus_set()
        self.rectangles = [
            self.canvas.create_rectangle(c * self.tetris.SIZE, r * self.tetris.SIZE, (c + 1) * self.tetris.SIZE, (r + 1) * self.tetris.SIZE)
            for r in range(self.tetris.HEIGHT) for c in range(self.tetris.WIDTH)
        ]
        self.canvas.pack(side="left", expand=True, fill="both")
        self.status_msg = tk.Label(self, anchor='w', width=11, font=("Tahoma", 20), justify='left') #Muestra Puntaje y Nivel
        self.status_msg.pack(side="top")
        self.game_over_msg = tk.Label(self, anchor='w', width=11, font=("Tahoma",20), fg="red", justify='left') #Muestra mensaje de Game Over
        self.game_over_msg.pack(side="top")
        

    def updates(self):
        for i, _id in enumerate(self.rectangles):
            color_num = self.tetris.get_color(i // self.tetris.WIDTH, i % self.tetris.WIDTH)
            self.canvas.itemconfig(_id, fill=self.tetris.COLORS[color_num])
        
        self.status_msg['text'] = "Score: {}\nLevel: {}\n\nP - Pause\nESC - Exit\n".format(self.tetris.score, self.tetris.level)
        self.game_over_msg['text'] = "GAME OVER\n\n\nPress\nSpace\nto restart" if self.tetris.game_over else ""
        if self.tetris.game_over == True: 
            while self.tetris.reset is False:
                self.audio.stop_music()
                self.audio.play_sound(self.audio.gameover_sound)
                self.tetris.reset = True
        
root = tk.Tk()
root.iconbitmap('src/image/icon.ico')
appl = App(master=root)
appl.mainloop()
