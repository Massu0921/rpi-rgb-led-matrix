#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading,time
import modules
import Tkinter as TK
import tkFileDialog as FD
from PIL import Image

#####################################################################
# LEDJ操作GUI
# 各モードの起動メソッドは LED に
# GUI関連は Gui に
#####################################################################

# LEDインスタンス生成, ストリーミング開始
class LED(object):
    def __init__(self,chain=10,bright=50):
        self.led = modules.Led_Setup(chain,bright)
        print(u'32x32 {0} 枚、明るさ {1} で動作します'.format(chain,bright))
        self.streaming = modules.Streaming(u'kosendj')
        print(u'ハッシュタグ：#' + self.streaming.hashtag)

        stream_th = threading.Thread(target = self.streaming.start_streaming,args=(self.streaming,))
        stream_th.setDaemon(True)
        stream_th.start()

# GUI・各モード起動
class GUI(TK.Frame,LED):
    def __init__(self,master=None):
        #エラー回避のため、先にGUIフレーム作成
        TK.Frame.__init__(self,master)
        LED.__init__(self)

        self.master.title('LEDJ_Controller')
        fontsize = 25
        # 外側隙間
        dx = 20
        dy = 10

        self.bt_intro = TK.Button(text=u'Introduction',font=("",fontsize),bg='cyan',command=self.introduction)
        self.bt_intro.grid(row=0,column=0,columnspan=4,padx=dx,pady=dy,sticky=TK.W + TK.E)

        self.bt_tweet = TK.Button(text=u'Twitter',font=("",fontsize),bg='cyan',command=self.display_tweet)
        self.bt_tweet.grid(row=0,column=4,columnspan=4,padx=dx,pady=dy,sticky=TK.W + TK.E)

        self.bt_djtt = TK.Button(text=u'DJTT',font=("",fontsize),bg='cyan',command=self.djtt)
        self.bt_djtt.grid(row=0,column=8,columnspan=4,padx=dx,pady=dy,sticky=TK.W + TK.E)

        self.bt_circle = TK.Button(text=u'CircleAnime',font=("",fontsize),bg='orchid1',command=self.circleanime)
        self.bt_circle.grid(row=1,column=0,columnspan=3,padx=dx,pady=dy,sticky=TK.W + TK.E)

        self.bt_pulb = TK.Button(text=u'PulsingBrightness',font=("",fontsize),bg='orchid1',command=self.pulsingbrightness)
        self.bt_pulb.grid(row=1,column=3,columnspan=3,padx=dx,pady=dy,sticky=TK.W + TK.E)

        self.bt_pulc = TK.Button(text=u'PulsingColors',font=("",fontsize),bg='orchid1',command=self.pulsingcolors)
        self.bt_pulc.grid(row=1,column=6,columnspan=3,padx=dx,pady=dy,sticky=TK.W + TK.E)

        # 廃止(Gif置き換え) 後で撤去すること
        self.bt_volume = TK.Button(text=u'VolumeBars',font=("",fontsize),bg='orchid1',command=self.volumebars)
        self.bt_volume.grid(row=1,column=9,columnspan=3,padx=dx,pady=dy,sticky=TK.W + TK.E)
        self.bt_volume.configure(state=TK.DISABLED)

        # DJリスト表示用
        self.message_label = TK.Label(text=u' --- ',font=("",16))
        self.message_label.grid(row=2,column=0,columnspan=12,padx=dx,pady=dy,sticky=TK.W + TK.E)

        self.bt_back = TK.Button(text=u'　　Back ❙◀　　',font=("",fontsize),bg='Khaki',command=self.sub)
        self.bt_back.grid(row=3,column=0,columnspan=4,padx=dx,pady=dy,sticky=TK.W + TK.E)
        self.bt_back.configure(state=TK.DISABLED)

        self.bt_start = TK.Button(text=u'　Start ▶　',font=("",fontsize),bg='green2',command=self.djlist)
        self.bt_start.grid(row=3,column=4,columnspan=4,padx=dx,pady=20,sticky=TK.W + TK.E)

        self.bt_next = TK.Button(text=u'　　Next ▶❙　　',font=("",fontsize),bg='Khaki',command=self.add)
        self.bt_next.grid(row=3,column=8,columnspan=4,padx=dx,pady=dy,sticky=TK.W + TK.E)

        # 停止ボタン
        self.bt_stop = TK.Button(text=u'　停　止　Stop ■　',font=("",fontsize),bg='OrangeRed2',command=self.stop_led)
        self.bt_stop.grid(row=4,column=0,columnspan=12,padx=dx,pady=20,sticky=TK.W + TK.E)

        # LEDJ x VJ
        # フレーム配置は見送り
        # ボタンの後にgridしないとエラー
        #*#* Deck 1 *#*#
        self.ent_media_1 = TK.Entry(font=("",16))

        self.bt_media_1 = TK.Button(text=u'Browse',font=("",16),command=self.browse_1)
        self.bt_media_1.grid(row=5,column=8,columnspan=2,padx=dx,pady=20,sticky=TK.W+TK.E)

        self.bt_mediaplay_1 = TK.Button(text=u'　Play ▶　',font=("",fontsize),bg='deep sky blue',command=self.mediaplayer_1)
        self.bt_mediaplay_1.grid(row=5,column=10,columnspan=2,padx=dx,pady=20,sticky=TK.W+TK.E)
        self.bt_mediaplay_1.configure(state=TK.DISABLED)
        # ここでEntry配置
        self.ent_media_1.grid(row=5,column=0,columnspan=8,padx=dx,pady=20,sticky=TK.W+TK.E)

        #*#* Deck 2 *#*#
        self.ent_media_2 = TK.Entry(font=("",16))

        self.bt_media_2 = TK.Button(text=u'Browse',font=("",16),command=self.browse_2)
        self.bt_media_2.grid(row=6,column=8,columnspan=2,padx=dx,pady=20,sticky=TK.W+TK.E)

        self.bt_mediaplay_2 = TK.Button(text=u'　Play ▶　',font=("",fontsize),bg='deep sky blue',command=self.mediaplayer_2)
        self.bt_mediaplay_2.grid(row=6,column=10,columnspan=2,padx=dx,pady=20,sticky=TK.W+TK.E)
        self.bt_mediaplay_2.configure(state=TK.DISABLED)

        self.ent_media_2.grid(row=6,column=0,columnspan=8,padx=dx,pady=20,sticky=TK.W+TK.E)

        # CheckBox
        self.blv_scroll = TK.BooleanVar()
        self.blv_resize = TK.BooleanVar()
        self.blv_flash = TK.BooleanVar()
        # Set
        self.blv_scroll.set(False)
        self.blv_resize.set(False)
        self.blv_flash.set(False)
        # Scroll
        self.ck_scroll = TK.Checkbutton(text=u'Scroll Media',font=("",22),variable=self.blv_scroll)
        self.ck_scroll.grid(row=7,column=0,columnspan=2,padx=dx,pady=20,sticky=TK.W+TK.E)
        # Resize
        self.ck_resize = TK.Checkbutton(text=u'resize',font=("",22),variable=self.blv_resize)
        self.ck_resize.grid(row=7,column=2,columnspan=2,padx=dx,pady=20,sticky=TK.W+TK.E)
        # Flash
        self.ck_flash = TK.Checkbutton(text=u'resize',font=("",22),variable=self.blv_flash)
        self.ck_flash.grid(row=7,column=4,columnspan=2,padx=dx,pady=20,sticky=TK.W+TK.E)

    # LED停止用
    def stop_led(self):
        self.led.stopper = False

    # ツイート表示
    def display_tweet(self):
        self.led.stopper = False
        time.sleep(0.5)
        th_led = threading.Thread(target = modules.DisplayTweet.run,args=(self.led,self.streaming,))
        th_led.setDaemon(True)
        self.led.stopper = True
        th_led.start()

    # 円アニメ
    def circleanime(self):
        self.led.stopper = False
        time.sleep(0.5)
        th_led = threading.Thread(target = modules.CircleAnime.run,args=(self.led,))
        th_led.setDaemon(True)
        self.led.stopper = True
        th_led.start()

    # 紹介
    def introduction(self):
        self.led.stopper = False
        time.sleep(0.5)
        th_led = threading.Thread(target = modules.Introduction.run,args=(self.led,))
        th_led.setDaemon(True)
        self.led.stopper = True
        th_led.start()

    # 明るさパルス
    def pulsingbrightness(self):
        self.led.stopper = False
        time.sleep(0.5)
        th_led = threading.Thread(target = modules.PulsingBrightness.run,args=(self.led,))
        th_led.setDaemon(True)
        self.led.stopper = True
        th_led.start()

    # 色パルス
    def pulsingcolors(self):
        self.led.stopper = False
        time.sleep(0.5)
        th_led = threading.Thread(target = modules.PulsingColors.run,args=(self.led,))
        th_led.setDaemon(True)
        self.led.stopper = True
        th_led.start()

    # ボリュームバー
    def volumebars(self):
        self.led.stopper = False
        time.sleep(0.5)
        th_led = threading.Thread(target = modules.VolumeBars.run,args=(self.led,))
        th_led.setDaemon(True)
        self.led.stopper = True
        th_led.start()

    # 発車標
    def djtt(self):
        self.led.stopper = False
        time.sleep(0.5)
        th_led = threading.Thread(target = modules.DJTT.run,args=(self.led,))
        th_led.setDaemon(True)
        self.led.stopper = True
        th_led.start()

    # DJ名・コメント表示用
    def djlist(self):
        self.led.stopper = False
        time.sleep(0.5)
        th_led = threading.Thread(target = modules.DJList.run,args=(self.led,))
        th_led.setDaemon(True)
        self.led.stopper = True
        th_led.start()

        self.message_label.configure(text = self.led.dj_name[self.led.djlist_num])

    # MediaPlayer
    def mediaplayer_1(self):
        self.led.media = self.media_1
        self.led.frame_len = self.frame_len_1
        self.led.bool_scroll = self.blv_scroll.get()
        self.led.bool_resize = self.blv_resize.get()
        self.led.bool_flash - self.blv_flash.get()
        self.led.stopper = False
        time.sleep(0.5)
        th_led = threading.Thread(target = modules.MediaPlayer.run,args=(self.led,))
        th_led.setDaemon(True)
        self.led.stopper = True
        th_led.start()

    def mediaplayer_2(self):
        self.led.media = self.media_2
        self.led.frame_len = self.frame_len_2
        self.led.bool_scroll = self.blv_scroll.get()
        self.led.bool_resize = self.blv_resize.get()
        self.led.bool_flash - self.blv_flash.get()
        self.led.stopper = False
        time.sleep(0.5)
        th_led = threading.Thread(target = modules.MediaPlayer.run,args=(self.led,))
        th_led.setDaemon(True)
        self.led.stopper = True
        th_led.start()

    # 曲番号加算・減算用メソッド
    def add(self):
        self.led.djlist_num += 1

        if  self.led.djlist_num >= self.led.djlist_len:
            self.bt_next.configure(state=TK.DISABLED)
        else:
            self.bt_next.configure(state=TK.NORMAL)
            self.bt_back.configure(state=TK.NORMAL)

        self.message_label.configure(text = self.led.dj_name[self.led.djlist_num])

    def sub(self):
        self.led.djlist_num -= 1

        if self.led.djlist_num <= 0:
            self.bt_back.configure(state=TK.DISABLED)
        else:
            self.bt_next.configure(state=TK.NORMAL)
            self.bt_back.configure(state=TK.NORMAL)

        self.message_label.configure(text = self.led.dj_name[self.led.djlist_num])

    # File Browse
    # Deck 1
    def browse_1(self):
        # ファイル名取得
        img_path = FD.askopenfilename(initialdir='/home/pi/rpi-rgb-led-matrix/bindings/python/Resources/')
        # Entryにdirを表示
        self.ent_media_1.delete(0,TK.END)
        self.ent_media_1.insert(0,img_path)

        try:
            self.bt_mediaplay_1.configure(state=TK.DISABLED)
            self.media_1,self.frame_len_1 = self.mediaopen(img_path)
            self.bt_mediaplay_1.configure(state=TK.NORMAL)
        except:
            print('Deck1 Load Failed')

    # Deck 2
    def browse_2(self):
        # ファイル名取得
        img_path = FD.askopenfilename(initialdir='/home/pi/Desktop/')
        # Entryにdirを表示
        self.ent_media_2.delete(0,TK.END)
        self.ent_media_2.insert(0,img_path)

        try:
            self.bt_mediaplay_2.configure(state=TK.DISABLED)
            self.media_2,self.frame_len_2 = self.mediaopen(img_path)
            self.bt_mediaplay_2.configure(state=TK.NORMAL)
        except:
            print('Deck2 Load Failed')

    # Open Media
    def mediaopen(self,img_path):
        # Media読み込み
        img = Image.open(img_path)

        # フレーム数確認
        frame_len = 0
        while True:
            try:
                img.seek(img.tell()+1)
                frame_len += 1
            except EOFError:
                break

        return img,frame_len

if __name__ == '__main__':
    gui = GUI()
    gui.mainloop()
