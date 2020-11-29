import os
from selenium.webdriver import Chrome, ChromeOptions
import time
import pandas as pd
import eel
import datetime

## Chromeを起動する関数
def set_driver(driver_path,headless_flg):
    # Chromeドライバーの読み込み
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg==True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    #options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。
    return Chrome(executable_path=os.getcwd() + "\\" + driver_path,options=options)

### main処理
def main(genre):
    # driverを起動
    driver=set_driver("chromedriver.exe",False)
    # Webサイトを開く
    driver.get("https://www.amazon.co.jp/gp/bestsellers/{}/".format(genre))

    result = ''
    list_df = pd.DataFrame( columns = ["url","title","price"])

    es = driver.find_elements_by_class_name("zg-item-immersion")
    while True:
        for i in range(len(es)):
            try:
                link = driver.find_element_by_xpath("//*[@id=\"zg-ordered-list\"]/li[{}]/span/div/span/a".format(i+1))
                url = link.get_attribute("href")
                driver.get(url)
                title = driver.find_element_by_id("productTitle").text
                price_element = driver.find_elements_by_id("priceblock_ourprice")
                dealprice_element = driver.find_elements_by_id("priceblock_dealprice")
                if price_element:
                    price = price_element[0].text
                elif dealprice_element:
                    price = "セール価格" + dealprice_element[0].text
                else:
                    pirce = "品切れ"

                tmp_se = pd.Series( [url, title, price], index = list_df.columns)
                list_df = list_df.append( tmp_se, ignore_index = True)

                # price = "セール価格" + driver.find_element_by_id("priceblock_dealprice").text
                print(i)
                print(url + title + price)
                result += title + '\n'
                print(result)
                # time.sleep(2)
                driver.back()
            except:
                continue
                # result.append(title.text)
        next_btn = driver.find_elements_by_partial_link_text("次のページ")
        if next_btn:
            driver.get(next_btn[0].get_attribute("href"))
        else:
            # 現在時刻の取得
            now = datetime.datetime.now()
            # テキストファイルのパス
            path = 'csv_data/{}{}.csv'.format(now.strftime('%Y%m%d_%H%M%S'),genre)
            list_df.to_csv("csv_data/{}{}.csv".format(now.strftime('%Y%m%d_%H%M%S'),genre))
            driver.quit()
            break
        
    
    return result
    

### 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()
