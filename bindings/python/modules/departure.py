#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from led_setup import Led_Setup
from rgbmatrix import graphics

#####################################################################
#発車標表示メソッド
#静的なので、インスタンス生成の必要はありません
# Departure.run(Led_Setupインスタンス)
#####################################################################

class Departure(object):
    # 発車標メソッド
    @staticmethod
    def run(led):
        #画像サイズ取得
        img_width,img_height = led.atos.size

        #発車標用座標
        x = 0
        y = -32
        #発車標表示時間
        wait1 = 4
        wait2 = 3

        #ループカウント用
        count = 0
        waiting = 0

        #団体表示（初回用）
        while count <= 2 and led.stopper:
            while led.stopper and waiting <= wait1:
                led.canvas.Clear()
                led.canvas.SetImage(led.atos,x,0)
                led.canvas = led.matrix.SwapOnVSync(led.canvas)
                time.sleep(0.1)
                waiting += 0.1

            waiting = 0

            while led.stopper and waiting <= wait2:
                led.canvas.Clear()
                led.canvas.SetImage(led.atos_en,x,0)
                led.canvas = led.matrix.SwapOnVSync(led.canvas)
                time.sleep(0.1)
                waiting += 0.1

            count += 1
            waiting = 0

        #ループカウントリセット
        count = 1
        waiting = 0

        # メインループ
        while led.stopper:
            # 2回繰り返し表示(count) waitingは待機
            while led.stopper and count <= 2:
                while led.stopper and waiting <= wait1:
                    led.canvas.Clear()
                    led.canvas.SetImage(led.atos,x,y)
                    led.canvas = led.matrix.SwapOnVSync(led.canvas)
                    time.sleep(0.1)
                    waiting += 0.1

                waiting = 0

                while led.stopper and waiting <= wait2:
                    led.canvas.Clear()
                    led.canvas.SetImage(led.atos_en,x,y)
                    led.canvas = led.matrix.SwapOnVSync(led.canvas)
                    time.sleep(0.1)
                    waiting += 0.1

                count += 1
                waiting = 0

            #ループカウントリセット
            waiting = 0
            count = 1
            y -= 16

            #終端判定・リスト・団体表示
            if y <= -img_height:
                while count <= 2 and led.stopper:
                    while led.stopper and waiting <= wait1:
                        led.canvas.Clear()
                        led.canvas.SetImage(led.atos,x,0)
                        led.canvas = led.matrix.SwapOnVSync(led.canvas)
                        time.sleep(0.1)
                        waiting += 0.1

                    waiting = 0

                    while led.stopper and waiting <= wait2:
                        led.canvas.Clear()
                        led.canvas.SetImage(led.atos_en,x,0)
                        led.canvas = led.matrix.SwapOnVSync(led.canvas)
                        time.sleep(0.1)
                        waiting += 0.1

                    count += 1
                    waiting = 0

                #ループカウント・座標リセット
                waiting = 0
                count = 1
                y = -32

        led.canvas.Clear()
        led.canvas = led.matrix.SwapOnVSync(led.canvas)

#直接実行（実行テスト用）
if __name__ == '__main__':
    print('Mode: 発車標表示')
    #引数に 32x32枚数,明るさ設定可 設定する際は両方書くこと
    # Ex: led = Led_Setup(4,50)
    led = Led_Setup(4,50)

    #ループするように
    led.stopper = True
    Departure.run(led)
