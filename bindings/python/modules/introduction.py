#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from led_setup import Led_Setup
from rgbmatrix import graphics

#####################################################################
#メッセージ表示メソッド
#静的なので、インスタンス生成の必要はありません
# Introduction.run(Led_Setupインスタンス)
#####################################################################

class Introduction(object):
    #DJリストメソッド
    @staticmethod
    def run(led):
        continuum = 0
        def rainbow(continuum):
            continuum %= 3 * 255

            red = 0
            green = 0
            blue = 0

            if continuum <= 255:
                c = continuum
                blue = 255 - c
                red = c
            elif continuum > 255 and continuum <= 511:
                c = continuum - 256
                red = 255 - c
                green = c
            else:
                c = continuum - 512
                green = 255 - c
                blue = c

            return red,green,blue

        #リスト表示内容
        text1 = u'音楽研究同好会'
        text2 = u'音楽が好きな人は、音研に入ろう！　DJしてみない？作曲してみない？　音研はいいぞ！！！'
        text3 = u'デザイン同好会'
        text4 = u'＜想像を創造しよう！＞　自分のアイディアを形にしたいと思ったら！デザイン同好会へ！レッツエンジョイ高専ライフ！'
        text5 = u'LEDJ同好会（非公式）'
        text6 = u'LEDマンになってみない？　DJイベントをLEDで盛り上げよう！'

        out1 = text1
        out2 = text2

        #リスト表示用座標
        pos1 = led._width

        #ループカウント用
        count = 0
        continuum = 0

        #リスト表示（初回用）
        while led.stopper:
            led.canvas.Clear()
            red,green,blue = rainbow(continuum)
            graphics.DrawText(led.canvas, led.gothic, 15, 15, graphics.Color(red,green,blue), out1)
            len = graphics.DrawText(led.canvas, led.gothic, pos1, 30, led.white, out2)
            pos1 -= 1

            if (pos1 + len < 0):
                pos1 = led._width
                if count % 3 == 0:
                    out1 = text3
                    out2 = text4
                elif count % 3 == 1:
                    out1 = text5
                    out2 = text6
                else:
                    out1 = text1
                    out2 = text2

                count += 1

            continuum += 1

            time.sleep(0.01)
            led.canvas = led.matrix.SwapOnVSync(led.canvas)

        led.canvas.Clear()
        led.canvas = led.matrix.SwapOnVSync(led.canvas)

#直接実行（実行テスト用）
if __name__ == '__main__':
    print('Mode: 紹介メッセージ表示')
    #引数に 32x32枚数,明るさ設定可 設定する際は両方書くこと
    # Ex: led = Led_Setup(4,50)
    led = Led_Setup(4,50)

    #ループするように
    led.stopper = True
    Introduction.run(led)
