#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random,time
from led_setup import Led_Setup
from PIL import Image, ImageDraw
#####################################################################
#円描画モード
#インスタンス生成の必要はありません
# CircleAnime.run(led_Setupインスタンス)
#####################################################################

class CircleAnime(object):

    @staticmethod
    def run(led):
        #円半径取得
        r = led._height // 2 #切り捨て除算
        #イメージ格納用
        circleimgs = []
        i = 0

        #最大円半径（半径1.5倍）
        max_rad = int(r * 1.5)

        #円描画用関数
        def drawcircle():
            imgs = []
            #色
            col1 = (random.randint(0,255),random.randint(0,255),random.randint(0,255))

            for i in range(0,max_rad):
                im = Image.new('RGB',(led._height,led._height),(0,0,0))
                draw = ImageDraw.Draw(im)
                draw.ellipse((r - i,r - i,r + i,r + i),fill = col1)
                im.point(lambda x: x * 0.8)
                imgs.append(im)

            for i in range(0,max_rad):
                im = Image.new('RGB',(led._height,led._height),col1)
                draw = ImageDraw.Draw(im)
                draw.ellipse((r - i,r - i,r + i,r + i),fill = (0,0,0))
                im.point(lambda x: x * 0.8)
                imgs.append(im)

            return imgs

        circleimgs = drawcircle()

        while led.stopper:

            led.canvas.Clear()

            for x in range(0,led._width,led._height):
                led.canvas.SetImage(circleimgs[i],x,0)

            led.canvas = led.matrix.SwapOnVSync(led.canvas)

            i += 1

            if i >= max_rad * 2:
                i = 0
                circleimgs = drawcircle()
            time.sleep(0.015)

        #終了時ブラックスクリーンに
        led.canvas.Clear()
        led.canvas = led.matrix.SwapOnVSync(led.canvas)

#テスト実行用
if __name__ == '__main__':
    print('Mode: CircleAnime')
    #引数に 32x32枚数,明るさ設定可 設定する際は両方書くこと
    # Ex: led = Led_Setup(4,50)
    led = Led_Setup()
    led.stopper = True
    CircleAnime.run(led)
