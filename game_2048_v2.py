import random
import time

import numpy as np
from colorama import init as color_init


board: np.array = []
row, col = 5, 5
random_range = [1, 2]
random_numbers = [2, 4]
cell_width = 9


show_template = f"""
{'*' * (col * 6)}
%(board)s\033[0m
{'*' * (col * 6)}
"""

color_map = {
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


class Direction:
    up = 'W'
    down = 'S'
    left = 'A'
    right = 'D'


def init():
    color_init()

    global board
    board = np.zeros([row, col], dtype=np.uint8)
    fill()
    show()


def _merge_move(board_row, pos_or_neg):
    """
    合并相同数字
    :param board_row: 行
    :param pos_or_neg: 正向(向右滑动)或负向(向左滑动)
    :return:
    """
    length = len(board_row)
    i, step, move_at = (0, 1, 0) if pos_or_neg else (length - 1, -1, -1)

    while i < length if pos_or_neg else i >= 0:
        if board_row[i] == 0:
            i += step
            continue
        meet, meet_idx, match = False, i, False
        for j in (range(i+1, length) if pos_or_neg else range(i-1, -1, -1)):
            meet_idx = j
            if board_row[j] == 0:
                continue
            meet = True
            if board_row[j] == board_row[i]:
                match = True
            break
        cur_idx = i
        if meet and match:
            board_row[i] *= 2
            board_row[meet_idx] = 0
            i = meet_idx + step
        elif meet and not match:
            i = meet_idx
        else:
            i += step

        if board_row[move_at] != board_row[cur_idx]:
            board_row[move_at] = board_row[cur_idx]
            board_row[cur_idx] = 0
        move_at += step


def merge_move(direction: Direction):
    global board
    pos_or_neg = False
    trans = False
    if direction in (Direction.down, Direction.up):
        board = board.T
        trans = True
    if direction in (Direction.left, Direction.up):
        pos_or_neg = True

    for item in board:
        _merge_move(item, pos_or_neg)

    if trans:
        board = board.T


def fill():
    empty_pos = []
    for i, item in enumerate(board):
        for j in range(col):
            if board[i, j] == 0:
                empty_pos.append((i, j))
    if not empty_pos:
        return
    random_amount = random.randint(*random_range)
    fill_pos = random.sample(empty_pos, min(len(empty_pos), random_amount))
    for pos in fill_pos:
        random_num = random.sample(random_numbers, 1)[0]
        board[pos] = random_num


def show():
    global board

    rows = []
    for item in board:
        rows.append(''.join([(color_map[i] + str(i)).ljust(cell_width, ' ') for i in item]))
    rows = [' ' * 5 + r for r in rows]
    show_board = '\n'.join(rows)
    print(show_template % {'board': show_board})


def play():
    while True:
        direction = input('W(上)S(下)A(左)D(右)>')
        direction = direction.strip().upper()
        if direction == 'Q':
            break
        if direction not in [v for k, v in Direction.__dict__.items() if not k.startswith('_')]:
            print(f"方向[{direction}]错误")
            continue

        merge_move(direction)
        fill()
        show()


def play_ai():
    for i in range(1, 5001):
        print(f"running at :{i}")
        direction = random.choice(['w', 's', 'd', 'a']).upper()
        merge_move(direction)
        fill()
        show()
        time.sleep(0.5)


def main():
    init()
    # play()
    play_ai()


if __name__ == '__main__':
    main()
