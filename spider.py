from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class JTWZ:
    def __init__(self, carAuthCode, carNum):
        """
        :param carAuthCode:车辆识别码
        :param carNum: 车牌号
        """
        self.driver = webdriver.Chrome('/home/feng/chromedriver_linux64/chromedriver')
        self.url = 'http://xxcx.hbsjg.gov.cn:8087/hbjj/'
        self.carAuthCode = carAuthCode
        self.carNum = carNum

    def get_content(self):
        self.driver.get(self.url)
        try:
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "checkCode1")))
            print(u"开始登录...")
        except Exception as e:
            print(e)
        self.carNum1 = self.driver.find_element_by_id('carNum1')
        self.carNum1.send_keys(self.carNum)
        self.carAuthCode1 = self.driver.find_element_by_id('carAuthCode1')
        self.carAuthCode1.send_keys(self.carAuthCode)
        captcha1 = self.driver.find_element_by_id('captcha1')
        # 从cookies找寻验证码
        for n in self.driver.get_cookies():
            if n.get('name') != None and n['name'] == 'RANDOMVALIDATECODEKEY1':
                checkCode1 = n['value']
                captcha1.send_keys(checkCode1)
                sub = self.driver.find_element_by_xpath("//input[@value='开始查询']")
                sub.click()
                try:
                    element = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "fsmiddle")))
                    print(u'获取违章内容成功，保存：wz.jpg...')
                    self.driver.save_screenshot('wz.jpg')
                    return 0
                except:
                    print(u'获取失败...')
                    return 1
                finally:
                    self.driver.quit()


if __name__ == '__main__':
    jtws = JTWZ(carAuthCode=000, carNum='')
    jtws.get_content()
