#!/usr/bin/env python
# -*- coding: utf-8 -*-

from led_setup import Led_Setup
from streaming import Streaming
from rgbmatrix import graphics
from PIL import Image
from urllib2 import *
import time,io

#####################################################################
#ツイート表示メソッド
#静的なので、インスタンス生成の必要はありません
# DisplayTweet.run(Led_Setupインスタンス,Streamingインスタンス)
#####################################################################

class DisplayTweet(object):
    @staticmethod
    def run(led,streaming):
        #下段x座標初期値 -> led幅
        low_x = led._width

        #ツイートリスト・リスト用変数初期化
        i = 0
        streaming.names = []
        streaming.scr_names = []
        streaming.tweet_text = []
        streaming.usr_icon_url = []

        #画像保存・読み込み用パス
        img_path = 'Resources/usr_icon.png'
        img_failed = 'Resources/failed.png'

        #アイコン設定、サイズ取得
        icon = led.icon_twitter
        icon_width = led.icon_twitter_width
        usr_icon_width = 0  #ツイートがあるときに 36 に設定 32がジャストだが、ズレが生じたため

        #上段x座標、表示テキスト初期化
        up_x = 0
        text_up1 = ' #' + streaming.hashtag
        text_up2 = ''
        text_low = ''

        #スクロール判定・待機カウント用変数
        up_scroll = False
        wait_count = 0

        #テキスト長さ保存用変数
        tag_length = 0

        while led.stopper:
            #canvas初期化
            led.canvas.Clear()

            #上段表示
            led.canvas.SetImage(icon,up_x,0)
            len = icon_width + graphics.DrawText(led.canvas,led.gothic,up_x + icon_width,14,led.white,text_up1)
            tag_length = len
            len = graphics.DrawText(led.canvas,led.gothic,tag_length + up_x,14,led.blue,text_up2)

            #枠からはみ出ていた場合
            if tag_length + len > led._width - 32 and not up_scroll:
                up_scroll = True

            if up_scroll:
                wait_count += 1
                #ウエイト1
                if wait_count >= 50 and wait_count <= 50 + tag_length + len - led._width + usr_icon_width:
                    up_x -= 1
                #ウエイト2
                elif wait_count == 100 + tag_length + len - led._width + usr_icon_width:
                    if not text_up2 == '':
                        up_x = 32
                    else:
                        up_x = 0
                    wait_count = 0

            #下段表示
            len = graphics.DrawText(led.canvas,led.gothic,low_x,30,led.orange,text_low)
            low_x -= 1


            #プロフィール画像表示
            if not text_up2 == '':
                led.canvas.SetImage(usr_icon_img,0,0)


            #スクロール終了処理
            if len + low_x < 0:
                #リストに次に表示するツイートがあるか
                try:
                    text_up1 = ' #' + streaming.hashtag
                    text_up2 = ' ' + streaming.names[i] + u'：' + streaming.scr_names[i]
                    text_low = streaming.tweet_text[i]

                    #プロフィール画像取得
                    try:
                        usr_icon_read = urlopen(streaming.usr_icon_url[i]).read()
                        usr_icon_bin = io.BytesIO(usr_icon_read)
                        usr_icon_img_bf = Image.open(usr_icon_bin).convert('RGB')
                        usr_icon_img = usr_icon_img_bf.resize((32,32))
                        usr_icon_img.point(lambda x: x * 0.8)
                    #失敗した場合
                    except:
                        usr_icon_img = Image.open(img_failed).convert('RGB')

                    usr_icon_width = 36
                    up_x = 32
                    i += 1

                #ない場合
                except:
                    text_up1 = ' #' + streaming.hashtag
                    text_up2 = ''
                    text_low = ''

                    usr_icon_width = 0
                    up_x = 0

                #リセット
                low_x = led._width
                up_scroll = False
                wait_count = 0

            #表示・スクロール待機
            led.canvas = led.matrix.SwapOnVSync(led.canvas)
            time.sleep(0.018)

        #終了時ブラックスクリーンに
        led.canvas.Clear()
        led.canvas = led.matrix.SwapOnVSync(led.canvas)

#直接実行（実行テスト用）
if __name__ == '__main__':
    import threading
    print('Mode: Tweet表示')
    #引数に 32x32枚数,明るさ設定可 設定する際は両方書くこと
    # Ex: led = Led_Setup(4,50)
    led = Led_Setup()
    #引数にハッシュタグ指定可、指定しなかった場合、streaming.pyのデフォルト設定になります
    streaming = Streaming()

    #ループするように
    led.stopper = True
    #ストリーミング開始、並列処理
    th = threading.Thread(target=streaming.start_streaming,args=(streaming,))
    th.setDaemon(True)
    th.start()

    print(u'ハッシュタグ：#' + streaming.hashtag)
    DisplayTweet.run(led,streaming)
