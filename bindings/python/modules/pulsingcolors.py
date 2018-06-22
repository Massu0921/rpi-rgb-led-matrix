#!/usr/bin/env python
# -*- coding: utf-8 -*-

from led_setup import Led_Setup

#####################################################################
#色変化モード
#インスタンス生成の必要はありません
# PulsingColors.run(led_Setupインスタンス)
#####################################################################

class PulsingColors(object):

    @staticmethod
    def run(led):
        continuum = 0

        #ループ開始
        while led.stopper:
            led.usleep(5 * 1000)
            continuum += 1
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

            led.canvas.Fill(red, green, blue)
            led.canvas = led.matrix.SwapOnVSync(led.canvas)

        #ループ終了時
        led.canvas.Clear()
        led.canvas = led.matrix.SwapOnVSync(led.canvas)

#直接実行時（テスト）
if __name__ == '__main__':
    print('Mode: PulsingColors')
    #引数に 32x32枚数,明るさ設定可 設定する際は両方書くこと
    # Ex: led = Led_Setup(4,50)
    led = Led_Setup()
    led.stopper = True
    PulsingColors.run(led)
