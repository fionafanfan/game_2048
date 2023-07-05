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

界面展现方式：
* cmd
* tkinter(优点：python标准库，无需额外安装， 可以借助界面工具生成代码，再进行代码优化  缺点：界面写不漂亮，比较生硬)
* wxpython （第三方库，需安装）


执行方式：
下载代码到本地，可以直接通过代码运行， 也可以通过也可以通过 pyinstaller -Fw game_2048.py 打包成exe格式运行。

过程中遇到的问题点及解决参考思路：
* cmd中根据不同的数字显示不同的颜色
* 在使用tkinter编写界面的时候，经常会出现界面无响应，卡死等现象：
```
原因：
  * 无限循环
  * 阻塞函数
  * 过重的计算
  * 死锁
  * 资源耗尽 
解决方案：尽量使用线程去执行你的操作，这样可以避免阻塞你的界面刷新，造成无响应
    * 避免在主事件循环中使用无限循环、阻塞函数或过重计算
    * 使用线程或子进程来执行阻塞操作和计算
    * 小心处理线程同步,避免死锁
    * 及时释放资源,避免资源耗尽
    * 将复杂的操作切分为多个步骤,在每一步都刷新界面,给用户响应的机会
   ```

AI合并方案列举：
* 上下左右顺序生成方向
* 上下左右随机生成方向
* 基于人工总结出来的规则，动态生成方向，
  * 当前局面四个方向分别运行，哪个方向空出来的空格最多，则选择哪个方向
  * 当前局面往哪个方向运行， 最大值能靠边靠角
  * 当前局面往哪个方向运行， 合并值最多最大
```
四个方向中， 有3个方向不能移动，只能往一个方向移动， 这种情况会比较危险，
会打乱原有的节奏，应该避免这种情况产生)
[0, 0, 0, 0,
0, 0, 0, 0,
0, 0, 0, 0,
2, 4, 8, 16]

[2, 0, 0, 0,
4, 0, 0, 0,
8, 0, 0, 0,
16, 0, 0, 0] 

[2, 4, 8, 16,
0, 0, 0, 0,
0, 0, 0, 0,
0, 0, 0, 0] 

[0, 0, 0, 16,
0, 0, 0, 8,
0, 0, 0, 4,
0, 0, 0, 2]

情况：向下移动
[0, 0, 0, 0,
0, 0, 0, 0,
0, 0, 0, 16,
2, 4, 8, 16]

情况：向右移动 
[0, 0, 0, 0,
0, 0, 0, 0,
8, 4, 2, 0,
16, 8, 4, 2]
```