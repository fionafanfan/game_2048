# -*-coding:utf-8-*-
# @作   者: fionafanfan
# @创建时间: 2023/6/23 20:28
# @项目名称: codes
# @文件名称：game_2048.py 
# @描   述: 2048游戏
import os
import sys
import random
import time
import copy
import tkinter as tk


class TkGUI2048(object):
    """
    top: D9D1E0
    back_page: B49FAC
    0: E9D4D1
    2: D8D7FF
    4: E5E0EA
    8: FBB4BA
    16: FF9B8B
    32: FF7261
    64: F3D8A9
    128: F7C679
    256:FF9B44
    512: FF7019
    1024:FF4001

    重置： 9D99A8，
    字体 ； D3D5FE
    """

    def __init__(self, top=None, seats=None, max_num=0, cur_num=0, move_num=0, play_keybord=None, play_up=None, play_down=None, play_left=None, play_right=None, quit=None, reset=None):
        """
        This class configures and populates the toplevel window.
        top is the toplevel containing window.
        """
        self.top = top
        if not seats:
            seats = [0 for i in range(16)]
        self.seats = seats
        self.max_num = max_num
        self.cur_num = cur_num
        self.move_num = move_num
        self.play_keybord = play_keybord
        self.play_up = play_up
        self.play_down = play_down
        self.play_left = play_left
        self.play_right = play_right

        self.quit = quit
        self.reset = reset

        self.Frame_game_root = None
        self.Label_num = None

        self.Label_max = None
        self.Label_cur = None

        self.Button_up = None
        self.Button_down = None
        self.Button_left = None
        self.Button_right = None

        self.Button_exit = None
        self.Button_reset = None

        self.draw_game_root_page()
        self.draw_game_num_page()
        self.draw_command_button()
        self.draw_keybord_label()
        self.draw_records()

    def draw_game_root_page(self):
        self.top.geometry("600x450+539+43")
        self.top.minsize(120, 1)
        self.top.maxsize(3004, 1901)
        self.top.resizable(0, 0)
        self.top.title("2048")
        self.top.configure(background="#D9D1E0")

    def draw_game_num_page(self, seats=None):
        if seats:
            self.seats = seats

        self.Frame_game_root = tk.Frame(self.top)
        self.Frame_game_root.place(x=10, y=10, height=410, width=410)
        self.Frame_game_root.configure(relief='groove', borderwidth="2", background="#B49FAC")

        label_num_size = 90
        label_num_x_size = 10  # 横轴间隔10
        label_num_y_siee = 10   # 纵轴间隔10
        label_num_x_size_map = [label_num_x_size, label_num_x_size+1*label_num_size, label_num_x_size+2*label_num_size, label_num_x_size+3*label_num_size]
        label_num_y_size_map = [label_num_y_siee, label_num_y_siee+1*label_num_size, label_num_y_siee+2*label_num_size, label_num_y_siee+3*label_num_size]
        num_color_map = {
            0: "#E9D4D1",
            2: "#6580f4", 4: "#E5E0EA", 8: "#FBB4BA", 16: "#FF9B8B",
            32: "#FF7261", 64: "#F3D8A9", 128: "#F7C679", 256: "#FF9B44", 512: "#FF7019", 1024: "#FF4001",
            2048: "#ff0040", 4096: "#640034"
        }

        label_num_css_map = {
            0: {"x": label_num_x_size_map[0], "y": label_num_y_size_map[0]}, 1: {"x": label_num_x_size_map[1], "y": label_num_y_size_map[0]}, 2: {"x": label_num_x_size_map[2], "y": label_num_y_size_map[0]}, 3: {"x": label_num_x_size_map[3], "y": label_num_y_size_map[0]},
            4: {"x": label_num_x_size_map[0], "y": label_num_y_size_map[1]}, 5: {"x": label_num_x_size_map[1], "y": label_num_y_size_map[1]}, 6: {"x": label_num_x_size_map[2], "y": label_num_y_size_map[1]}, 7: {"x": label_num_x_size_map[3], "y": label_num_y_size_map[1]},
            8: {"x": label_num_x_size_map[0], "y": label_num_y_size_map[2]}, 9: {"x": label_num_x_size_map[1], "y": label_num_y_size_map[2]}, 10: {"x": label_num_x_size_map[2], "y": label_num_y_size_map[2]}, 11: {"x": label_num_x_size_map[3], "y": label_num_y_size_map[2]},
            12: {"x": label_num_x_size_map[0], "y": label_num_y_size_map[3]}, 13: {"x": label_num_x_size_map[1], "y": label_num_y_size_map[3]}, 14: {"x": label_num_x_size_map[2], "y": label_num_y_size_map[3]}, 15: {"x": label_num_x_size_map[3], "y": label_num_y_size_map[3]},
        }

        for i in range(16):
            self.Label_num = tk.Label(self.Frame_game_root)
            self.Label_num.place(x=label_num_css_map.get(i).get('x'), y=label_num_css_map.get(i).get('y'),
                                 height=label_num_size, width=label_num_size)

            background = num_color_map.get(self.seats[i])
            text = str(self.seats[i]) if self.seats[i] else ""
            self.Label_num.configure(activebackground="#ab5858", activeforeground="#000000",
                                       anchor='w', background=background, compound='center',
                                       border=1,
                                       disabledforeground="#a3a3a3",
                                       font="-family {High Tower Text} -size 36 -weight bold",
                                       foreground="#000000",
                                       relief="solid",
                                       text=text)

    def draw_command_button(self):
        self.Button_exit = tk.Button(self.top)
        self.Button_exit.place(x=510, y=370, height=28, width=49)
        self.Button_exit.configure(activebackground="#793e3e", activeforeground="#793e3e",
                                   background="#b16363", compound='left', disabledforeground="#a3a3a3",
                                   foreground="#000000",
                                   highlightbackground="#d9d9d9",
                                   highlightcolor="black",
                                   pady="0",
                                   text='''退出''',
                                   command=self.quit
                                   )

        self.Button_reset = tk.Button(self.top)
        self.Button_reset.place(x=440, y=370, height=28, width=49)
        self.Button_reset.configure(activebackground="#793e3e", activeforeground="#793e3e",
                                    background="#b16363", compound='left', disabledforeground="#a3a3a3",
                                    foreground="#000000",
                                    highlightbackground="#d9d9d9",
                                    highlightcolor="black",
                                    pady="0",
                                    text='''重置''',
                                    command=self.reset
                                    )

        self.Button_up = tk.Button(self.top)
        self.Button_up.place(x=470, y=150, height=28, width=49)
        self.Button_up.configure(activebackground="beige", activeforeground="black",
                                 background="#b16363", compound='left', cursor="fleur",
                                 foreground="#000000", highlightbackground="#d9d9d9",
                                 highlightcolor="black", pady="0", text='''上''',
                                 command=self.play_up
                                 )

        self.Button_down = tk.Button(self.top)
        self.Button_down.place(x=470, y=250, height=28, width=49)
        self.Button_down.configure(activebackground="beige", activeforeground="black",
                                    background="#b16363", compound='left', cursor="fleur",
                                    foreground="#000000", highlightbackground="#d9d9d9",
                                    highlightcolor="black", pady="0", text='''下''',
                                   command=self.play_down
                                    )

        self.Button_left = tk.Button(self.top)
        self.Button_left.place(x=430, y=200, height=28, width=49)
        self.Button_left.configure(activebackground="beige", activeforeground="black",
                                    background="#b16363", compound='left', cursor="fleur",
                                    foreground="#000000", highlightbackground="#d9d9d9",
                                    highlightcolor="black", pady="0", text='''左''',
                                   command=self.play_left
                                   )

        self.Button_right = tk.Button(self.top)
        self.Button_right.place(x=520, y=200, height=28, width=49)
        self.Button_right.configure(activebackground="beige", activeforeground="black",
                                    background="#b16363", compound='left', cursor="fleur",
                                    foreground="#000000", highlightbackground="#d9d9d9",
                                    highlightcolor="black", pady="0", text='''右''',
                                    command=self.play_right
                                    )

    def draw_keybord_label(self):
        """
        label邦健键盘事件，来控制移动方向
        """
        self.Label_keybord_event = tk.Label(self.top)
        # self.Label_keybord_event.place(x=430, y=10, height=33, width=80)
        # self.Label_keybord_event.configure(anchor='w',
        #                                    compound='left',
        #                                     cursor="fleur",
        #                                    highlightbackground="white",  # 设置为白色
        #                                    highlightthickness=0  # 透明度不可见
        #                                    )

        self.Label_keybord_event.focus_set()
        self.Label_keybord_event.pack()
        self.Label_keybord_event.bind('<Key>', self.play_keybord)
        pass

    def draw_records(self, cur_num=0, move_num=-1):
        if cur_num:
            self.cur_num = cur_num
        if move_num != -1:
            self.move_num = move_num

        self.Label_max = tk.Label(self.top)
        self.Label_max.place(x=430, y=10, height=33, width=80)
        self.Label_max.configure(anchor='w', background="#b16363", compound='left',
                                 cursor="fleur", disabledforeground="#a3a3a3",
                                 foreground="#000000", text=f'''最高：{str(self.max_num)}''')

        self.Label_cur = tk.Label(self.top)
        self.Label_cur.place(x=430, y=60, height=33, width=80)
        self.Label_cur.configure(anchor='w', background="#b16363", compound='left',
                                 cursor="fleur", disabledforeground="#a3a3a3",
                                 foreground="#000000", text=f'''当前：{str(self.cur_num)}''')

        self.Label_move = tk.Label(self.top)
        self.Label_move.place(x=430, y=110, height=33, width=80)
        self.Label_move.configure(anchor='w', background="#b16363", compound='left',
                                 cursor="fleur", disabledforeground="#a3a3a3",
                                 foreground="#000000", text=f'''移动：{str(self.move_num)}''')

    def run(self):
        self.top.mainloop()


