#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os,time
from datetime import datetime as dt

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '../'))
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image


class Metroclock(object):
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

        # 時計用フォント読み込み
        self.clcfont = graphics.Font()
        self.clcfont.LoadFont("Resources/Metroclock.bdf")

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

    def run(self):
        while True:
            self.canvas.Clear()
            hour = dt.now().strftime("%H")
            minute = dt.now().strftime("%M")
            sec = dt.now().strftime("%S")

            if int(sec) % 2 == 0:
                text = hour + ':' + minute
            else:
                text = hour + ' ' + minute

            graphics.DrawText(self.canvas,self.clcfont,0,16,self.white,text)
            self.canvas = self.matrix.SwapOnVSync(self.canvas)
            time.sleep(0.1)

if __name__ == '__main__':
    metroclock = Metroclock()
    metroclock.run()
