import random
import time
from io import BytesIO

from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains


class BilibiliLogin:
    def __init__(self,url,username,password):
        self.url = url
        self.username = username
        self.password = password
        self.slideLength = None
        self.driver = None
        self.cookies = None
        self.retry = 0


    def driver_init(self):
        """
        浏览器初始化：
            设置浏览器、浏览器的选项
        """
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36')
        self.driver = webdriver.Chrome(options=options)


    def biliLogin(self):
        """
        登录操作：
            进入首页
            进入登录页
            输入账号密码
            滑动验证码
            若登录失败会重试2次
        """
        print("正在登录...")
        self.driver_init()
        self.driver.get(self.url) # 导航到一个页面
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="internationalHeader"]/div[1]/div/div[3]/div[2]/div[1]/div/span/div/span').click() # 进入登录
        self.driver.switch_to.window(self.driver.window_handles[-1]) # 切换窗口
        self.inputID(self.username,self.password) # 输入账号密码
        self.slideCheck() # 滑动验证码
        self.driver.switch_to.window(self.driver.window_handles[-1])  # 切换窗口
        try:
            self.driver.find_element_by_css_selector("[class='user-con signin']")
            print("登录成功！")
            self.cookies = self.driver.get_cookies()
            return True
        except:
            if self.retry < 2:
                self.retry += 1
                print("登录失败，重试中...")
                self.driver.quit()
                self.biliLogin()
            else:
                print("登陆失败次数达3次，请检查代码")
                return False


    def inputID(self,username,password):
        """
        输入账号密码：
            通过xpath找到元素然后填入值、点击登录
        """
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="login-username"]').send_keys(username)
        self.driver.find_element_by_xpath('//*[@id="login-passwd"]').send_keys(password)
        self.driver.find_element_by_xpath('//*[@id="geetest-wrap"]/div/div[5]/a[1]').click()  # 点击登录


    def slideCheck(self):
        """
        滑动验证码：
            获取长度后随机等长分割，随机休眠时间来模拟拖动滑块效果
        """
        self.slideLength = self.getDistance()
        slider = self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[6]/div/div[1]/div[2]/div[2]')
        ActionChains(self.driver).move_to_element(slider).perform()
        time.sleep(random.random())
        ActionChains(self.driver).click_and_hold(slider).perform()
        randN = random.randint(5,8)
        l = self.slideLength / randN
        for i in range(randN):
            # 纵坐标随机晃动通过机器验证
            ActionChains(self.driver).move_by_offset(xoffset=l,yoffset=random.randint(-2,2)).perform()
            ActionChains(self.driver).click_and_hold(slider).perform()
            time.sleep(random.random()/100)
        time.sleep(random.random())
        ActionChains(self.driver).release(slider).perform()
        time.sleep(5)


    def getDistance(self):
        """
        获得滑动距离：
            获得原图和缺图
            通过对比原图和缺图像素点RGB的差值，如果差值之和大于一个阈值(60)说明在缺图中该处是缺块或者拼块
            按区域搜索缺块到左边界的距离x和拼块到左边界的距离x0，二者距离之差就是滑动距离
        :return: x-x0
        """
        time.sleep(1)
        cutImg = self.getCutImg()
        fullImg = self.getFullImg()
        cutImg.save('cut.png')
        fullImg.save('full.png')
        cutPixies = cutImg.load()
        fullPixies = fullImg.load()
        width, height = fullImg.size
        print(width,height)
        x=0
        y=0
        # 计算灰块的x
        for i in range(int((1/4)*width),width):
            for j in range(int((1/5)*height),int((4/5)*height)):
                c = cutPixies[i, j]
                f = fullPixies[i, j]
                if abs(f[0] - c[0]) + abs(f[1] - c[1]) + abs(f[2] - c[2]) > 60:
                    # print(f[0],f[1],f[2])
                    # print(c[0],c[1],c[2])
                    x=i
                    y=j
                    break
            else:
                continue
            break
        print(x,y)
        # 计算拼图的x
        x0=0
        y0=0
        for i in range(int((1/4)*width)):
            c = cutPixies[i, y]
            f = fullPixies[i, y]
            if abs(f[0] - c[0]) + abs(f[1] - c[1]) + abs(f[2] - c[2]) > 60:
                # print(f[0], f[1], f[2])
                # print(c[0], c[1], c[2])
                x0=i
                y0=y
                break
        print(x0,y0)
        print(x-x0)
        return x-x0


    def getCutImg(self):
        """
        获取缺图：
            直接用xpath找到canvas然后截图就是缺图
        """
        time.sleep(2)
        cutImg = self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[6]/div/div[1]/div[1]/div/a/div[1]/div/canvas[1]').screenshot_as_png
        return Image.open(BytesIO(cutImg))


    def getFullImg(self):
        """
        获取原图：
            执行js可以显示原图，截图后把原图改回缺图
        """
        self.driver.execute_script("$('.geetest_canvas_fullbg.geetest_fade.geetest_absolute')[0].style.display='block'")
        time.sleep(2)
        fullImg = self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[6]/div/div[1]/div[1]/div/a/div[1]/div/canvas[1]').screenshot_as_png
        self.driver.execute_script("$('.geetest_canvas_fullbg.geetest_fade.geetest_absolute')[0].style.display='none'")
        time.sleep(1)
        return Image.open(BytesIO(fullImg))

    @property
    def driver(self):
        return self._driver

    @driver.setter
    def driver(self, value):
        self._driver = value

    @property
    def cookies(self):
        return self._cookies

    @cookies.setter
    def cookies(self, value):
        self._cookies = value





