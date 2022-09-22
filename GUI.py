from tkinter import *
from tkinter.messagebox import *
from Player import Player, Point
from Weiqi import Stone_liberty, GameState, Action, Board
from PIL import Image, ImageTk
import Scoring
import os
import tkinter as tk
print(os.getcwd())
class MyApp(tk.Tk): 
    def __init__(self):
        super(MyApp, self).__init__()
        self.board_color = "#CDBA96"
        self.board_grid = 19
        self.board_grid_size = 40
        self.board_edge_left = 20
        self.board_edge_right = (self.board_grid - 1) * 40 + 20
        self.xin_size = self.board_grid_size / 10
        self.stop = True
        self.mouse_last = None
        self.present = 1 # 黑：1，白：2
        self.title("Weiqi")
        self.geometry("{}x{}+{}+{}".format(900, 900, 300, 100))
        self.resizable(width=0, height=0)

        photoB= (Image.open('./fig/black.png'))
        photoW= (Image.open('./fig/white.png'))
        resized_photoB= photoB.resize((40,40), Image.ANTIALIAS)
        resized_photoW= photoW.resize((40,40), Image.ANTIALIAS)
        self.photoB=ImageTk.PhotoImage(resized_photoB)
        self.photoW=ImageTk.PhotoImage(resized_photoW)
        self.photoWB_list=['', self.photoB, self.photoW]

        self.set_widgets()

        self.startButton = Button(self,text='開始',command=self.start)
        self.startButton.place(x=60,y=800)
        self.startButton = Button(self,text='重來',command=self.restart)
        self.startButton.place(x=160,y=800)
        self.passButton = Button(self,text='虛手',command=self.pass_move)
        self.passButton.place(x=560,y=800)
        self.passButton = Button(self,text='投降',command=self.resign)
        self.passButton.place(x=660,y=800)
        self.scroingButton = Button(self,text='數地',command=self.scroing)
        self.scroingButton.place(x=760,y=800)

        self.board.bind('<Motion>',self.shadow)
        self.copygrid = set()
        self.board.bind('<Button-1>',self.getDown)

    def run(self):
        self.mainloop()

    def set_widgets(self):
        self.board = tk.Canvas(self, width=self.board_edge_right + 40, height=self.board_edge_right + 40, bg=self.board_color)
        self.board.pack()
        self.board2info = [-1] * (self.board_grid + 2) + [[0, -1][i in [0, (self.board_grid + 1)]] \
            for i in range((self.board_grid + 2))] * self.board_grid + [-1] * (self.board_grid + 2)
        self.tag2pos = {}
        self.z2tag = {}
        self.numstr = [str(i) for i in range(1,self.board_grid + 1)]
        self.kanstr = ['一','二','三','四','五','六','七','八','九','十','十一','十二','十三','十四','十五','十六','十七','十八','十九']
        for i, y in zip(self.kanstr, range(self.board_edge_left, self.board_edge_right, self.board_grid_size)):
            for j, x in zip(self.numstr[::-1], range(self.board_edge_left, self.board_edge_right, self.board_grid_size)):
                pos = (x, y, x + self.board_grid_size, y + self.board_grid_size)
                tag = (j , i)
                self.tag2pos[tag] = pos[:2]
                self.board.create_rectangle(*pos, fill=self.board_color, tags=tag)
                self.z2tag[self.z_coordinate(tag)] = tag
        for i, y in zip(self.kanstr, range(self.board_edge_left, self.board_edge_right, self.board_grid_size)):
            for j, x in zip(self.numstr, range(self.board_edge_left, self.board_edge_right, self.board_grid_size)):
                if ((j == str(4) or j == str(10) or j == str(self.board_grid - 3)) and (i == '四' or i == '十' or i == '十六')):
                    self.board.create_oval(y - self.xin_size, x - self.xin_size, y + self.xin_size, x + self.xin_size, fill="black")
        #self.get_board_info()

    def z_coordinate(self, tag):
        x, y = self.numstr[::-1].index(tag[0])+1, self.kanstr.index(tag[1])+1
        return y * (self.board_grid + 2) + x

    def get_board_info(self, a=None, b=None):
        tags = "" if a is None else "\n{} -> {}".format(a, b)
        board_format = " {:2d} " * (self.board_grid + 2)
        print(tags, *[board_format.format(*self.board2info[i:i + (self.board_grid + 2)]) \
                                    for i in range(0, (self.board_grid + 2) * (self.board_grid + 2), self.board_grid + 2)], sep='\n')

    def start(self):
        self.stop=False
        self.game = GameState.new_game(19)

    def restart(self):
        self.stop=False
        self.board.delete('now')
        for reset_board in self.game.board._grid.keys():
            self.board.delete('position'+str(reset_board.row)+str(reset_board.col))
        self.present = 1
        self.game = GameState.new_game(19)

    def pass_move(self):
        self.game = self.game.apply_move(Action.pass_move())
        if self.present == 2:
            self.present = 1
        else:
            self.present = 2

    def resign(self):
        self.game = self.game.apply_move(Action.resign())
        self.stop=True
        label = Label(self, text = str(self.game.next_player) + ' win')
        label.pack() 

    def scroing(self):
        result = Scoring.compute_game_result(self.game)
        label = Label(self, text = str(result.winner) +' + '+ str(result.winning_margin))
        label.pack() 

    def shadow(self, event):
        if not self.stop:
            if (0 < event.x < self.board_edge_right + self.board_grid_size / 2) and (0 < event.y < self.board_edge_right + self.board_grid_size / 2):
                shadow_x = round((event.x - self.board_edge_left) / self.board_grid_size) + 1
                shadow_y = round((event.y - self.board_edge_left) / self.board_grid_size) + 1
                if Point(shadow_x, shadow_y) not in self.game.board._grid.keys():
                    self.mouse = self.board.create_image(self.board_grid_size * shadow_x - self.board_grid_size / 2, 
                                                   self.board_grid_size * shadow_y - self.board_grid_size / 2, 
                                                   image=self.photoWB_list[self.present])
                self.board.addtag_withtag('image',self.mouse)
                if self.mouse_last!=None:
                    self.board.delete(self.mouse_last)
                self.mouse_last=self.mouse

    def getDown(self, event):
        if not self.stop:
            if (0 < event.x < self.board_edge_right + self.board_grid_size / 2) and (0 < event.y < self.board_edge_right + self.board_grid_size / 2):
                place_stone_x = round((event.x - self.board_edge_left) / self.board_grid_size) + 1
                place_stone_y = round((event.y - self.board_edge_left) / self.board_grid_size) + 1
                self.copygrid = self.game.board._grid
                if Point(place_stone_x, place_stone_y) not in self.copygrid.keys():
                    try:
                        self.game = self.game.apply_move(Action.move(Point(place_stone_x, place_stone_y)))
                        self.board.delete('now')
                        self.place_stone = self.board.create_image(self.board_grid_size * place_stone_x - self.board_grid_size / 2, 
                                                    self.board_grid_size * place_stone_y - self.board_grid_size / 2, 
                                                    image=self.photoWB_list[self.present])
                        self.board.create_rectangle(self.board_grid_size * place_stone_x - self.board_grid_size / 2 - self.xin_size, 
                                                    self.board_grid_size * place_stone_y - self.board_grid_size / 2 - self.xin_size, 
                                                    self.board_grid_size * place_stone_x - self.board_grid_size / 2 + self.xin_size, 
                                                    self.board_grid_size * place_stone_y - self.board_grid_size / 2 + self.xin_size, fill='red', tag='now')
                        self.board.addtag_withtag('position'+str(place_stone_x)+str(place_stone_y),self.place_stone)
                        #print(set(list(self.copygrid.keys())) | {Point(place_stone_x, place_stone_y)})
                        self.remove_stones = (set(list(self.copygrid.keys())) | {Point(place_stone_x, place_stone_y)}) - set(list(self.game.board._grid.keys()))
                        #print(self.remove_stones)
                        if len(self.remove_stones) != 0:
                            for remove_stone in self.remove_stones:
                                self.board.delete('position'+str(remove_stone.row)+str(remove_stone.col))
                        if self.present == 2:
                            self.present = 1
                        else:
                            self.present = 2
                    except:
                        pass
            
if __name__ == '__main__':
    app = MyApp()
    app.run()