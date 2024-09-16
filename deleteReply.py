from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.keys import Keys
import configparser

# 設定ファイルを読み込む
config = configparser.ConfigParser()
config.read('setting.conf')

'''
# Chromeをポートを指定してデバッグモードで起動してください。※Chromeのウィンドウを一度すべて閉じてから実施。
# 未ログインの場合はログインしてください。
# ※Windowsの例
# "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --new-window "https://x.com/" --remote-debugging-port=9222

イーロン・マスクに怒られてどんな目にあっても知りません。


ソースコード一番上のtwitter_usernameを指定して下さい。
'''

# #########################################################
# 自分のアカウント名を指定
twitter_username = config['Twitter']['username']

# #########################################################



urlhost = "https://x.com/"
reply = "/with_replies"
url = urlhost + twitter_username + reply

print(f"start--")

options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
options.add_argument("--disable-extensions")
options.add_argument("--disable-component-extensions-with-background-pages")
driver = webdriver.Chrome(options=options)


def init_driver(driver):
    driver.get(url)
    time.sleep(3)


def is_RT():
    article = driver.find_element(By.TAG_NAME, "article")
    try:
        is_reposted = article.find_element(By.XPATH, ".//span[contains(text(), 'あなたがリポストしました')]")
        print("リポストされた投稿です")
        return is_reposted 
    
    except NoSuchElementException:
        print("リポストされた投稿ではありません")
        return False

def clear_rt():
    print("clear_rt start")
    article = driver.find_element(By.TAG_NAME, "article")

    # article要素内の3つ目のボタンを見つけてクリック
    buttons = article.find_elements(By.TAG_NAME, "button")
    if len(buttons) >= 3:
        if len(buttons) == 6:
            buttons[2].click()
        elif len(buttons) == 7:
            buttons[3].click()
        else:
            raise Exception("未対応のツイートパターンです。")
        
        # "ポストを取り消す"テキストを持つメニュー項目を探してクリック
        menu_items = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[role="menuitem"]'))
        )
        # data-testid属性がunretweetConfirmの要素を探してクリック
        unretweetConfirm = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="unretweetConfirm"]'))
        )
        # JavaScriptを使用してクリック
        driver.execute_script("arguments[0].click();", unretweetConfirm)
        print("「ポストを取り消す」確認ボタンをクリックしました")
        return True            
        
    else:
        print("記事内に3つ目のボタンが見つかりませんでした")
        return False


def click_delete():
    
    menu_items = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[role="menuitem"]'))
    )
    for item in menu_items:
        if item.text == "削除":
            item.click()
            print("「削除」メニューアイテムをクリックしました")
            
            #削除確認ボタンをクリック
            # css-175oi2r r-sdzlij r-1phboty r-rs99b7 r-lrvibr r-16y2uox r-6gpygo r-1udh08x r-1udbk01 r-3s2u2q r-peo1c r-1ps3wis r-cxgwc0 r-1loqt21 r-o7ynqc r-6416eg r-1ny4l3lクラスを持つ要素をクリック
            element = driver.find_element(By.CSS_SELECTOR, '.css-175oi2r.r-sdzlij.r-1phboty.r-rs99b7.r-lrvibr.r-16y2uox.r-6gpygo.r-1udh08x.r-1udbk01.r-3s2u2q.r-peo1c.r-1ps3wis.r-cxgwc0.r-1loqt21.r-o7ynqc.r-6416eg.r-1ny4l3l')
            element.click()
            print("削除2をクリックしました。")
            time.sleep(1)  # クリック後の待機時間

            return True
        
        elif item.text == "興味がない":
            print("トレンドに到達")
            #最初から
            mainloop()
            
        else:
            print("「削除」メニューアイテムが見つかりませんでした")
            # ESCキーを送信してモーダルをクローズ
            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            print("モーダルをクローズするためにESCキーを送信しました")
            
 # キー送信後の待機時間
            break

    return False

    
#削除処理
def delete_tweets():
    print("delete_tweets start")      
# "もっと見る"ボタンを見つけてクリックする
    more_buttons = driver.find_elements(By.CSS_SELECTOR, 'button[aria-label="もっと見る"]')
    print(f"取得した「もっと見る」ボタンの数: {len(more_buttons)}")
    
    for more_button in more_buttons:
        more_button.click()
        print("「もっと見る」ボタンをクリックしました。")
        more_buttons_count = len(driver.find_elements(By.CSS_SELECTOR, 'button[aria-label="もっと見る"]'))
        time.sleep(1)  # クリック後の読み込み待機


    # メニューアイテムを見つけて削除をクリックする
        if click_delete():
            print("削除が成功しました。")
        else:
            print("削除ボタンが見つかりませんでした")
        
        print("delete_tweets end")

    
    
def logic():
    while True:
        # 最初のArticleをゲットしてRTか判定する。  
        articles = driver.find_elements(By.TAG_NAME, "article")
        for article in articles:
            if is_RT():
                # RTをけす
                clear_rt()
                time.sleep(1)
                
            else:
                # RTではない自分のツイートなら消す
                delete_tweets()
        
    
          

        
#mainloop
def mainloop():

        init_driver(driver)
        logic()
        time.sleep(1)
        
                
try: 

    mainloop()

   
except Exception as e:
    print(f"予期せぬエラーが発生しました: {e}")
finally:
    driver.quit()


