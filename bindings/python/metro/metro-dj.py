#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os,time
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

        #LED長さ
        self._width = self.canvas.width
        self._height = self.canvas.height

        #Colors
        self.orange = graphics.Color(255, 110, 0)
        self.blue = graphics.Color(0, 220, 255)
        self.white = graphics.Color(255, 255, 255)
        self.red = graphics.Color(255, 0, 0)
        self.green = graphics.Color(0,255,0)

        #ループ制御用変数
        self.stopper = False

        # 曲番号用変数
        self.number = 0

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
        self.low_text = setlist[self.number]

    # 表示部
    def run(self):
        low_x = self._width
        while True:
            self.canvas.Clear()

            graphics.DrawText(self.canvas,self.clcfont,0,16,self.white,self.up_text)
            len = graphics.DrawText(self.canvas,self.gothic,low_x,32,self.blue,self.low_text)
            if (low_x + len < 0):
                low_x = self._width

            self.canvas = self.matrix.SwapOnVSync(self.canvas)
            time.sleep(0.02)

if __name__ == '__main__':
    metroclock = Metroclock()
    metroclock.run()
