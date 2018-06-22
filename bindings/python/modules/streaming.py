#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy
import threading

#####################################################################
#ツイートストリーミングクラス
#インスタンス生成時にhashtag指定可能、第一引数に
#以下、起動方法です
#インスタンス生成、タグ変更する場合は引数に任意タグ設定
# Ex: streaming = Streaming()
# Ex: streaming = Streaming(u'任意タグ')
#スレッド設定、引数には自身のインスタンスを指定
#th = threading.Thread(target=streaming.start_streaming,args=(streaming,))
#th.setDaemon(True) #メインスレッド終了とともにこのスレッドも終了するように
#th.start()
#メインスレッドで起動するとそこで詰みます
#####################################################################

class Streaming(tweepy.StreamListener):
    def __init__(self,hashtag=u'Masテスト'): #デフォルト設定（引数なしの場合）
        #受け渡し用リスト
        self.tweet_text = ['']
        self.names = ['']
        self.scr_names = ['']
        self.usr_icon_url = ['']

        #タグ
        self.hashtag = hashtag

        #Twitter アクセスキー
        CK = ""
        CS = ""
        AT = ""
        AS = ""

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

#直接実行時（ツイート取得テスト）
if __name__ == '__main__':
    print(u'Tweepy ストリーミングテスト')

    #引数にハッシュタグ指定可、指定しなかった場合、streaming.pyのデフォルト設定になります
    streaming = Streaming(u'Test')
    #ストリーミング開始、並列処理
    th = threading.Thread(target=streaming.start_streaming,args=(streaming,))
    th.setDaemon(True)
    th.start()

    print(u'ハッシュタグ：#' + streaming.hashtag)
    #テスト開始、CLI上に取得情報表示
    streaming.print_tweet()
