# game_2048
自己用python写的2048小游戏

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

执行方式：
下载代码到本地，可以直接通过代码运行， 也可以通过也可以通过 pyinstaller -Fw game_2048.py 打包成exe格式运行。