pythonはインストール済みとする

# 仮想環境の作成＠好きな作業ディレクトリ
python -m venv venv

# 仮想環境の有効化
source venv/bin/activate  # MacOS/Linux
.\venv\Scripts\activate  # Windows

# 依存関係のインストール
pip install -r requirements.txt

＊Chromeのデバッグモードでツイッターを開く
"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --new-window "https://x.com/" --remote-debugging-port=9222　#Windows　#macはぐぐれ

# 実行
python main.py
