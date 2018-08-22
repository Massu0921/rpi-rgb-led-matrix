#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Tkinter as TK
import threading,time
import modules

#####################################################################
# LEDJ操作GUI
# 各モードの起動メソッドは LED に
# GUI関連は Gui に
#####################################################################

# LEDインスタンス生成, ストリーミング開始
class LED(object):
    def __init__(self,chain=4,bright=40):
        self.led = modules.Led_Setup(chain,bright)
        print(u'32x32 {0} 枚、明るさ {1} で動作します'.format(chain,bright))
        self.streaming = modules.Streaming(u'文発')
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
        dx = 20
        dy = 20

        self.bt_intro = TK.Button(text=u'　紹　介　',font=("",fontsize),bg='Khaki',command=self.introduction)
        self.bt_intro.grid(row=0,column=0,columnspan=2,padx=dx,pady=dy,sticky=TK.W + TK.E)

        self.bt_tweet = TK.Button(text=u'ツイート晒し',font=("",fontsize),bg='cyan',command=self.display_tweet)
        self.bt_tweet.grid(row=0,column=2,columnspan=2,padx=dx,pady=dy,sticky=TK.W + TK.E)

        self.bt_dep = TK.Button(text=u'Departure',font=("",fontsize),bg='green2',command=self.departure)
        self.bt_dep.grid(row=0,column=4,columnspan=2,padx=dx,pady=dy,sticky=TK.W + TK.E)

        self.bt_circle = TK.Button(text=u'CircleAnime',font=("",fontsize),bg='purple1',command=self.circleanime)
        self.bt_circle.grid(row=1,column=0,columnspan=1,padx=dx,pady=dy,sticky=TK.W + TK.E)

        self.bt_pulb = TK.Button(text=u'PulsingBrightness',font=("",fontsize),bg='magenta2',command=self.pulsingbrightness)
        self.bt_pulb.grid(row=1,column=1,columnspan=1,padx=dx,pady=dy,sticky=TK.W + TK.E)

        self.bt_pulc = TK.Button(text=u'PulsingColors',font=("",fontsize),bg='OrangeRed2',command=self.pulsingcolors)
        self.bt_pulc.grid(row=1,column=2,columnspan=1,padx=dx,pady=dy,sticky=TK.W + TK.E)

        self.bt_volume = TK.Button(text=u'VolumeBars',font=("",fontsize),bg='yellow2',command=self.volumebars)
        self.bt_volume.grid(row=1,column=3,columnspan=1,padx=dx,pady=dy,sticky=TK.W + TK.E)

        # DJリスト表示用
        self.message_label = TK.Label(text=u' --- ',font=("",16))
        self.message_label.grid(row=3,column=0,columnspan=1,padx=dx,pady=dy,sticky=TK.W + TK.E)

        self.bt_back = TK.Button(text=u'　　Back ❙◀　　',font=("",fontsize),bg='cyan',command=self.sub)
        self.bt_back.grid(row=4,column=0,columnspan=2,padx=dx,pady=dy,sticky=TK.W + TK.E)

        self.bt_start = TK.Button(text=u'　Start (Reset) ▶　',font=("",fontsize),bg='green2',command=self.djlist)
        self.bt_start.grid(row=4,column=1,columnspan=2,padx=dx,pady=20,sticky=TK.W + TK.E)

        self.bt_next = TK.Button(text=u'　　Next ▶❙　　',font=("",fontsize),bg='Khaki',command=self.add)
        self.bt_next.grid(row=4,column=2,columnspan=2,padx=dx,pady=dy,sticky=TK.W + TK.E)

        # 停止ボタン
        self.bt_stop = TK.Button(text=u'　停　止　Stop ■　',font=("",fontsize),bg='IndianRed1',command=self.stop_led)
        self.bt_stop.grid(row=3,column=0,columnspan=1,padx=dx,pady=20,sticky=TK.W + TK.E)

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
    def departure(self):
        self.led.stopper = False
        time.sleep(0.5)
        th_led = threading.Thread(target = modules.Departure.run,args=(self.led,))
        th_led.setDaemon(True)
        self.led.stopper = True
        th_led.start()

    # メッセージ表示用
    def djlist(self):
        self.led.stopper = False
        time.sleep(0.5)
        th_led = threading.Thread(target = modules.DJList.run,args=(self.led,))
        th_led.setDaemon(True)
        self.led.stopper = True
        th_led.start()

        self.message_label.configure(text = self.led.dj_name[self.led.djlist_num])

    # 曲番号加算・減算用メソッド
    def add(self):
        self.led.djlist_num += 1

        if  self.led.djlist_num <= self.led.djlist_len:
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

if __name__ == '__main__':
    gui = GUI()
    gui.mainloop()
