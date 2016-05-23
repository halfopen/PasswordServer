#!/usr/bin/env python
# coding=utf-8
from CMD import *
import serial
import time
import sys
import os
sys.path.append("..")
from sm.common import *
from sm.SM4 import *

# 指纹设备与树莓派通信文档
#

# 我的大拇指特征值，用于测试
my_finger_value = "0b258c65c12c9262213b9d212159250c6168a64dc17818ac6181a3682124155fa2652ace22668c09428d1ea9620000571a0000000000000000b6dd080223c0000065e02001000000000000000087f80803b53b08020000000000fefffe0000000000000000000000a00078000200320000000500000000000000010000000000000000000000000040000000000000b200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
time_out = 30


class FingerApi:
    ser = None          # 串口通信接口
    cmd = None          # 命令封装解包

    def __init__(self):
        self.ser= serial.Serial("/dev/ttyAMA0", 19200)
        self.cmd = CMD()
        print "build an FingerApi"

    def send(self, cmd):
        """
        发一个请求到指纹识别模块（基本操作）
        :param cmd: 命令字符串
        :return: 无返回
        """
        cmd_hex= cmd.decode("hex")
        self.ser.flushInput()
        i = self.ser.write(cmd_hex)
        time.sleep(0.5)

    def get(self):
        """
        获取返回信息(基本操作)
        :return:返回信息
        """
        result = ""
        j = self.ser.inWaiting()
        # print "get"+str(j)
        while j > 0:
            num = self.ser.read()
            # print "get:"+str(num.encode("hex"))
            result += str(num.encode("hex"))
            j = self.ser.inWaiting()
            # print "rest:"+str(j)
        return result

    def get_data(self):
        '''
        获取返回信息，给定超时时间
        :return:
        '''
        t = time_out*2
        while t > 0:
            if self.ser.inWaiting() > 0:        # 如果采集到返回
                return self.get()
            time.sleep(0.5)
            t -= 1
            print t
        self.stop_current_cmd()
        return ""

    def add_finger(self,userID):
        """
        发三次请求，添加一个指纹
        :param userID: 两位数字字符
        :return:
        """
        self.send(self.cmd.cmd("01","00",userID,"01"))
        if self.ser.inWaiting()>0:
            print self.get_data()
            self.send(self.cmd.cmd("02","00",userID,"01"))
            if self.ser.inWaiting()>0:
                print self.get_data()
                self.send(self.cmd.cmd("03","00",userID,"01"))
                print self.get_data()
                return True
        return False

    def get_finger_value(self):
        """
        采集手指特征值
        :return: 193个字节，也就是193*2位的字符串
        """
        self.send(self.cmd.cmd("23"))
        t = time_out*2
        while t > 0:
            time.sleep(0.5)
            if self.ser.inWaiting()>0:
                get_data = self.get()
                finger_value = get_data[24:24+193*2]
                return finger_value
            t -= 1
        self.stop_current_cmd()                         # 如果超时
        return ""

    def one_to_N(self):
        """
        1:N 指纹对比
        :return:
        """
        finger_value=self.get_finger_value()
        one2N_cmd = self.cmd.cmd("43","00","c4","00","000000"+finger_value)
        self.send(one2N_cmd)
        print self.get_data()

    def stop_current_cmd(self):
        '''
        发一条查询语句，用于停止上一条语句
        :return:
        '''
        self.send("f5090000000009f5")
        self.ser.flushInput()
        self.ser.flushOutput()

    def close(self):
        self.ser.close()

    def confirm_user(self):
        """
        确认用户
        :return: True:通过 False:未通过
        """
        command = self.cmd.cmd("0c")
        check_times = 3
        while check_times > 0:
            self.send(command)
            result = self.get_data()
            if len(result) > 0:
                if result[8:10] == "01":
                    return True
        return False


    def test_my_finger(self):
        """
        测试本地特征值对比
        :return: 结果 00 成功 01 错误 08 超时
        """
        """
        command = self.cmd.cmd("44","00","c4","00", "000000"+my_finger_value)
        print command
        self.send(command)
        result = self.get_data()
        print result
        if len(result) > 0:
            return result[8:10]
        else:
            return "08"
        """
        command = self.cmd.cmd("0c","00","03","01")
        self.send(command)
        result = self.get_data()
        print result
        if len(result) > 0:
            return result[8:10]
        else:
            return "08"

if __name__ == "__main__":
    print "test my finger"

    f = FingerApi()
    print f.test_my_finger()
