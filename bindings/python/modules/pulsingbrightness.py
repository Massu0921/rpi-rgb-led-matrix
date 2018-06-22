#!/usr/bin/env python
# -*- coding: utf-8 -*-

from led_setup import Led_Setup

#####################################################################
#明るさ変化モード
#インスタンス生成の必要はありません
# PulsingBrightness.run(led_Setupインスタンス)
#####################################################################

class PulsingBrightness(object):

    @staticmethod
    def run(led):
        max_brightness = led.matrix.brightness
        count = 0
        c = 255

        #ループ開始
        while led.stopper:
            if led.matrix.brightness < 1:
                led.matrix.brightness = max_brightness
                count += 1
            else:
                led.matrix.brightness -= 1

            if count % 4 == 0:
                led.canvas.Fill(c, 0, 0)
            elif count % 4 == 1:
                led.canvas.Fill(0, c, 0)
            elif count % 4 == 2:
                led.canvas.Fill(0, 0, c)
            elif count % 4 == 3:
                led.canvas.Fill(c, c, c)

            led.canvas = led.matrix.SwapOnVSync(led.canvas)
            #マイクロ秒待機
            led.usleep(20 * 1000)

        #明るさを元に戻す
        led.matrix.brightness = max_brightness
        led.canvas.Clear()
        led.canvas = led.matrix.SwapOnVSync(led.canvas)

#直接実行時（テスト）
if __name__ == '__main__':
    print('Mode: PulsingBrightness')
    #引数に 32x32枚数,明るさ設定可 設定する際は両方書くこと
    # Ex: led = Led_Setup(4,50)
    led = Led_Setup()
    led.stopper = True
    PulsingBrightness.run(led)
