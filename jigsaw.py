from tkinter import*
from tkinter.messagebox import*
import random
from enum import IntEnum
import os
from PIL import Image, ImageTk
import cv2 as cv
import numpy as np
import time
from prediction import Prediction
a = Prediction()


# 枚举法，方便后续操作
class Direction(IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


# 将图片导入矩阵中
class Square:
    def __init__(self, orderID):
        self.orderID = orderID

    def draw(self, canvas, board_pos):
        img = Pics[self.orderID]
        canvas.create_image(board_pos, image=img)


# 切图
def cut_image(image):
    # 读取图片大小
    img_width, img_height = image.size
    # 3*3图片每张图片的大小
    item_width = int(img_width / 3)
    box_list = []
    # 两重循环，生成9张图片基于原图的位置
    for item in range(0, 3):
        for j in range(0, 3):
            # 每张图片的位置
            box = (j * item_width, item * item_width, (j + 1) * item_width, (item + 1) * item_width)
            # 将图片位置信息存入一个列表中
            box_list.append(box)
    image_list = [image.crop(box) for box in box_list]
    # 利用save_images保存切割好的图
    save_images(image_list)


# 保存图片到文件夹方便读取
def save_images(image_list):
    save_path = 'D:/data/file2/file' + str(photo_num)
    if not os.path.exists(save_path):
        os.mkdir('D:/data/file2/file' + str(photo_num))
    index = 1
    for image in image_list:
        image.save(save_path + '/' + str(index) + '.png')
        index += 1


# 初始化拼图排版
def init_board():
    # L列表中[0,1,2,3,4,5,6,7,8]
    L = list(range(9))
    '''# 随机抠掉一张图
    n = random.randint(0, 8)'''
    # 填充拼图板
    for i in range(ROWS):
        for j in range(COLS):
            idx = i*ROWS+j
            orderID = L[idx]
            # 8号拼块不显示,所以存为None
            if orderID == 8:
                blocks[i][j] = None
            else:
                blocks[i][j] = Square(orderID)
    # 随机打乱拼图
    for i in range(500):
        random_num = random.randint(0, 3)
        move(Direction(random_num))
    cv.delete('all')


# 将拼图绘制在画布上
def drawBoard(canvas):
    canvas.create_polygon((0, 0, WIDTH, 0, WIDTH, HEIGHT, 0, HEIGHT), width=1, outline='White', fill='White')
    # 画所有图像块
    for i in range(ROWS):
        for j in range(COLS):
            if blocks[i][j] is not None:
                blocks[i][j].draw(canvas, (IMAGE_WIDTH*(j+0.5), IMAGE_HEIGHT*(i+0.5)))


# 通过键盘识别指令
def keyPressEvent(event):
    key = event.keysym
    if key == 'w':
        move(Direction.UP)
    if key == 's':
        move(Direction.DOWN)
    if key == 'a':
        move(Direction.LEFT)
    if key == 'd':
        move(Direction.RIGHT)
    '''# 进行到第十步的时候进行强制交换
    global steps
    if steps == 10:
        force_exchange()'''
    # 胜利后的选择
    if win():
        # 将每一次成功耗费的步数记录
        sore.append(steps)
        # 询问是否继续游戏
        question = askquestion(title="是否继续", message="是否要继续游戏？")
        if question == "yes":
            start()
        else:
            showinfo(title="再见", message="祝您愉快")
        best_sore()


# 移动空白快
def move(direction):
    # 空白块的位置
    global blank_row
    global blank_column
    for i in range(ROWS):
        for j in range(COLS):
            if blocks[i][j] is None:
                blank_row = i
                blank_column = j
    if direction == Direction.DOWN:
        if blank_row != 2:
            blocks[blank_row][blank_column] = blocks[blank_row + 1][blank_column]
            blocks[blank_row + 1][blank_column] = None
            temp = array[blank_row][blank_column]
            array[blank_row][blank_column] = array[blank_row + 1][blank_column]
            array[blank_row + 1][blank_column] = temp
            update()
    if direction == Direction.UP:
        if blank_row != 0:
            blocks[blank_row][blank_column] = blocks[blank_row - 1][blank_column]
            blocks[blank_row - 1][blank_column] = None
            temp = array[blank_row][blank_column]
            array[blank_row][blank_column] = array[blank_row - 1][blank_column]
            array[blank_row - 1][blank_column] = temp
            update()
    if direction == Direction.RIGHT:
        if blank_column != 2:
            blocks[blank_row][blank_column] = blocks[blank_row][blank_column + 1]
            blocks[blank_row][blank_column + 1] = None
            temp = array[blank_row][blank_column]
            array[blank_row][blank_column] = array[blank_row][blank_column + 1]
            array[blank_row][blank_column + 1] = temp
            update()
    if direction == Direction.LEFT:
        if blank_column != 0:
            blocks[blank_row][blank_column] = blocks[blank_row][blank_column - 1]
            blocks[blank_row][blank_column - 1] = None
            temp = array[blank_row][blank_column]
            array[blank_row][blank_column] = array[blank_row][blank_column - 1]
            array[blank_row][blank_column - 1] = temp
            update()


# 更新游戏版面
def update():
    global steps
    steps += 1
    label_step["text"] = "步数：" + str(steps)
    # 清除画布重新绘图
    cv.delete('all')
    drawBoard(cv)


# 判断胜利条件
def win():
    for i in range(ROWS):
        for j in range(COLS):
            if blocks[i][j] is not None and blocks[i][j].orderID != i * ROWS + j:
                return False
    return True


# 开始游戏
def start():
    init_board()
    # 存储本局游戏初始布局
    for item in range(3):
        for j in range(3):
            board[item][j] = blocks[item][j]
            array2[item][j] = array[item][j]
    play_game()


def play_game():
    global steps
    steps = 0
    label_step["text"] = "步数：" + str(steps)
    drawBoard(cv)


# 重新开始
def afresh():
    play_game()
    cv.delete('all')
    # 清除画布上的内容
    for item in range(3):
        for j in range(3):
            blocks[item][j] = board[item][j]
            array[item][j] = array2[item][j]
    drawBoard(cv)


# 历史纪录
def history():
    root_bank = Tk('bank')
    root_bank.title("历史成绩")
    width2 = 400
    height2 = 400
    screenwidth2 = root_bank.winfo_screenwidth()
    screenheight2 = root_bank.winfo_screenheight()
    location2 = '%dx%d+%d+%d' % (width2, height2, (screenwidth2 - width2) / 2, (screenheight2 - height2) / 2)
    root_bank.geometry(location2)
    len_sore = len(sore)
    if len_sore == 0:
        label_blank = Label(root_bank, text='当前没有历史纪录', font=('宋体', 20), fg='black', width=40, justify='center')
        label_blank.pack()
    else:
        sore_list = []
        for i in range(len_sore):
            sore_list.append("第%d次成绩：" % (i + 1) + str(sore[i]))
            label_sore = Label(root_bank, text=sore_list[i], font=('宋体', 15), fg="black", width=40)
            label_sore.grid(row=i, column=0)


# 历史最佳
def best_sore():
    global mvp
    if len(sore) != 0:
        if sore[-1] < mvp:
            mvp = sore[-1]
    else:
        mvp = '---'
    label_mvp["text"] = "历史最佳:" + str(mvp)
    label_mvp.pack(anchor='n', side='left')
    label_mvp.place(x=50, y=25)


# 退出游戏
def game_quit():
    q = askquestion(title='exit', message='你真的想退出游戏吗?')
    if q == 'yes':
        root.destroy()


# 帮助
def game_help():
    root_help = Tk('help')
    root_help.title('帮助')
    width2 = 400
    height2 = 100
    screenwidth2 = root_help.winfo_screenwidth()
    screenheight2 = root_help.winfo_screenheight()
    location2 = '%dx%d+%d+%d' % (width2, height2, (screenwidth2 - width2) / 2, (screenheight2 - height2) / 2)
    root_help.geometry(location2)
    label_help = Label(root_help, text='这是一个拼图游戏，你需要通过使用键盘上的w,s,d,a来控制'
                                       '游戏中的空白格，从而使图片还原成左侧的样子达到胜利，当你'
                                       '遇到困难时可以按提示键获取提示',
                       font=('宋体', 15), wraplength=350, justify='left')
    label_help.pack()


# 游戏信息
def game_info():
    root_info = Tk('info')
    root_info.title('game info')
    width2 = 400
    height2 = 100
    screenwidth2 = root_info.winfo_screenwidth()
    screenheight2 = root_info.winfo_screenheight()
    location2 = '%dx%d+%d+%d' % (width2, height2, (screenwidth2 - width2) / 2, (screenheight2 - height2) / 2)
    root_info.geometry(location2)
    label1 = Label(root_info, text='游戏名称：jigsaw', font=('宋体', 15), justify='left')
    label1.pack()
    label2 = Label(root_info, text='版本：1.0', font=('宋体', 15), justify='left')
    label2.pack()
    label3 = Label(root_info, text='制作时间：2020.10', font=('宋体', 15), justify='left')
    label3.pack()


# 其他信息
def other_info():
    root_other = Tk('other')
    root_other.title('other info')
    width2 = 300
    height2 = 100
    screenwidth2 = root_other.winfo_screenwidth()
    screenheight2 = root_other.winfo_screenheight()
    location2 = '%dx%d+%d+%d' % (width2, height2, (screenwidth2 - width2) / 2, (screenheight2 - height2) / 2)
    root_other.geometry(location2)
    label_info = Label(root_other, text='2018级软工实践K班第二次作业', font=('宋体', 15))
    label_info.pack()


# 强制交换
def force_exchange():
    global x1, x2, y1, y2
    x1 = random.randint(0, 2)
    x2 = random.randint(0, 2)
    y1 = random.randint(0, 2)
    y2 = random.randint(0, 2)
    n = blocks[x1][y1]
    blocks[x1][y1] = blocks[x2][y2]
    blocks[x2][y2] = n
    global steps
    steps -= 1
    update()
    showinfo(title='tip', message='两个方块发生交换了')
    '''bt_change = Button(root, text="撤销交换")
    bt_change.pack(anchor='w', side='left')
    bt_change.place(x=50, y=125, width=200)'''
    bt_history = Button(root, text="查看交换方块", command=exchange_view)
    bt_history.pack(anchor='w', side='left')
    bt_history.place(x=50, y=125, width=200)


# 查看交换的方块
def exchange_view():
    x = (x1+1)*(y1+1)
    y = (x2+1) * (y2+1)
    showinfo(title='1', message='在第十步的时候第' + str(x) + '块与第' + str(y) + '块发生了交换')


# AI演示
def AI_show():
    # 当游戏没有获胜时，不断执行下一步
    while not win():
        global blank_row
        global blank_column
        for i in range(ROWS):
            for j in range(COLS):
                if blocks[i][j] is None:
                    blank_row = i
                    blank_column = j
        reminde = a.pre_next(np.array(array), blank_row, blank_column)
        if reminde == 0:
            move(Direction.UP)
        if reminde == 1:
            move(Direction.LEFT)
        if reminde == 2:
            move(Direction.DOWN)
        if reminde == 3:
            move(Direction.RIGHT)
    if win():
        # 将每一次成功耗费的步数记录
        sore.append(steps)
        # 询问是否继续游戏
        question = askquestion(title="是否继续", message="是否要继续游戏？")
        if question == "yes":
            start()
        else:
            showinfo(title="再见", message="祝您愉快")
        best_sore()


# 提示
def reminder():
    global blank_row
    global blank_column
    for i in range(ROWS):
        for j in range(COLS):
            if blocks[i][j] is None:
                blank_row = i
                blank_column = j
    reminde = a.pre_next(np.array(array), blank_row, blank_column)
    if reminde == 0:
        move(Direction.UP)
    if reminde == 1:
        move(Direction.LEFT)
    if reminde == 2:
        move(Direction.DOWN)
    if reminde == 3:
        move(Direction.RIGHT)
    if win():
        # 将每一次成功耗费的步数记录
        sore.append(steps)
        # 询问是否继续游戏
        question = askquestion(title="是否继续", message="是否要进入下一关？")
        if question == "yes":
            start()
        else:
            showinfo(title="再见", message="祝您愉快")
        best_sore()


path = 'D:/data/file1'
picture_list = os.listdir(path)
picture_num = len(picture_list)
photo_num = random.randint(0, picture_num-1)
picture_path = path + '/' + picture_list[photo_num]
# 修改图片大小
img = cv.imread(picture_path)
p = cv.resize(img, (600, 600), interpolation=cv.INTER_CUBIC)
cv.imwrite(picture_path, p)
img = Image.open(picture_path)
cut_image(img)

# 定义常量
# 画布的尺寸
WIDTH = 600
HEIGHT = 600
# 图像块的边长
IMAGE_WIDTH = WIDTH//3
IMAGE_HEIGHT = HEIGHT//3
# 游戏的行/列数
ROWS = 3
COLS = 3
# 得分表
sore = []
# 移动步数
steps = 0
# 保存所有图像块的列表
blocks = [[0, 1, 2],
          [3, 4, 5],
          [6, 7, 8]]
# 存储初始图像
board = [[0, 1, 2],
         [3, 4, 5],
         [6, 7, 8]]
# 数字
array = [[1, 2, 3],
         [4, 5, 6],
         [7, 8, 9]]
# 存储初始数字
array2 = [[1, 2, 3],
         [4, 5, 6],
         [7, 8, 9]]

# 创建主窗口
root = Tk('jigsaw')
root.title("华容道")

# 创建菜单
menubar = Menu(root)
# 添加菜单内容
fmenu1 = Menu(root)
fmenu1.add_command(label='开始游戏', command=start)
fmenu1.add_command(label='重置本关', command=afresh)
fmenu1.add_command(label='退出游戏', command=game_quit)
fmenu2 = Menu(root)
fmenu2.add_command(label='历史成绩', command=history)
fmenu2.add_command(label='帮助', command=game_help)
fmenu3 = Menu(root)
fmenu3.add_command(label='游戏信息', command=game_info)
fmenu3.add_command(label='其他说明', command=other_info)

menubar.add_cascade(label="游戏", menu=fmenu1)
menubar.add_cascade(label="查看", menu=fmenu2)
menubar.add_cascade(label="关于", menu=fmenu3)
root.config(menu=menubar)

# 设置窗口居中
width = 900
height = 600
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
location = '%dx%d+%d+%d' % (width, height, (screenwidth-width)/2, (screenheight-height)/2)
root.geometry(location)
root.resizable(width=False, height=False)

# 将切割好的小图存入空列表
Pics = []
for i in range(9):
    filename = "D:/data/file2/file"+str(photo_num)+'/'+str(i+1)+".png"
    Pics.append(PhotoImage(file=filename))

# 设置按钮
bt_AI = Button(root, text='一键通关', command=AI_show)
bt_AI.pack(anchor='w', side='left')
bt_AI.place(x=50, y=225, width=200)
bt_again = Button(root, text="重置本关", command=afresh)
bt_again.pack(anchor='w', side='left')
bt_again.place(x=50, y=275, width=200)
bt_reminder = Button(root, text="提示下一步", command=reminder)
bt_reminder.pack(anchor='w', side='left')
bt_reminder.place(x=50, y=175, width=200)

# 原图形状
image = cv.imread(picture_path)
p = cv.resize(image, (200, 200), interpolation=cv.INTER_CUBIC)
cv.imwrite(picture_path, p)
image_origin = Image.open(picture_path)
photo = ImageTk.PhotoImage(image_origin)
label_photo = Label(root, image=photo)
label_photo.place(x=50, y=350, width=200)

# 设置文本框
label_txt = Label(root, text="你将拼成下图形状：")
label_txt.place(x=50, y=325)
label_step = Label(root, text="步数："+str(steps), fg="red")
label_step.pack(anchor='n', side='left')
label_step.place(x=50, y=50)
mvp = 999
label_mvp = Label(root, text="历史最佳:---", fg="red")
label_mvp.pack(anchor='n', side='left')
label_mvp.place(x=50, y=25)

cv = Canvas(root, bg='black', width=WIDTH, height=HEIGHT)
# 通过键盘进行控制
cv.bind("<Key>", keyPressEvent)
# 聚焦在画布上
cv.focus_set()
cv.pack(side='right')

root.mainloop()