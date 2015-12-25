音声認識用サーバ構築

西村良太

----------------------------
# Ubuntuインストール
## Ubuntu14.04日本語版

## ディレクトリ名を英語にするコマンド
```
$ LANG=C xdg-user-dirs-gtk-update
```
## VM ware Tools

## 固定IP設定
まず、network-manager を使わないようにアンインストールします。
```
$ sudo apt-get remove network-manager
```
そして、`sudo nano /etc/network/interfaces`
でファイルを編集して固定ＩＰを記述します。

```
auto eth0
iface eth0 inet static
address 192.168.100.103
netmask 255.255.255.0
gateway 192.168.100.1
dns-nameservers 192.168.100.1
#dns-search hoge.com
```

## アップデート
```
$ sudo apt-get update && sudo apt-get -y upgrade
```

----------------------------
# Juliusインストール
## ソースをダウンロードしてコンパイル
```
$ cd ~/Downloads
$ wget --trust-server-names "http://osdn.jp/frs/redir.php?m=iij&f=%2Fjulius%2F60273%2Fjulius-4.3.1.tar.gz"
$ tar zxvf julius-4.3.1.tar.gz
$ cd julius-4.3.1
$ ./configure
$ make
```
## 音声認識用モデルをダウンロード
```
$ cd ~/Downloads
$ wget --trust-server-names 'http://osdn.jp/frs/redir.php?m=iij&f=%2Fjulius%2F60416%2Fdictation-kit-v4.3.1-linux.tgz'
$ tar xvzf dictation-kit-v4.3.1-linux.tgz
```
## ディレクトリ構成を綺麗にする
~/Software/julius　の下に，コンパイルしたjuliusバイナリと音声認識用モデルを置く．
```
$ cd ~
$ mkdir -p ~/Software/julius
$ cp ~/Downloads/julius-4.3.1/julius/julius ~/Software/julius/.
$ mv ~/Downloads/dictation-kit-v4.3.1-linux ~/Software/julius/julius-kit
```

## テスト用音声ダウンロード（西村良太の声on西村良太webサーバ）
「これはマイクのテストです」というwavファイルをダウンロード
```
$ cd ~/Software/julius
$ mkdir test_wav
$ cd test_wav
$ wget http://sayonari.com/data/test_16000.wav
```
音を聞いてみたい場合には，`play test_16000.wav`を実行すれば良い．（実行には，soxがインストールされている必要がある．）

## 音声認識テスト
```
$ cd ~/Software/julius/
$ ./julius -C ./julius-kit/am-gmm.jconf -C ./julius-kit/main.jconf -input rawfile
```
実行すると以下のように表示される
```
（何やらザザザーっと表示されて）
----------------------- System Information end -----------------------

Notice for feature extraction (01),
	*************************************************************
	* Cepstral mean normalization for batch decoding:           *
	* per-utterance mean will be computed and applied.          *
	*************************************************************

------
### read waveform input
enter filename->

```

認識させたいファイル名`./test_wav/test_16000.wav`を入力すると以下のように出力される．
```
### read waveform input
enter filename->./test_wav/test_16000.wav
Stat: adin_file: input speechfile: ./test_wav/test_16000.wav
STAT: 52832 samples (3.30 sec.)
STAT: ### speech analysis (waveform -> MFCC)
### Recognition: 1st pass (LR beam)
........................................................................................................................................................................................................................................................................................................................................pass1_best:  これ は マイク の テイスト です 。
pass1_best_wordseq: <s> これ+代名詞 は+助詞 マイク+名詞 の+助詞 テイスト+名詞 です+助動詞 </s>
pass1_best_phonemeseq: silB | k o r e | w a | m a i k u | n o | t e: s u t o | d e s u | silE
pass1_best_score: -7939.280273
### Recognition: 2nd pass (RL heuristic best-first)
STAT: 00 _default: 33334 generated, 3165 pushed, 363 nodes popped in 328
sentence1:  これ は マイク の テスト です 。
wseq1: <s> これ+代名詞 は+助詞 マイク+名詞 の+助詞 テスト+名詞 です+助動詞 </s>
phseq1: silB | k o r e | w a | m a i k u | n o | t e s u t o | d e s u | silE
cmscore1: 0.564 0.538 0.329 0.399 0.227 0.131 0.588 1.000
score1: -7946.526367


------
### read waveform input
enter filename->
```

