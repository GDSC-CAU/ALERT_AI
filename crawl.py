from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import urllib.request
import os

query = 'Nutria'
PAUSE_TIME = 5
new_height = 0
last_height = 0

chrome_options = webdriver.ChromeOptions()
chrome_options.binary = 'C://chromedriver_win32/chromedriver.exe'
driver = webdriver.Chrome()
driver.get(f'https://www.google.com/imghp')
search_bar = driver.find_element(By.NAME,"q")
search_bar.send_keys(query)
search_bar.submit()

last_height = driver.execute_script("return document.body.scrollHeight")

while True :
    driver.execute_script("window.scrollBy(0,50000)")
    time.sleep(PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height > last_height:
        last_height = new_height
        continue
    else :
        break

img_elements = driver.find_elements(By.CSS_SELECTOR,".rg_i")
imgs = []

for idx, img in enumerate(img_elements) :
    print(f"{query} : {idx+1}/{len(img_elements)} proceed...")
    try :
        img.click()
        time.sleep(PAUSE_TIME)
        # 에러 시 직접 개발자 도구 F12 활용해서 XPATH 추출한 뒤에 값을 변경
        img_element = driver.find_element(By.XPATH, '//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[3]/div[1]/a/img[1]')
        img_src = img_element.get_attribute('src')
        img_alt = img_element.get_attribute('alt')
        imgs.append({
            'alt' : img_alt,
            'src' : img_src
        })
        
    except :
        print(f'err: {idx}')
        pass

driver.close()

save_path = f'C://Users//CAU//Desktop//Alert//image//{query}'
if not os.path.exists(save_path):
    os.mkdir(save_path)

for idx, one in enumerate(imgs):
    try : 
        src = one['src']
        alt = one['alt']
        urllib.request.urlretrieve(src,  f"{save_path}\{query}_{idx}.png")
        print(idx, alt)
    except:
        print(idx, " Error")
        pass
print('crawling finished')
