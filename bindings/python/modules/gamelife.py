#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
#from numba.decorators import jit
from led_setup import Led_Setup

#####################################################################
#目に悪いモード
#インスタンス生成の必要はありません
# GameLife.run(led_Setupインスタンス)
#動作遅いです、そのうち改良します
#####################################################################

class GameLife(object):

    #@jit
    @staticmethod
    def run(led):
        # LED長さ
        width_ = led._width
        height_ = led._height

        torus_ = True

        #遅延用
        #delay_ms_ = 500

        # Allocate memory
        values_ = width_ * [0]
        for x in range(0,width_):
            values_[x] = height_ * [0]

        newValues_ = width_ *[0]
        for x in range(0,width_):
            newValues_[x] = height_ * [0]

        # Init values randomly
        for x in range(0,width_):
            for y in range(0,height_):
                values_[x][y] = random.randint(0,1)

        r_ = random.randint(0,254)
        g_ = random.randint(0,254)
        b_ = random.randint(0,254)

        if r_<150 and g_<150 and b_<150:
            c = random.randint(0,2)
            if c == 0:
                r_ = 200
            elif c == 1:
                g_ = 200
            elif c == 2:
                b_ == 200

        #演算用関数
        def updateValues():
            # Copy values to newValues
            for x in range(0,width_):
                for y in range(0,height_):
                    newValues_[x][y] = values_[x][y]

            # update newValues based on values
            for x in range(0,width_):
                for y in range(0,height_):
                    num = numAliveNeighbours(x, y)
                    if values_[x][y]:
                        # cell is alive
                        if num < 2 or num > 3:
                            newValues_[x][y] = 0

                    else:
                        #cell is dead
                        if num == 3:
                            newValues_[x][y] = 1

            # copy newValues to values
            for x in range(0, width_):
                for y in range(0, height_):
                    values_[x][y] = newValues_[x][y]


        def numAliveNeighbours(x, y):
            num = 0

            if torus_:
                # Edges are connected (torus)
                num += values_[(x-1+width_)%width_][(y-1+height_)%height_]
                num += values_[(x-1+width_)%width_][y                    ]
                num += values_[(x-1+width_)%width_][(y+1        )%height_]
                num += values_[(x+1       )%width_][(y-1+height_)%height_]
                num += values_[(x+1       )%width_][y                    ]
                num += values_[(x+1       )%width_][(y+1        )%height_]
                num += values_[x                  ][(y-1+height_)%height_]
                num += values_[x                  ][(y+1        )%height_]

            else:
                # Edges are not connected (no torus)
                if x > 0:
                    if y > 0:
                        num += values_[x-1][y-1]
                    if y < height_ - 1:
                        num += values_[x-1][y+1]
                    num += values_[x-1][y]

                if x < width_ - 1:
                    if y > 0:
                        num += values_[x+1][y-1]
                    if y < 31:
                        num += values_[x+1][y+1]
                    num += values_[x+1][y]

                if y > 0:
                    num += values_[x][y-1]
                if y < height_ - 1:
                    num += values_[x][y+1]

            return num

        #メインループ
        while led.stopper:
            #リスト更新
            updateValues()

            #更新
            for x in range(0, width_):
                 for y in range(0,height_):
                    if values_[x][y]:
                        led.canvas.SetPixel(x, y, r_, g_, b_)

                    else:
                        led.canvas.SetPixel(x, y, 0, 0, 0)

            led.canvas = led.matrix.SwapOnVSync(led.canvas)
            #led.usleep(delay_ms_ * 1000)

        led.canvas.Clear()
        led.canvas = led.matrix.SwapOnVSync(led.canvas)


#直接実行時（テスト）
if __name__ == '__main__':
    print('Mode: GameLife')
    #引数に 32x32枚数,明るさ設定可 設定する際は両方書くこと
    # Ex: led = Led_Setup(4,50)
    led = Led_Setup()
    led.stopper = True
    GameLife.run(led)