これでJuliusインストールは成功

----------------------------
# Juliusサーバ化に向けたテスト
CherryPyというシステムを用いて，Juliusをサーバー化させる．
http://www.cherrypy.org/

## CherryPyのインストール
```
cd ~/Downloads
$ wget https://pypi.python.org/packages/source/C/CherryPy/CherryPy-3.8.1.tar.gz#md5=919301731c9835cf7941f8bdc1aee9aa
$ tar zxvf CherryPy-3.8.1.tar.gz
$ cd CherryPy-3.8.1
$ sudo python setup.py install
```

## ASRサーバ起動
ファイル：/home/nishimura/Public/cgi-bin/ASRServer.py
```python
#!/usr/bin/env python

# Please configure the path at LINE:15(cwd), 21(asr_filepath)
# Please change the IP at LINE:31

import cherrypy
import subprocess
import sys
import os
import time

class ASRServer(object):
	p = subprocess.Popen (
		"./julius -C ./julius-kit/am-gmm.jconf -C ./julius-kit/main.jconf -input file -outfile",
		shell=True, 
		cwd="/home/nishimura/Software/julius/.", 
		stdin=subprocess.PIPE,
		stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
		close_fds=True)
	(stdouterr, stdin) = (p.stdout, p.stdin)
	def index(self):
	        asr_filepath = '/home/nishimura/Public/asr/'
# wave GET
# wave write
		os.remove(asr_filepath + 'ch_asr.out')
		self.p.stdin.write(asr_filepath + 'ch_asr.wav\n')
		self.p.stdin.flush()
		while not (os.path.exists(asr_filepath + 'ch_asr.out') and len(open(asr_filepath + 'ch_asr.out').readlines()) == 5):
			time.sleep(0.1)
		outlines = open(asr_filepath + 'ch_asr.out').read()
		return outlines
	index.exposed = True
cherrypy.config.update({'server.socket_port': 8000,})
cherrypy.config.update({'server.socket_host': '192.168.100.103',})
cherrypy.quickstart(ASRServer())

```

```
$ python ./ASRServer.py
```
すると，localhostの，8000番ポートに，音声認識サーバが立ち上がる．

### 動作説明
- juliusを　`-input file`（ファイル入力）モードで起動
- 標準入力からファイル名を入れると，そのファイルの認識を行う
	- 外部サーバから，POSTでwaveファイルを送信
	- サーバ上の`/home/nishimura/Public/asr/ch_asr.wav`に上書き
	- このファイルをjuliusで認識
	- 認識結果を`/home/nishimura/Public/asr/ch_asr.out`に出力
		- 出力用ファイル`ch_asr.out`は，毎回消される
		- juliusから.outファイルが生成された後，出力結果が5行になるまでループで待つ
		- （待たないと，ファイル内容が無いうちに，中身0なファイルを出力して処理が完了してしまう）		

## クライアントからの使い方
●●POSTで外部から叩く
●●WAVEファイルを送りつける
●●クライアントのソースを貼る


----------------------------
# Python Webサーバ（CGI）
## cgi起動用Pythonスクリプト起動

`./cgiserver.py`に以下の内容を入れる．
```Python
#!/usr/bin/env python

import CGIHTTPServer
CGIHTTPServer.test()
```
実行権限を与えて実行
```
$ chmod +x ./cgiserver.py
$ ./cgiserver.py
```
実行したディレクトリをホームとした，webサーバが立ち上がる．

## テスト接続
http://nishimura-asr.local:8000/
