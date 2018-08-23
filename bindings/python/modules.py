#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,os,time,math,random,tweepy,io
from datetime import datetime as dt

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image, ImageDraw

class Led_Setup(object):

    # Setup LEDs
    def __init__(self,chain=4,bright=50): # デフォルト設定（引数なしの場合）
        # Options
        self.options = RGBMatrixOptions()
        self.options.rows = 32
        self.options.chain_length = chain
        self.options.parallel = 1
        self.options.hardware_mapping = 'adafruit-hat-pwm'
        self.options.brightness = bright
        self.options.show_refresh_rate = 0
        self.matrix = RGBMatrix(options=self.options)
        self.canvas = self.matrix.CreateFrameCanvas()

        ### Load Font ###
        # 時計用フォント
        self.clcfont = graphics.Font()
        self.clcfont.LoadFont("Resources/Metroclock.bdf")

        # テキスト用フォント
        self.gothic = graphics.Font()
        self.gothic.LoadFont("Resources/Gothic-16.bdf")

        ###################

        ### Load images ###
        # twitterロゴ読み込み
        self.icon_twitter = Image.open("Resources/icon_twitter.png").convert('RGB')
        self.icon_twitter_width,self.icon_twitter_height = self.icon_twitter.size

        # TT用画像
        self.atos = Image.open("Resources/bunpatsu_atos.ppm").convert('RGB')

        ###################


        ### DJ名・コメント読み込み
        # DJ名・ジャンル・コメント用変数
        self.dj_name    = []
        self.dj_genre   = []
        self.dj_comment = []

        # リスト用変数
        self.djlist_num = 0

        # テキストファイル読み込み
        with open("Resources/DJList.txt",'r') as djtext:
            djlist = djtext.readlines()

        #各リストに格納
        for i in range(0,len(djlist)):
            djlist[i] = djlist[i].decode('utf-8')
            djlist[i] = djlist[i].replace('\n','')
            dj_sp = djlist[i].split(',')
            self.dj_name.append(dj_sp[0])
            self.dj_genre.append(dj_sp[1].replace('#',','))
            self.dj_comment.append(dj_sp[2])

        # リスト長を取得 (-1)
        self.djlist_len = len(self.dj_name) - 1

        ####################

        # Gifファイルパス用
        self.gif_path = ''

        # LED長さ
        self._width  = self.canvas.width
        self._height = self.canvas.height

        # Colors
        self.orange = graphics.Color(255, 110, 0)
        self.blue   = graphics.Color(0, 220, 255)
        self.white  = graphics.Color(255, 255, 255)
        self.red    = graphics.Color(255, 0, 0)
        self.green  = graphics.Color(0 ,255, 0)
        self.peach  = graphics.Color(255, 0, 255)

        # ループ制御用変数
        self.stopper = False

    # マイクロ秒換算関数
    def usleep(self, value):
        time.sleep(value / 1000000.0)

# Twitter Streaming
class Streaming(tweepy.StreamListener):
    def __init__(self,hashtag=u'Masテスト'): #デフォルト設定（引数なしの場合）
        #受け渡し用リスト
        self.tweet_text = ['']
        self.names = ['']
        self.scr_names = ['']
        self.usr_icon_url = ['']

        #タグ
        self.hashtag = hashtag

        #Twitter アクセスキー 読み込み
        keytxt_path = '/home/pi/twitter/key.txt'
        with open(keytxt_path,'r') as keytxt:
            keylist = keytxt.readlines()

        for i in range(0,len(keylist)):
            keylist[i] = keylist[i].decode('utf-8')
            keylist[i] = keylist[i].replace('\n','')

        CK = keylist[0]
        CS = keylist[1]
        AT = keylist[2]
        AS = keylist[3]

        self.auth = tweepy.OAuthHandler(CK,CS)
        self.auth.set_access_token(AT,AS)
        self.api = tweepy.API(self.auth)

    #ツイート取得時処理、最新ツイート取得時にこのメソッドが呼ばれます
    def on_status(self, status):

        #ハッシュタグがツイートに含まれていた場合
        if u'#'+self.hashtag in status.text or u'＃'+self.hashtag in status.text:
            #RT除外
            if 'RT' in status.text.replace(self.hashtag,''):
                return True
            #置換処理・リストに追加
            self.tweet_text.append(status.text.replace('\n',' ').replace('#' + self.hashtag,'').replace(u'＃' + self.hashtag,''))
            self.names.append(status.user.name)
            self.scr_names.append('@' + status.user.screen_name)

            #ユーザーアイコンURL格納
            self.usr_icon_url.append(status.user.profile_image_url_https.replace('_normal',''))

        else:
            pass

        #正常終了、Falseを返すと終了
        #現段階でFalseを返すことはなさそう
        return True

    def on_error(self, status_code):
        print(u'Twitterでエラー！')
        return True

    def on_timeout(self):
        print(u'タイムアウト...')
        return True

    #ストリーミング起動用
    #threadingで起動させること、setDaemonも忘れずに
    def start_streaming(self,streaming):
        self.stream = tweepy.Stream(self.auth, streaming)
        self.stream.filter(track=[self.hashtag])

    #デバッグ用メソッド
    def print_tweet(self):
        i = 0
        while True:
            try:
                tx1 = self.names[i]
                tx2 = self.scr_names[i]
                tx3 = self.tweet_text[i]
                tx4 = self.usr_icon_url[i]
                print(u'{0} {1}:{2} \nIcon:{3}'.format(tx1,tx2,tx3,tx4))
                i += 1
            except:
                pass

# 紹介
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

