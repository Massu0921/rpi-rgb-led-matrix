#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math,random
from led_setup import Led_Setup

#####################################################################
#スペクトルアナライザ風モード（非同期）
# c++ -> Python
#インスタンス生成の必要はありません
# VolumeBars.run(led_Setupインスタンス)
#実行速度遅いので、C++より遅延を短くしています
#####################################################################

class VolumeBars(object):

    @staticmethod
    def run(led):

        #遅延用
        delay_ms_ = 90

        #バー(幅2)の数
        numBars_ = led._width / 2

        width = led._width
        height_ = led._height

        #バー長（横）
        barWidth_ = width / numBars_

        barHeights_ = numBars_ * [0]
        barMeans_ = numBars_ * [0]
        barFreqs_ = numBars_ * [0]

        #バー色分け
        heightGreen_  = height_ * 4 / 12
        heightYellow_ = height_ * 8 / 12
        heightOrange_ = height_ * 10 / 12
        heightRed_    = height_ * 12 / 12

        #カウント用？
        t_ = 0

        # Array of possible bar means ？？？
        numMeans = 10
        means = [1,2,3,4,5,6,7,8,16,32]
        for i in range(numMeans):
            means[i] = height_ - means[i] * height_ / 8

        # Initialize bar means randomly
        for i in range(numBars_):
            barMeans_[i] = random.randint(0,9)
            barFreqs_[i] = 1 << random.randint(0,2)

        #描画用関数
        def drawBarRow(canvas,bar,y,r,g,b):
            for x in range(bar*barWidth_,(bar+1)*barWidth_):
                canvas.SetPixel(x,height_ -1-y,r,g,b)

        #ループ開始
        while led.stopper:
            if t_ % 8 == 0:
                # Change the means
                for i in range(numBars_):
                    barMeans_[i] += random.randint(0,2) - 1
                    if barMeans_[i] >= numMeans:
                        barMeans_[i] = numMeans - 1
                    if barMeans_[i] < 0:
                        barMeans_[i] = 0

            # Update bar heights
            t_ += 1

            #バーの伸びの設定
            for i in range(numBars_):
                barHeights_[i] = (height_ - means[barMeans_[i]]) * math.sin(0.1*t_*barFreqs_[i]) + means[barMeans_[i]]
                if barHeights_[i] < height_ / 8:
                    barHeights_[i] = random.randint(1,height_ / 8)

            #バーの描画（高さにより色変更）
            for i in range(numBars_):
                for y in range(int(barHeights_[i]) + random.randint(0,1)):
                    if y < heightGreen_:
                        drawBarRow(led.canvas,i, y, 0, 200, 0)
                    elif y < heightYellow_:
                        drawBarRow(led.canvas,i, y, 150, 150, 0)
                    elif y < heightOrange_:
                        drawBarRow(led.canvas,i, y, 250, 100, 0)
                    else:
                        drawBarRow(led.canvas,i, y, 200, 0, 0)

                    #保持用
                    kp_y = y

                for y in range(kp_y,height_):
                    drawBarRow(led.canvas,i, y, 0, 0, 0)

            #表示・遅延
            led.canvas = led.matrix.SwapOnVSync(led.canvas)
            led.usleep(delay_ms_ * 100)

        #終了時初期化
        led.canvas.Clear()
        led.canvas = led.matrix.SwapOnVSync(led.canvas)

#テスト実行用
if __name__ == '__main__':
    print('Mode: VolumeBars')
    #引数に 32x32枚数,明るさ設定可 設定する際は両方書くこと
    # Ex: led = Led_Setup(4,50)
    led = Led_Setup()
    led.stopper = True
    VolumeBars.run(led)
