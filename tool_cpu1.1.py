from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os

def init_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # 无头模式
    # options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_experimental_option('detach', True)
    options.add_argument("--log-level=3")  # 只显示 FATAL 级别错误（最小日志）
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    wd = webdriver.Chrome(options=options)
    wd.implicitly_wait(5)
    return wd

def excute_data(wd,data):
    socNames = wd.find_elements(By.CLASS_NAME,"socName")
    socNames.__delitem__(0)
    socre = wd.find_elements(By.CSS_SELECTOR,".ratio > a")
    for i in range(len(socNames)):
      data["cpu名称"].append(socNames[i].text)
      data["跑分"].append(socre[i].text)
    return data


if __name__ == "__main__":
    data = {
        "cpu名称":[],
        "跑分":[]
    }
    # 新建
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, "cpu_data.xlsx")

    writer = pd.ExcelWriter(file_path, engine='openpyxl')
    url = input('输入需要爬取的url:')
    # url = 'https://www.socpk.com/cpu/?brand=phone'
    wd = init_driver()
    wd.get(url)
    frame_count = len(wd.find_elements(By.XPATH,"//a[@class='downBtn']"))

    for i in range(frame_count):
        frames = wd.find_elements(By.XPATH,"//a[@class='downBtn']")
        sheet_name = frames[i].text[:31]  # Excel sheet名称最多31个字符
        frames[i].click()
        data = excute_data(wd,data)

        print(f"处理完第{i+1}页数据")

        df = pd.DataFrame(data)
        df.to_excel(writer,sheet_name=sheet_name,index=False)

        data = {"cpu名称":[],"跑分":[]}
    writer.close()
    print(f"所有数据已成功保存到 {file_path}")
    wd.quit()


 
