#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os,time

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image

#####################################################################
#ledセットアップ用モジュール・クラス
#このファイルは実行できません
#引数に32x32パネルの枚数、明るさ(0~100)を設定しています
#インスタンス生成時に引数に設定してください(chain,bright)  Ex: led = Led_Setup(4,50)
#デフォルト chain 4 bright 50
#フォント:MSゴシック,LEDサイズ(int),数色用意
#マイクロ秒換算メソッド付き
#モードメソッドの第一引数にこのインスタンスを必ず設定してください
#モードメソッド引数にある'led'は、このクラスのインスタンスを指しています
#####################################################################

class Led_Setup(object):
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

        #Load Font
        self.gothic = graphics.Font()
        self.gothic.LoadFont("Resources/Gothic-16.bdf")
        #明朝は現時点で未使用なので、コメントアウト
        """
        self.mincho = graphics.Font()
        self.mincho.LoadFont("Resources/Mincho-16.bdf")
        """

        #Load images
        self.icon_twitter = Image.open("Resources/icon_twitter.ppm").convert('RGB')
        self.icon_twitter_width,self.icon_twitter_height = self.icon_twitter.size

        self.atos = Image.open("Resources/atos.png").convert('RGB')
        self.atos_en = Image.open("Resources/atos-en.png").convert('RGB')

        #LED長さ
        self._width = self.canvas.width
        self._height = self.canvas.height

        #Colors
        self.orange = graphics.Color(255, 110, 0)
        self.blue = graphics.Color(0, 220, 255)
        self.white = graphics.Color(255, 255, 255)
        self.red = graphics.Color(255, 0, 0)
        self.green = graphics.Color(0,255,0)
        self.peach = graphics.Color(255, 0, 255)

        #ループ制御用変数
        self.stopper = False

    #マイクロ秒換算関数
    def usleep(self, value):
        time.sleep(value / 1000000.0)
