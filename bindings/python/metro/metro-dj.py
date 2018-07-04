#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os,time,threading
import Tkinter as TK
from datetime import datetime as dt

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '../'))
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

class MetroDJ(object):
    #インスタンス生成時に実行
    def __init__(self,chain=4,bright=50): #デフォルト設定（引数なしの場合）
        #Options
        self.options = RGBMatrixOptions()
        self.options.rows = 32
        self.options.chain_length = chain
        self.options.parallel = 1
        self.options.hardware_mapping = 'adafruit-hat-pwm'
        self.options.brightness = bright
        self.options.show_refresh_rate = 0
        self.matrix = RGBMatrix(options=self.options)
        self.canvas = self.matrix.CreateFrameCanvas()

        # フォント読み込み
        self.clcfont = graphics.Font()
        self.clcfont.LoadFont("Resources/Metroclock.bdf")
        self.gothic = graphics.Font()
        self.gothic.LoadFont("Resources/Gothic-16.bdf")

        # セットリストのテキストファイル読み込み
        with open("Resources/SetList.txt") as sl:
            self.setlist = sl.readlines()
        for i in range(len(self.setlist)):
            self.setlist[i] = self.setlist[i].replace('\n','').replace('	','　')
            self.setlist[i] = self.setlist[i].decode('utf-8')

        # リスト最後に空白を追加
        self.setlist.append('')
        # リスト長を取得 (-1)
        self.setlist_len = len(self.setlist) - 1

        #print(self.setlist)
        #LED長さ
        self._width = self.canvas.width
        self._height = self.canvas.height

        #Colors
        self.orange = graphics.Color(255, 110, 0)
        self.blue = graphics.Color(0, 220, 255)
        self.white = graphics.Color(255, 255, 255)
        self.red = graphics.Color(255, 0, 0)
        self.green = graphics.Color(0,255,0)

        #座標用変数
        self.low_x = self._width

        # 曲番号用変数
        self.number = self.setlist_len

    # 上段
    def up_led(self):
        hour = dt.now().strftime("%H")
        minute = dt.now().strftime("%M")
        sec = dt.now().strftime("%S")

        if int(sec) % 2 == 0:
            self.up_text = hour + ':' + minute
        else:
            self.up_text = hour + ' ' + minute

    # 下段
    def low_led(self):
        # 例外処理
        try:
            self.low_text = self.setlist[self.number]
        except:
            self.number = self.setlist_len

    # 表示部
    def run(self):
        while True:
            self.canvas.Clear()

            self.up_led()
            self.low_led()

            graphics.DrawText(self.canvas,self.clcfont,0,16,self.white,self.up_text)
            len = graphics.DrawText(self.canvas,self.gothic,self.low_x,30,self.blue,self.low_text)
            if (self.low_x + len < 0):
                self.low_x = self._width

            self.canvas = self.matrix.SwapOnVSync(self.canvas)
            self.low_x -= 1

            # スクロール速度
            time.sleep(0.02)

class GUI(TK.Frame,MetroDJ):
    def __init__(self,master=None):
        # エラー回避のため先にGUIを作成
        TK.Frame.__init__(self,master)
        MetroDJ.__init__(self)

        self.master.title('Metro-LEDJ')
        fontsize = 25
        dx = 20
        dy = 20

        th_led = threading.Thread(target = self.run)
        th_led.setDaemon(True)
        th_led.start()

        self.bt_next = TK.Button(text=u' Next ▶▶ ',font=("",fontsize),bg='Khaki',command=self.add)
        self.bt_next.grid(row=0,column=0,columnspan=2,padx=dx,pady=dy,sticky=TK.W + TK.E)

        self.bt_back = TK.Button(text=u' Back ◀◀ ',font=("",fontsize),bg='cyan',command=self.sub)
        self.bt_back.grid(row=0,column=2,columnspan=2,padx=dx,pady=dy,sticky=TK.W + TK.E)

        self.bt_start = TK.Button(text=u' Start (Reset) ',font=("",fontsize),bg='green2',command=self.start)
        self.bt_start.grid(row=1,column=0,columnspan=2,padx=dx,pady=20,sticky=TK.W + TK.E)

        self.bt_end = TK.Button(text=u' End Message ',font=("",fontsize),bg='yellow2',command=self.end)
        self.bt_end.grid(row=1,column=2,columnspan=2,padx=dx,pady=20,sticky=TK.W + TK.E)

        #self.bt_pause = TK.Button(text=u' Pause ',font=("",fontsize),bg='magenta2',command=self.pause)
        #self.bt_pause.grid(row=2,column=0,columnspan=2,padx=dx,pady=20,sticky=TK.W + TK.E)

        self.bt_stop = TK.Button(text=u' Stop ',font=("",fontsize),bg='IndianRed1',command=self.stop)
        self.bt_stop.grid(row=2,column=2,columnspan=2,padx=dx,pady=20,sticky=TK.W + TK.E)

        self.bt_next.configure(state=TK.DISABLED)
        self.bt_back.configure(state=TK.DISABLED)
        self.bt_start.configure(state=TK.NORMAL)
        self.bt_end.configure(state=TK.NORMAL)
        #self.bt_pause.configure(state=TK.NORMAL)
        self.bt_stop.configure(state=TK.DISABLED)

    # 曲番号加算・減算用メソッド
    def add(self):
        self.number += 1
        self.low_x = self._width

        if self.number > self.setlist_len - 1:
            self.bt_next.configure(state=TK.DISABLED)
        self.bt_back.configure(state=TK.NORMAL)
        self.bt_start.configure(state=TK.NORMAL)
        self.bt_end.configure(state=TK.NORMAL)
        #self.bt_pause.configure(state=TK.DISABLED)
        self.bt_stop.configure(state=TK.NORMAL)

    def sub(self):
        self.number -= 1
        self.low_x = self._width

        self.bt_next.configure(state=TK.NORMAL)
        if self.number <= 0:
            self.bt_back.configure(state=TK.DISABLED)
        self.bt_start.configure(state=TK.NORMAL)
        self.bt_end.configure(state=TK.NORMAL)
        #self.bt_pause.configure(state=TK.DISABLED)
        self.bt_stop.configure(state=TK.NORMAL)

    def start(self):
        self.number = 0
        self.low_x = self._width

        self.bt_next.configure(state=TK.NORMAL)
        self.bt_back.configure(state=TK.DISABLED)
        self.bt_start.configure(state=TK.DISABLED)
        self.bt_end.configure(state=TK.NORMAL)
        #self.bt_pause.configure(state=TK.DISABLED)
        self.bt_stop.configure(state=TK.NORMAL)

    def end(self):
        self.number = self.setlist_len - 1
        self.low_x = self._width

        self.bt_next.configure(state=TK.DISABLED)
        self.bt_back.configure(state=TK.NORMAL)
        self.bt_start.configure(state=TK.NORMAL)
        self.bt_end.configure(state=TK.DISABLED)
        #self.bt_pause.configure(state=TK.DISABLED)
        self.bt_stop.configure(state=TK.NORMAL)

    def stop(self):
        self.number = self.setlist_len
        self.low_x = self._width

        self.bt_next.configure(state=TK.DISABLED)
        self.bt_back.configure(state=TK.DISABLED)
        self.bt_start.configure(state=TK.NORMAL)
        self.bt_end.configure(state=TK.NORMAL)
        #self.bt_pause.configure(state=TK.NORMAL)
        self.bt_stop.configure(state=TK.DISABLED)

if __name__ == '__main__':
    gui = GUI()
    gui.mainloop()