class Game2048(object):
    """
    2048游戏大概玩法：
    有4*4=16个方格位置， 刚入场会随机初始化1-2个数，分别是2或者4， 位置随机。
    通过上下左右滑动，控制界面上的数字成倍相加， 数的范围：
    【2、4、8、16、32、64、128、256、512、1024、2048】
    通过上下左右滑动，让最后界面上有的最大数越大，就会越有成就感，其实就是另一种有目标的消消乐，
    当界面的空格数越来越少，就越难滑动，最后没有空格为止，就划不动，代表游戏失败。
    我用了2周的时间认真的玩了下， 后面能够比较有概率的玩到1024， 再往后，就没有达到过了，
    到后面就很难玩动， 最佳战绩就是【1024、512、256、128、64、32、16、8、4、2】 数字都有，
    但是它们合并不到一块去， 所以最后还是游戏结束掉了，所以想要通过仔细研究下算法， 将这个游戏玩通关掉。
    顺便写一个简易的python版的2048。

    1行:[0, 1, 2, 3]
    2行:[4, 5, 6, 7]
    3行:[8, 9, 10, 11]
    4行:[12, 13, 14, 15]
    up = [[0, 4, 8, 12], [1, 5, 9, 13], [2, 6, 10, 14], [3, 7, 11, 15]]
    down = [[12, 8, 4, 0], [13, 9, 5, 1], [14, 10, 6, 2], [15, 11, 7, 3]]
    left = [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
    right = [[3, 2, 1, 0], [7, 6, 5,4], [11, 10, 9, 8], [15, 14, 13, 12]]

    如果4行数据都没有产生任何计算及唯一，则代表这个方向不能进行移动， 不能产生新的数，改变局面
    0|0|0|0-> 没有计算， 没有位移
    2|4|8|16-> 没有计算， 没有位移
    2|2|2|2 -> 4|4|0|0

    2|2|2|4-> 4|2|4|0

    2|2|4|8-> 4|4|8|0
    2|2|4|4-> 4|8|0|0
    2|4|8|8-> 2|4|16|0
    """
    def __init__(self):
        self.default_val = 0
        self.temp_seats = [self.default_val for i in range(16)]  # 临时区
        self.all_seats = [self.default_val for i in range(16)]  # 改变后的

        self.up = [[0, 4, 8, 12], [1, 5, 9, 13], [2, 6, 10, 14], [3, 7, 11, 15]]
        self.down = [[12, 8, 4, 0], [13, 9, 5, 1], [14, 10, 6, 2], [15, 11, 7, 3]]
        self.left = [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
        self.right = [[3, 2, 1, 0], [7, 6, 5, 4], [11, 10, 9, 8], [15, 14, 13, 12]]
        self.game_2048_play = None
        self.cur_num = 0
        self.move_num = 0  # 有效的操作次数

    def gen_new_nums(self, indexs):
        # 随机选取1-2个数， 赋值给1-2个空格位置
        n_num = random.randint(1, 2)
        low_n_vals = [random.choices([2, 4], weights=[0.8, 0.6])[0] for i in range(1, n_num+1)]
        low_n_indexs = [random.choices(indexs)[0] for i in range(1, n_num+1)]
        # print(f"随机新增:{n_num}个数:{low_n_vals} , 放在方格位置：{low_n_indexs}")
        for i, val in enumerate(low_n_vals):
            self.all_seats[low_n_indexs[i]] = val

    def _init_game_2048(self):
        self.all_seats = [self.default_val for i in range(16)]  # 改变后的
        self.gen_new_nums([i for i in range(16)])

    def play_caculate(self, direction_indexs):
        new_lines_val_list = []
        zero_index_list = []
        self.temp_seats = copy.deepcopy(self.all_seats)
        for n, line in enumerate(direction_indexs):
            line_val_list = [self.all_seats[line[i]] for i in range(4) if self.all_seats[line[i]]]  # 当前局面的当前行或列所有值
            new_line_val_list = []   # 每一行或每一列通过位移或计算后的值
            if len(line_val_list) == 0 or len(line_val_list) == 1:
                new_line_val_list = line_val_list
            elif len(line_val_list) == 2:
                if line_val_list[0] == line_val_list[1]:
                    new_line_val_list = [sum(line_val_list)]
                else:
                    new_line_val_list = line_val_list
            elif len(line_val_list) == 3:
                if line_val_list[0] == line_val_list[1]:
                    new_line_val_list = [sum(line_val_list[:2]), line_val_list[2]]
                elif line_val_list[1] == line_val_list[2]:
                    new_line_val_list = [line_val_list[0], sum(line_val_list[1:])]
                else:
                    new_line_val_list = line_val_list
            elif len(line_val_list) == 4:
                if line_val_list[0] == line_val_list[1]:
                    new_line_val_list.append(sum([line_val_list[0], line_val_list[1]]))
                    if line_val_list[2] == line_val_list[3]:
                        new_line_val_list.append(sum([line_val_list[2], line_val_list[3]]))
                    else:
                        new_line_val_list.extend([line_val_list[2], line_val_list[3]])
                elif line_val_list[1] == line_val_list[2]:
                    new_line_val_list = [line_val_list[0], sum([line_val_list[1], line_val_list[2]]), line_val_list[3]]
                elif line_val_list[2] == line_val_list[3]:
                    new_line_val_list = [line_val_list[0], line_val_list[1], sum([line_val_list[2], line_val_list[3]])]
                else:
                    new_line_val_list = line_val_list

            new_line_val_list.extend([0 for i in range(4 - len(new_line_val_list))])
            new_lines_val_list.append(new_line_val_list)
            for i, new_line_val in enumerate(new_line_val_list):
                if not new_line_val:
                    zero_index_list.append(line[i])
                self.all_seats[line[i]] = new_line_val

            # 变换前后局面上的值有变化，才能随机在剩余的空间中生成新的数值
        if self.all_seats != self.temp_seats:
            self.gen_new_nums(zero_index_list)
            self.move_num += 1

    def play_up(self):
        self.play_caculate(self.up)

    def play_down(self):
        self.play_caculate(self.down)

    def play_left(self):
        self.play_caculate(self.left)

    def play_right(self):
        self.play_caculate(self.right)

    def draw_2048(self):
        """
        绘制面板
        :return:
        """

    def reset(self):
        """
        重置
        :return:
        """
        pass

    def quit(self):
        """退出"""
        print("== 退出 ==")
        sys.exit(-1)

    def play(self):
        """
        开始
        :return:
        """
        pass


class CmdGame2048(Game2048):

    def __init__(self):
        super(CmdGame2048, self).__init__()

    def draw_2048(self):
        os.system('cls')
        r = 1
        for i in range(1, 17):
            if i % 4 == 0:
                print(f"{str(r)}行:{self.all_seats[i-4:i]}")
                r += 1

    def play_caculate(self, direction_indexs):
        super(CmdGame2048, self).play_caculate(direction_indexs)
        self.draw_2048()

    def play(self):
        """
        开始
        :return:
        """
        self._init_game_2048()
        self.draw_2048()
        while True:
            step = input(f"请输入命令（w-上、s-下、a-左、d-右、 r-重置、q-退出 ）:")
            if step == 'w':
                self.play_up()
            elif step == 's':
                self.play_down()
            elif step == 'a':
                self.play_left()
            elif step == 'd':
                self.play_right()
            elif step == 'r':
                self.reset()
            elif step == 'q':
                self.quit()
            else:
                print(f"输入命令【{step}】出错")
            time.sleep(0.1)


class GuiTkGame2048(Game2048):

    def __init__(self):
        super(GuiTkGame2048, self).__init__()

    def draw_2048(self):
        if self.game_2048_play:
            self.cur_num = max(self.all_seats)  # 当前最大值
            self.game_2048_play.draw_records(cur_num=self.cur_num, move_num=self.move_num)
            self.game_2048_play.draw_game_num_page()

    def play_caculate(self, direction_indexs):
        super(GuiTkGame2048, self).play_caculate(direction_indexs)
        self.draw_2048()

    def play_keybord(self, evt):
        # msg = f"您点击了{evt.char}, ASCII代码{evt.keycode}\n"
        # msg += f"按键名称{evt.keysym}, 代码{evt.keysym_num}"
        if evt.keysym == 'Up':
            self.play_up()
        elif evt.keysym == 'Down':
            self.play_down()
        elif evt.keysym == 'Left':
            self.play_left()
        elif evt.keysym == 'Right':
            self.play_right()

    def reset(self):
        """
        重置
        :return:
        """
        if self.game_2048_play:
            self._init_game_2048()
            self.cur_num = max(self.all_seats)  # 当前最大值
            self.move_num = 0
            self.game_2048_play.draw_records(cur_num=self.cur_num, move_num=self.move_num)
            self.game_2048_play.draw_game_num_page(seats=self.all_seats)

    def play(self):
        init_top = tk.Tk()
        self._init_game_2048()
        # init_seats = [0, 0, 0, 0, 0, 0, 0, 16, 0, 0, 0, 4, 32, 64, 64, 0]  # 临时修改初始值
        # self.all_seats = init_seats
        self.cur_num = max(self.all_seats)  # 当前最大值
        self.game_2048_play = TkGUI2048(top=init_top, seats=self.all_seats, max_num=2048, cur_num=self.cur_num, move_num=self.move_num,
                                      play_keybord=self.play_keybord,
                                      play_up=self.play_up, play_down=self.play_down,
                                      play_left=self.play_left, play_right=self.play_right,
                                      quit=self.quit,
                                      reset=self.reset
                                      )
        self.game_2048_play.run()


if __name__ == "__main__":
    # game_2048 = CmdGame2048()  # 命令行模式
    game_2048 = GuiTkGame2048()  # tkinter实现的图形界面模式
    game_2048.play()