# 発車標TT
class Departure(object):
    # 発車標メソッド
    @staticmethod
    def run(led):
        #画像サイズ取得
        img_width,img_height = led.atos.size

        # 発車標用座標
        x = 0
        y = -32

        # 発車標表示時間
        wait1 = 5

        # ループカウント用
        waiting = 0

        # 団体表示（初回用）
        while led.stopper and waiting <= wait1:
            led.canvas.Clear()
            led.canvas.SetImage(led.atos,x,0)
            led.canvas = led.matrix.SwapOnVSync(led.canvas)
            time.sleep(0.1)
            waiting += 0.1

        #ループカウントリセット
        waiting = 0

        # メインループ
        while led.stopper:

            while led.stopper and waiting <= wait1:
                led.canvas.Clear()
                led.canvas.SetImage(led.atos,x,y)
                led.canvas = led.matrix.SwapOnVSync(led.canvas)
                time.sleep(0.1)
                waiting += 0.1

            #ループカウントリセット
            waiting = 0
            count = 1
            y -= 16

            #終端判定・リスト・団体表示
            if y <= -img_height:

                while led.stopper and waiting <= wait1:
                    led.canvas.Clear()
                    led.canvas.SetImage(led.atos,x,0)
                    led.canvas = led.matrix.SwapOnVSync(led.canvas)
                    time.sleep(0.1)
                    waiting += 0.1

                #ループカウント・座標リセット
                waiting = 0
                count = 1
                y = -32

        led.canvas.Clear()
        led.canvas = led.matrix.SwapOnVSync(led.canvas)

# Twitter
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

# 円アニメ
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

        # 終了時ブラックスクリーンに
        led.canvas.Clear()
        led.canvas = led.matrix.SwapOnVSync(led.canvas)

# 明るさパルス
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

# 色パルス
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

# ボリュームバー
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

# 次DJ名・ジャンル表示
class DJList(object):

    @staticmethod
    def run(led):
        # レインボー用カウント
        continuum = 0

        # 初期設定
        text_up1 = u'  次は  '
        text_up2 = led.dj_name[led.djlist_num] + '  '
        text_up3 = led.dj_genre[led.djlist_num]
        text_low = led.dj_comment[led.djlist_num]

        # 座標保持
        save_x = 0

        # リスト確認・座標リセット用
        save_num = led.djlist_num

        # 初期座標
        low_x = led._width

        # 表示切り替え用
        count = 0

        # レインボー表示
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

        # メインループ
        while led.stopper:
            led.canvas.Clear()

            red,green,blue = rainbow(continuum)
            len = graphics.DrawText(led.canvas,led.gothic,0,14,led.green,text_up1)
            save_x = len
            len = graphics.DrawText(led.canvas,led.gothic,save_x,14,graphics.Color(red,green,blue),text_up2)
            len = graphics.DrawText(led.canvas,led.gothic,save_x+len,14,led.blue,text_up3)
            len = graphics.DrawText(led.canvas,led.gothic,low_x,30,led.white,text_low)

            low_x -= 1
            count += 0.5
            continuum += 1

            if count > 200:
                count = 0
            if count <= 100:
                text_up1 = u'  次は  '
                text_up2 = led.dj_name[led.djlist_num] + '  '
                text_up3 = led.dj_genre[led.djlist_num]
            elif count > 100 and count <= 200:
                text_up1 = u'  Next  '
                text_up2 = led.dj_name[led.djlist_num] + '  '
                text_up3 = led.dj_genre[led.djlist_num]
            if len + low_x < 0 or not save_num == led.djlist_num:
                low_x = led._width
                text_low = led.dj_comment[led.djlist_num]

            save_num = led.djlist_num

            led.canvas = led.matrix.SwapOnVSync(led.canvas)
            time.sleep(0.01)

        led.canvas.Clear()
        led.canvas = led.matrix.SwapOnVSync(led.canvas)

# LEDJ x VJ
class GifPlayer(object):

    @staticmethod
    def run(led):
        imgs = Image.open(led.gif_path).convert('RGB')
        #imgs = imgs.resize((led._width,led._height))
        print(imgs.info.loop)
        #imgs_len = imgs.n_frames

        while led.stopper:
            led.canvas.Clear()

            try:
                led.canvas.SetImage(imgs.seek(imgs.tell()+1),0,0)
            except EOFError:
                led.canvas.SetImage(imgs.seek(0),0,0)

            led.canvas = led.matrix.SwapOnVSync(led.canvas)
            time.sleep(1/30)

        led.canvas.Clear()
        led.canvas = led.matrix.SwapOnVSync(led.canvas)

"""
# DJ名・セトリ・時計表示
class MetroDJ(object):

    @staticmethod
    def run(led):

        # 位置比較・座標リセット用
        compnum = led.number

        # 上段
        def up_led():
            # 時刻取得
            hour = dt.now().strftime("%H")
            minute = dt.now().strftime("%M")
            sec = dt.now().strftime("%S")

            # コロン表示判定
            if int(sec) % 2 == 0:
                up_text = hour + ':' + minute
            else:
                up_text = hour + ' ' + minute

            return up_text


        while led.stopper:
            # 表示初期化
            led.canvas.Clear()

            up_text = up_led()

            # 下段 例外処理
            try:
                low_text = led.setlist[led.number]
            except:
                led.number = led.setlist_len

            # 上段表示
            graphics.DrawText(led.canvas,led.clcfont,0,16,led.white,up_text)
            # 下段表示
            len = graphics.DrawText(led.canvas,led.gothic,low_x,30,led.blue,low_text)

            # 端に到達した場合・
            if (low_x + len < 0) or not compnum == led.number:
                low_x = led._width

            compnum = led.number

            led.canvas = led.matrix.SwapOnVSync(led.canvas)
            low_x -= 1

            # スクロール速度
            time.sleep(0.02)
"""
