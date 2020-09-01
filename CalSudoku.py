# -*- coding: utf-8 -*-
"""
cal_sudoku.py
Created on Mon Mar 16 17:20:56 2020.

@author: Lance.Xu
"""
from time import perf_counter
from copy import deepcopy


class Sudoku:
    # @staticmethod
    def ini_candidate(self):
        """
        初始化候选数字典列表
        二维列表，每个元素是一个字典类型
        字典中的 key 是候选数，Value 无关
        初始时所有位置候选数都是 1 到 9
        :param: 无参
        :return: 初始化后的候选数列表
        """
        candi = []
        self.candidate = []
        tmp = {1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: "", 8: "", 9: ""}
        for i in range(9):
            candi.append(deepcopy(tmp))
        tmp = deepcopy(candi)
        for i in range(9):
            self.candidate.append(deepcopy(tmp))
        # return candidate

    def del_can(self, row, column, key):
        """
        根据在指定位置填入的数字，删除所在行、列、宫的其它位置的候选数
        如：在（1，2）位置写入 7，则第 1 行、第 2 列和该位置所在的宫格内所有的候选数7都删除
        :param row: 行
        :param column: 列
        :param key: 填入的数字
        """
        my_squ = 3 * (row // 3) + column // 3           # 根据行、列计算所在宫格
        for k in range(9):                              # 每行，每列，每宫格都是9个位置，放进同一个循环中处理
            self.candidate[row][k].pop(key, "")              # 同一行中如果存在候选数 key 则删除
            self.candidate[k][column].pop(key, "")           # 同一列中如果存在候选数 key 则删除
            my_row1 = 3 * (my_squ // 3) + k // 3        # 根据宫格和序列 k 计算所在行
            my_column1 = 3 * (my_squ % 3) + k % 3       # 根据宫格和序列 k 计算所在列
            self.candidate[my_row1][my_column1].pop(key, "")  # 同一宫中如果存在候选数 key 则删除
        # return candidate

    def candidate_gen(self):
        """
        根据数独生成候选数列表
        """
        for i in range(9):                      # 双重循环，遍历数独中每一个元素
            for j in range(9):
                if self.sudoku[i][j] != 0:           # 如果该位置不是0
                    self.candidate[i][j].clear()     # 则删除这个位置所有的候选数
                    self.del_can(i, j, self.sudoku[i][j])   # 调用 del_can 函数删除所在行、列、宫对应的候选数
        # return candidate

    # @staticmethod
    def check(self):
        """
        根据数独和候选数判断数独状态是成功、失败还是未完成
        :return:-1：失败，0:未完成，1：成功
        """
        count = 0       # 统计数独中空白位置数量
        # 生成一个 3x9 的字典列表 CheCan 辅助判断，3分别表示：行、列、宫，9表示每一个行（列、宫）中有9个位置
        tmp = {1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: "", 8: "", 9: ""}
        che_can = []
        for i in range(3):
            che_can.append([])
            for j in range(9):
                che_can[i].append(deepcopy(tmp))

        for i in range(9):                                  # 双重循环遍历数独中每一个位置
            for j in range(9):
                if self.sudoku[i][j] == 0:                   # 如果该位置为空
                    count = count + 1                       # 统计空白位置数量
                    if len(self.candidate[i][j]) == 0:           # 如果候选数数量为 0
                        return -1                           # 空格无候选数，返回失败
                else:                                   # 如果该位置有数字
                    if self.sudoku[i][j] in che_can[0][i]:       # 如果辅助列表CheCan行中存在
                        del che_can[0][i][self.sudoku[i][j]]     # 则从辅助列表CheCan行中删除他
                    else:                                   # 如果不存在（之前被删除过一次）
                        return -1                           # 行中重复返回失败
                    if self.sudoku[i][j] in che_can[1][j]:       # 如果辅助列表CheCan列中存在
                        del che_can[1][j][self.sudoku[i][j]]     # 则从辅助列表CheCan列中删除他
                    else:                                   # 如果不存在（之前被删除过一次）
                        return -1                           # 列中重复返回失败
                    my_squ = 3 * (i // 3) + j // 3          # 根据行、列计算所在宫格
                    if self.sudoku[i][j] in che_can[2][my_squ]:    # 如果辅助列表CheCan宫中存在
                        del che_can[2][my_squ][self.sudoku[i][j]]  # 则从辅助列表CheCan宫中删除他
                    else:                                   # 如果不存在（之前被删除过一次）
                        return -1                           # 宫格中重复返回失败
        if count == 0:  # 如果数字全满，并且上面没有返回
            return 1    # 则返回成功
        else:           # 如果未满，并且上面没有返回
            return 0    # 则返回未完成

    def sole(self):
        """
        行、列、宫候选数唯一法填放数字
        :return:candidate:最后生成的候选数列表，Sudoku:最后生成的数独状态
        """
        flag = 1                                                        # 标志位
        while flag == 1:                                                # 标志位为 1 继续循环
            flag = 0                                                    # 重置标志位
            for i in range(9):                                          # 双重循环遍历数独中每一个位置
                for j in range(9):
                    if self.sudoku[i][j] == 0:                               # 如果该位置为空
                        if len(self.candidate[i][j]) == 1:                   # 如果该位置只有一个候选数
                            self.sudoku[i][j] = list(self.candidate[i][j])[0]     # 写入这个唯一数
                            self.candidate[i][j].clear()                     # 清除该位置候选数
                            self.del_can(i, j, self.sudoku[i][j])    # 调用DelCan函数，删除所在行、列、宫其它位置候选数
                            continue                                    # 处理下一个位置
                        candi = deepcopy(self.candidate[i][j])
                        # 取出该位置候选数放入Candi中（如果不取出，后面修改Candidate[i][j]后会有报错）
                        for key in candi:                               # 依次取出候选数中的数字
                            r_num = 0                                   # 行统计
                            c_num = 0                                   # 列统计
                            b_num = 0                                   # 宫统计
                            for k in range(9):                          # 遍历所在行、列、宫
                                if key in self.candidate[i][k]:              # 如果行中存在 RNum + 1
                                    r_num += 1
                                if key in self.candidate[k][j]:              # 如果列中存在 CNum + 1
                                    c_num += 1
                                my_squ = 3 * (i // 3) + j // 3          # 根据行列计算宫
                                my_row = 3 * (my_squ // 3) + k // 3     # 根据宫，格计算行
                                my_column = 3 * (my_squ % 3) + k % 3    # 根据宫格计算列
                                if key in self.candidate[my_row][my_column]:   # 如果宫中存在 BNum + 1
                                    b_num += 1
                            if r_num == 1 or c_num == 1 or b_num == 1:  # 行、列、宫任一个唯一
                                self.sudoku[i][j] = key                      # 写入这个唯一数
                                self.candidate[i][j].clear()                 # 清除该位置候选数
                                self.del_can(i, j, key)    # 调用DelCan函数，删除所在行、列、宫其它位置候选数
                                # Flag = 1                              # 如果数据发生变化，给Flag赋值，再次循环
                                break                                   # 跳出本次循环，进入下一个单元格
        # return candidate, sudoku

    def trial(self, my_row, my_column):
        """
        核心递归函数，对不能用唯一法确定数字的位置，用候选数中的数字依次尝试，直到得出正确结果（很 * 很暴力）。
        :param my_row: 开始行
        :param my_column: 开始列
        :return: 无（并非真正的无返回值，因为 Python 中列表和字典类型的调用是通过地址引用的方式调用的，
                    所以修改后的数据调用后的位置可以直接使用。）
        """                                      # 用来存放计算结果的数组
        can_bak = deepcopy(self.candidate)                                   # 备份候选数列表
        sudo_bak = deepcopy(self.sudoku)                                     # 备份数独状态
        for key in can_bak[my_row][my_column]:                          # 利用备份的候选数列表遍历（因为候选数列表后面会发生变化，如果直接用的话会报错）
            self.sudoku[my_row][my_column] = key                             # 尝试写入候选数
            self.candidate[my_row][my_column].clear()                        # 删除当前位置候选数
            self.del_can(my_row, my_column, key)                             # 调用 del_can 函数删除所在行列宫候选数
            self.sole()                                                     # 调用 sole 函数，用唯一法尝试完成数独
            my_check = self.check()                         # 检查数独是完成，有三种情况：完成，未完成，失败
            if my_check == 1:                                           # 如果完成
                self.answerArr.append(deepcopy(self.sudoku))                      # 写入答案列表
                break                                                   # 跳出循环（结束本次调用，如果求解非唯一解数独需要去掉这一行）
            else:                                                       # 如果不等于1（合并失败和未完成状态，因为这两种状态都需要写回溯函数）
                if my_check == 0:                                       # 如果是未完成状态向下递归
                    for i in range(9 * my_row + my_column + 1, 80):     # 从下一个位置遍历数独
                        if self.sudoku[i // 9][i % 9] == 0:                  # 找到空白位置
                            self.trial(i // 9, i % 9)   # 递归调用本函数，尝试下一个空白位置试值
                            break                                       # 递归调用完成后不再去找下一个空白位置（因为候选数中上肯定有正确数字）
                if len(self.answerArr) >= 1:                                 # 如果有答案（非唯一解数独需要求几个解把 1 改成几）
                    break                               # 跳出循环（结束调用，如果非唯一解数独所有解，删除本函数中第一个 break 行，上面一行和本行）
            self.sudoku = deepcopy(sudo_bak)                                 # 失败回溯数独状态
            self.candidate = deepcopy(can_bak)                               # 失败回溯候选数列表
        # return

    # ?@staticmethod
    def __init__(self, text):
        """
        根据输入的数字转换成二维列表
        :param text:输入的一串81位的数字（如果输入超过81位，只取前81位）
        :return:返回生成的二维列表型数独
        """
        self.candidate = []
        self.sudoku = []                         # 定义一个列表
        tmp = []                            # 定义 tmp 变量
        for i in range(1, 82):              # 遍历 text 的前 81 位
            if i % 9 == 1:                  # 够一行初始化 tmp
                tmp = []                    # 过渡变量，够 9 个加入 sudoku 中
            if "0" <= text[0] <= "9":       # 判断是不是数字，如果是
                tmp.append(eval(text[0]))   # 加入到 tmp 后面
                text = text[1:]             # 删除 text 第一位字符
            else:                           # 如果输入的不是数字
                tmp.append(0)               # 按 0 处理，加入到 tmp 后面
                text = text[1:]             # 删除 text 第一位字符
            if i % 9 == 0:                  # 够 9 位 存入 sudoku 后面
                self.sudoku.append(deepcopy(tmp))
        # return sudoku                       # 返回生成的数独二维列表
        self.candidate = []
        self.answerArr = []
        self.cal_sudoku()

    def input_sudoku(self):
        """
        输入数独函数
        :param: 无参数
        :return: 返回生成的数独
        """
        text = input("请输入一个数独（连续81个数字；或者9行数字，每行9个）：")
        while 1:                                # 无限循环，直到输入的数字达到 81 个
            if len(text) < 81:
                text += input("请继续输入（还缺少{}位）:".format(81 - len(text)))      # 新输入的数字写到 text 后面
            else:
                break                           # 够 81 个数字退出
        return self.sudoku_gen(text)                 # 调用 sudoku_gen 函数，将生成的数独验证，转换为二维列表，并返回

    def cal_sudoku(self):
        """
        主函数，根据传入的数独求解并输出，如果没有参数传入，则使用 tmp3 做为要计算的数独
        :return: 无返回值
        """
        if self.sudoku is None:
            self.sudoku = self.tmp3
        self.ini_candidate()                             # 调用ini_Candidate函数，初始化候选数列表
        self.candidate_gen()    # 根据数独生成候选数列表
        self.sole()             # 调用 sole 函数，用唯一法先填一次
        my_check = self.check()                     # 调用　check 函数检查数独状态
        if my_check == 0:                                       # 如果未完成
            for i in range(81):                                 # 遍历数独
                if self.sudoku[i // 9][i % 9] == 0:                  # 查找空白位置
                    self.trial(i // 9, i % 9)     # 调用 trial 函数完成数独
                    break                                       # 主函数只调用一次
        elif my_check == 1:                                     # 如果一次完成
            self.answerArr.append(deepcopy(self.sudoku))                  # 把结果写入答案列表
        elif my_check < 0:                                      # 如果失败，数独无解
            raise ValueError("此数独无解")                                          # 返回 -1
        # return self.answerArr[0]

    @staticmethod
    def printAnswer(ansArr):
        print()
        for i in range(len(ansArr)):                     # 遍历答案列表，输出答案
            print(ansArr[i])
