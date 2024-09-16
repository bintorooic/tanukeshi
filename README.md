pythonはインストール済みとする   

# 仮想環境の作成＠好きな作業ディレクトリ  
```
python -m venv venv  
```

```
git clone -b master  https://github.com/bintorooic/tanukeshi.git
```
# 仮想環境の有効化  
- MacOS/Linux
```
source venv/bin/activate
```
- Windows
```
.\venv\Scripts\Activate.ps1
```
※仮想環境の取り扱い方法詳細はvenvでぐぐってください

# 依存関係のインストール  
```
pip install -r requirements.txt  
```

# Configの設定
username = 自分のアカウント名　※@は不要。

# Chromeの立ち上げ
＊Chromeのデバッグモードでツイッターを開く #Windows #macはぐぐれ  
```
"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --new-window "https://x.com/" --remote-debugging-port=9222
```
対象のアカウントでログインしてください。  

# 実行
自ツイート、RTの取り消し  
```
python main.py
```
リプライ欄の削除、RTの取り消し  
```
python deleteReply.py
```
スクリプトを途中で止めたいとき:  
Ctrl+c
