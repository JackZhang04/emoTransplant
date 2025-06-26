"""
自动完成获取窗口，完成鼠标操作并将微信文件传输助手的gif图片添加到表情包
"""

# pygetwindow获取窗口
# pyautogui模拟鼠标操作
import pygetwindow as gw
import pyautogui as pag
from time import sleep
import os

def intialize_settings():
    """初始化窗口，让窗口始终保持在前台并且检查和调整窗口位置和大小"""
    wx = gw.getWindowsWithTitle('微信')[0]
    wx.minimize()
    wx.restore()   # 让微信窗口保持在前台
    sleep(1)
    wx.resizeTo(1050, 750)  # 调整窗口大小
    wx.moveTo(0, 0)  # 移动窗口到屏幕左上角
    return wx

def auto_add(times, tol=5):
    count = 0
    tolerance = tol

    """自动添加表情包脚本"""
    wx = intialize_settings()
    # 确保用户已经将微信头像png图片放在程序同一目录下
    if not os.path.exists('headshot.png'):
        print("请将微信头像png图片放在程序同一目录下，并将其命名为headshot.png！")
        raise FileNotFoundError("微信头像图片未找到！")

    while count < times and tolerance > 0:
        if (gw.getActiveWindowTitle() != '微信'):
            wx.minimize()
            wx.restore() 
        
        findornot = False

        for pos in pag.locateAllOnScreen('headshot.png', region = (0,0,1050,750)):
            x = pos.left - 70
            y = pos.top + 10
            pag.moveTo(x, y)
            pag.rightClick()
            sleep(0.5)
            if pag.pixelMatchesColor(x+40, y+42, (237, 237, 237)):
                pag.moveTo(x+20, y+20)
                pag.click()
                sleep(0.5)
                count += 1 # 计数+1
                findornot = True # 找到可添加表情
                print(f'添加成功，当前添加表情数量：{count}')

            else:
                print('该表情已添加')
                pag.moveTo(x-10, y-10)
                pag.click()
                sleep(0.5)

        pag.scroll(250)
        sleep(0.5)
        
        if not findornot:
            tolerance -= 1
        else:
            tolerance = tol

    print('添加完毕')

if __name__ == '__main__':
    try:
        times = int(input('请输入要添加的表情包数量：'))
        if times <= 0:
            raise ValueError("数量必须大于0")
        auto_add(times)
    except ValueError as e:
        print(f"输入错误: {e}")
    except Exception as e:
        print(f"发生错误: {e}")
        