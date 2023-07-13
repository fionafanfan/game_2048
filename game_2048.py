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
from pprint import pprint
import tkinter as tk
import numpy as np
import threading


class TkGUI2048(object):
    """
    top: D9D1E0
    back_page: B49FAC
    0: CDC1B4
    2: EEE4DA
    4: E5E0EA
    8: FBB4BA
    16: FF9B8B
    32: FF7261
    64: F3D8A9
    128: F7C679
    256:FF9B44
    512: FF7019
    1024:FF4001
    2048: ff0040
    4096: 640034

    重置： 9D99A8，
    字体 ； D3D5FE
    """

    def __init__(self, top=None, seats=None, max_num=0, cur_num=0, move_num=0, play_keyboard=None, play_up=None,
                 play_down=None, play_left=None, play_right=None, play_ai=None, quit=None, reset=None):
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
        self.play_keyboard = play_keyboard
        self.play_up = play_up
        self.play_down = play_down
        self.play_left = play_left
        self.play_right = play_right
        self.play_ai = play_ai

        self.quit = quit
        self.reset = reset

        self.Frame_game_root = None
        self.Label_num = None

        self.Label_max = None
        self.Label_cur = None
        self.Label_move = None

        self.Button_up = None
        self.Button_down = None
        self.Button_left = None
        self.Button_right = None
        self.Button_ai_play = None

        self.Button_exit = None
        self.Button_reset = None
        self.Label_keyboard_event = None

        self.draw_game_root_page()
        self.draw_game_num_page()
        self.draw_command_button()
        self.draw_keyboard_label()
        self.draw_records()

    # 打包进线程（耗时的操作）
    @staticmethod
    def thread_it(func, *args):
        t = threading.Thread(target=func, args=args)
        t.setDaemon(True)  # 守护
        t.start()  # 启动
        # t.join()          # 阻塞--会卡死界面！

    def draw_game_root_page(self):
        self.top.geometry("650x450+539+43")
        self.top.minsize(120, 1)
        self.top.maxsize(3004, 1901)
        self.top.resizable(0, 0)
        self.top.title("2048")
        # self.top.iconbitmap('2048.ico')  # 更改窗口图标, 需要一个ico类型位图参数作为窗口图标，.png.jpg等其他类型不能显示
        self.top.tk.call('wm', 'iconphoto', self.top._w, tk.PhotoImage(file='2048.png'))  # 图片为.png格式
        self.top.configure(background="#FAF8EF")

    def draw_game_num_page(self, seats=None):
        if seats:
            self.seats = seats

        self.Frame_game_root = tk.Frame(self.top)
        self.Frame_game_root.place(x=10, y=10, height=410, width=410)
        self.Frame_game_root.configure(relief='groove', borderwidth="0", background="#BBADA0")

        label_num_size = 90
        label_num_x_size = 10  # 横轴间隔10
        label_num_y_siee = 10   # 纵轴间隔10
        label_num_x_size_map = [label_num_x_size, label_num_x_size+1*label_num_size, label_num_x_size+2*label_num_size, label_num_x_size+3*label_num_size]
        label_num_y_size_map = [label_num_y_siee, label_num_y_siee+1*label_num_size, label_num_y_siee+2*label_num_size, label_num_y_siee+3*label_num_size]
        num_color_map = {
            0: "#CDC1B4",
            2: "#EEE4DA", 4: "#E5E0EA", 8: "#FBB4BA", 16: "#FF9B8B",
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
                                     border=1, disabledforeground="#a3a3a3",
                                     font="-family {High Tower Text} -size 36 -weight bold",
                                     foreground="#000000",
                                     relief="solid",
                                     text=text)

    def draw_command_button(self):
        self.Button_ai_play = tk.Button(self.top)
        self.Button_ai_play.place(x=580, y=370, height=28, width=49)
        self.Button_ai_play.configure(activebackground="#793e3e", activeforeground="#793e3e",
                                      background="#b16363", compound='left', disabledforeground="#a3a3a3",
                                      foreground="#000000",
                                      highlightbackground="#d9d9d9",
                                      highlightcolor="black",
                                      pady="0",
                                      text='''AI Play''',
                                      command=lambda: self.thread_it(self.play_ai))

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
                                 command=lambda: self.thread_it(self.play_up)
                                 )

        self.Button_down = tk.Button(self.top)
        self.Button_down.place(x=470, y=250, height=28, width=49)
        self.Button_down.configure(activebackground="beige", activeforeground="black",
                                   background="#b16363", compound='left', cursor="fleur",
                                   foreground="#000000", highlightbackground="#d9d9d9",
                                   highlightcolor="black", pady="0", text='''下''',
                                   command=lambda: self.thread_it(self.play_down))

        self.Button_left = tk.Button(self.top)
        self.Button_left.place(x=430, y=200, height=28, width=49)
        self.Button_left.configure(activebackground="beige", activeforeground="black",
                                   background="#b16363", compound='left', cursor="fleur",
                                   foreground="#000000", highlightbackground="#d9d9d9",
                                   highlightcolor="black", pady="0", text='''左''',
                                   command=lambda: self.thread_it(self.play_left)
                                   )

        self.Button_right = tk.Button(self.top)
        self.Button_right.place(x=520, y=200, height=28, width=49)
        self.Button_right.configure(activebackground="beige", activeforeground="black",
                                    background="#b16363", compound='left', cursor="fleur",
                                    foreground="#000000", highlightbackground="#d9d9d9",
                                    highlightcolor="black", pady="0", text='''右''',
                                    command=lambda: self.thread_it(self.play_right)
                                    )

    def draw_keyboard_label(self):
        """
        label邦健键盘事件，来控制移动方向
        """
        self.Label_keyboard_event = tk.Label(self.top)
        self.Label_keyboard_event.focus_set()
        self.Label_keyboard_event.pack()
        self.Label_keyboard_event.bind('<Key>', self.play_keyboard)

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

    游戏终止条件判断：
    [2, 8, 2, 8, 4, 16, 8, 2, 8, 64, 32, 8, 2, 4, 16, 4]
    1、列表中的值全大于0
    2、每每相邻的值不相等
    3、同行或同列相邻值不等
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
        self.play_ai_running = True  # 2048 AI状态
        self.last_direction = 's'  # 默认是向下， 最近的一次移动方向

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

    def check_finish(self, seats):
        is_finished = True
        if not all(seats):
            return False

        set_seats = set(seats)
        nums = np.reshape(np.array(seats), (4, 4))
        for seat in set_seats:
            indexs_tuple = np.where(nums == seat)
            indexs = [(row, col) for row, col in zip(indexs_tuple[0].tolist(), indexs_tuple[1].tolist())]
            # print(seat, indexs)

            for item in indexs:
                if (item[0], item[1] + 1) in indexs:
                    return False
                elif (item[0] + 1, item[1]) in indexs:
                    return False
        return is_finished

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

    @staticmethod
    def check_play_caculate(all_seats, direction, direction_indexs):
        new_lines_val_list = []
        zero_index_list = []
        temp_seats = copy.deepcopy(all_seats)
        for n, line in enumerate(direction_indexs):
            line_val_list = [all_seats[line[i]] for i in range(4) if all_seats[line[i]]]  # 当前局面的当前行或列所有值
            new_line_val_list = []  # 每一行或每一列通过位移或计算后的值
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
                all_seats[line[i]] = new_line_val

        # 变换前后局面上的值有变化，才能随机在剩余的空间中生成新的数值
        if not all_seats == temp_seats:
            return {"zero_index_num": len(zero_index_list), "all_seats": all_seats, "max_num": max(all_seats), "direction": direction}
        else:
            return {"zero_index_num": 0, "all_seats": all_seats,  "max_num": 0, "direction": direction}

    def check_directions(self, seats):
        direction_indexs = {'w': self.up, 's': self.down, 'a': self.left, 'd': self.right}

        temp_directions = sorted(
            [self.check_play_caculate(copy.deepcopy(seats), direction, indexs) for direction, indexs in
             direction_indexs.items()],
            key=lambda x: x['zero_index_num'], reverse=True)

        max_direction_zero_num = max([d['zero_index_num'] for d in temp_directions])
        max_direction_num = max([d['max_num'] for d in temp_directions])
        directions = [data for data in temp_directions if
                      data['zero_index_num'] == max_direction_zero_num and data['max_num'] == max_direction_num]

        return directions

    def check_direction(self, seats):
        """
        w, a, s, d
        """
        # 第一级别
        one_direction_datas = self.check_directions(seats)
        one_directions = [data['direction'] for data in one_direction_datas]
        temp_two_direction_datas = []

        for direction, data in zip(one_directions, one_direction_datas):
            two_temp_directions = self.check_directions(copy.deepcopy(data['all_seats']))
            two_max_zero_index_num = max([data['zero_index_num'] for data in two_temp_directions] + [0])
            two_max_num = max([data['max_num'] for data in two_temp_directions] + [0])
            temp_two_direction_datas.append({'direction': direction,
                                             'zero_index_num': two_max_zero_index_num,
                                             'max_num': two_max_num})

        max_direction_zero_num = max([data['zero_index_num'] for data in temp_two_direction_datas] + [0])
        max_direction_num = max([data['max_num'] for data in temp_two_direction_datas] + [0])
        two_directions = [data['direction'] for data in temp_two_direction_datas if
                      data['zero_index_num'] == max_direction_zero_num and data['max_num'] == max_direction_num]

        if 's' in two_directions:
            two_direction = 's'
        elif 'a' in two_directions:
            two_direction = 'a'
        elif 'd' in two_directions:
            two_direction = 'd'
        elif 'w' in two_directions:
            two_direction = 'w'
        else:
            two_direction = 's'

        if two_direction in one_directions:
            direction = two_direction
        else:
            direction = 's'

        print(f"one_directions:{one_directions}  one_direction_datas: {one_direction_datas} two_direction_datas:{temp_two_direction_datas}, two_direction:{two_direction}  direction:{direction}")
        self.last_direction = direction
        return direction

    def play_up(self):
        self.play_caculate(self.up)

    def play_down(self):
        self.play_caculate(self.down)

    def play_left(self):
        self.play_caculate(self.left)

    def play_right(self):
        self.play_caculate(self.right)

    def play_ai(self):
        """
        ai自动玩2048
        :return:
        """
        pass

    def draw_2048(self):
        """
        绘制面板
        :return:
        """
        pass

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
        self.col = 4
        self.show_template = f"""begin{'*' * (self.col * 6)}
%(board)s\033[0m
{'*' * (self.col* 6)}end"""

    @property
    def color_map(self):
        return {
            0: '\033[37m',  # 白色
            2: '\033[34m',  # 蓝色
            4: '\033[32m',  # 绿色
            8: '\033[36m',  # 青色
            16: '\033[31m',  # 红色
            32: '\033[35m',  # 紫色
            64: '\033[33m',  # 黄色
            128: '\033[90m',  # 灰色
            256: '\033[94m',  # 亮蓝色
            512: '\033[92m',  # 亮绿色
            1024: '\033[96m',  # 亮青色
            2048: '\033[91m',  # 亮红色
            4096: '\033[95m',  # 亮紫色
            8192: '\033[93m',  # 亮黄色
        }

    def draw_2048(self):
        cell_width = 9
        os.system('cls')
        r = 1
        rows = []
        for i in range(1, 17):
            if i % 4 == 0:
                # print(f"{str(r)}行:{self.all_seats[i-4:i]}")
                rows.append(''.join([(self.color_map[i] + str(i)).ljust(cell_width, ' ') for i in self.all_seats[i-4:i]]))
                r += 1
        rows = ['' * 5 + r for r in rows]
        show_board = '\n'.join(rows)
        print(self.show_template % {'board': show_board})

    def play_caculate(self, direction_indexs):
        super(CmdGame2048, self).play_caculate(direction_indexs)
        self.draw_2048()

    def reset(self):
        self.play_ai_running = False
        self._init_game_2048()
        self.cur_num = max(self.all_seats)  # 当前最大值
        self.move_num = 0

    def ai_one(self):
        """
        策略： 随机上下左右
        :return:
        """
        count = 1
        while True:
            if not self.play_ai_running or count > 5001:
                break
            direction = random.choice(['w', 's', 'd', 'a'])
            if direction == 'w':
                self.play_up()
            elif direction == 's':
                self.play_down()
            elif direction == 'a':
                self.play_left()
            elif direction == 'd':
                self.play_right()
            self.draw_2048()
            if self.check_finish(self.all_seats):
                print("-*- 游戏结束- * -")
                break
            count += 1
            time.sleep(1)

    def ai_two(self):
        """
        策略：
          1、开局优先向下
          2、 只要最下方还有空位，则优先向下
          3、 如果能够合并， 则向左向右合并
          4、 如果向下不能改变局面， 只能向上移动， 再向下移回来
          5、重复上上面的操作
        :return:
        """
        self.play_down()
        self.draw_2048()

        count = 1
        while True:
            if not self.play_ai_running or count > 5001:
                break
            direction = self.check_direction(self.all_seats)
            if direction == 'w':
                self.play_up()
            elif direction == 's':
                self.play_down()
            elif direction == 'a':
                self.play_left()
            elif direction == 'd':
                self.play_right()

            # self.draw_2048()
            if self.check_finish(self.all_seats):
                print("-*- 游戏结束- * -")
                break
            count += 1
            time.sleep(1)

    def play_ai(self):
        self._init_game_2048()
        self.draw_2048()
        # self.ai_one()
        self.ai_two()

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
            if self.check_finish(self.all_seats):
                print("-*- 游戏结束- * -")
                break
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

    def play_keyboard(self, evt):
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
        self.play_ai_running = False
        if self.game_2048_play:
            self._init_game_2048()
            self.cur_num = max(self.all_seats)  # 当前最大值
            self.move_num = 0
            self.game_2048_play.draw_records(cur_num=self.cur_num, move_num=self.move_num)
            self.game_2048_play.draw_game_num_page(seats=self.all_seats)

    def ai_one(self):
        """
        策略： 随机上下左右
        :return:
        """
        count = 1
        while True:
            if not self.play_ai_running or count > 5001:
                break
            direction = random.choice(['w', 's', 'd', 'a'])
            if direction == 'w':
                self.play_up()
            elif direction == 's':
                self.play_down()
            elif direction == 'a':
                self.play_left()
            elif direction == 'd':
                self.play_right()
            # self.draw_2048()
            if self.check_finish(self.all_seats):
                print("-*- 游戏结束- * -")
                break
            count += 1
            time.sleep(1)

    def ai_two(self):
        """
        策略：
          1、开局优先向下
          2、 只要最下方还有空位，则优先向下
          3、 如果能够合并， 则向左向右合并
          4、 如果向下不能改变局面， 只能向上移动， 再向下移回来
          5、重复上上面的操作
        :return:
        """
        self.play_down()
        # self.draw_2048()

        count = 1
        while True:
            if not self.play_ai_running or count > 5001:
                break
            direction = self.check_direction(self.all_seats)
            if direction == 'w':
                self.play_up()
            elif direction == 's':
                self.play_down()
            elif direction == 'a':
                self.play_left()
            elif direction == 'd':
                self.play_right()

            # self.draw_2048()
            if self.check_finish(self.all_seats):
                print("-*- 游戏结束- * -")
                break
            count += 1
            time.sleep(1)

    def play_ai(self):
        print("play ai")
        # self._init_game_2048()
        # self.draw_2048()
        self.ai_two()

    def play(self):
        init_top = tk.Tk()
        self._init_game_2048()
        # init_seats = [0, 0, 0, 0, 0, 0, 0, 16, 0, 0, 0, 4, 32, 64, 64, 0]  # 临时修改初始值
        # self.all_seats = init_seats
        self.cur_num = max(self.all_seats)  # 当前最大值
        self.game_2048_play = TkGUI2048(top=init_top, seats=self.all_seats,
                                        max_num=2048, cur_num=self.cur_num, move_num=self.move_num,
                                        play_keyboard=self.play_keyboard,
                                        play_up=self.play_up, play_down=self.play_down,
                                        play_left=self.play_left, play_right=self.play_right, play_ai=self.play_ai,
                                        quit=self.quit, reset=self.reset)

        self.game_2048_play.run()


if __name__ == "__main__":
    # game_2048 = CmdGame2048()  # 命令行模式
    game_2048 = GuiTkGame2048()  # tkinter实现的图形界面模式
    # ret = []
    # for i in range(1, 3):
    #     game_2048.play_ai()
    #     ret.append(game_2048.all_seats)
    #     print(f"--第{i}局结束--")
    # print("结果:")
    # pprint(ret)
    game_2048.play()

