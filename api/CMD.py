#!/usr/bin/env python
# coding=utf-8

import string


class CMD():
    """
    CMD类说明
    实现对模块的 命令/应答的 封装和拆分
     CMD： 命令/应答类型
    P1，P2，P3：命令参数
    Q1，Q2，Q3：应答参数，
    Q3 多用于返回操作的有效性信息，此时可有如下取值：
       define ACK_SUCCESS 0x00 //操作成功
       define ACK_FAIL 0x01 //操作失败
       define ACK_FULL 0x04 //指纹数据库已满
       define ACK_NOUSER 0x05 //无此用户
       define ACK_FIN_OPD 0x07 //指纹已存在
       define ACK_TIMEOUT 0x08 //采集超时
     CHK： 校验和，为第2 字节到第6 字节的异或值
     cmd, arg都是字符串
     详细格式定义见: http://www.waveshare.net/w/upload/6/65/UART-Fingerprint-Reader-UserManual.pdf
    """
    # 返回数据定义
    data_len = 0    # 数据长度
    q3 = "00"       # 返回状态
    Data = ""       # 返回数据

    def cmd(self, cmd_str, arg1="00", arg2="00", arg3="00", data_str=None):
        """ 封装8个字节命令
        @:param cmd 命令号
        @:param arg1 命令参数1
        @:param arg2 命令参数1
        @:param arg3 命令参数1
        @:return 命令字符串 8个字节，也就是16个字符 """
        c = string.atoi(cmd_str,16)
        a1 = string.atoi(arg1,16)
        a2 = string.atoi(arg2,16)
        a3 = string.atoi(arg3,16)

        chk = c^a1^a2^a3 # 计算校验合
        chk = "%02X" % chk # 返回16进制

        if data_str is not None:                        # 如果是大于8位的命令
            # print len(data_str)
            chk2 = string.atoi(data_str[0:2],16)        # 取第一个
            for i in range(2,len(data_str),2):          # 每两位进行计算
                temp = data_str[i:i+2]
                chk2 = chk2^string.atoi(temp,16)

            chk2 = "%02X" % chk2                          # 数据段的校验位
            return "f5"+cmd_str+arg1+arg2+arg3+"00"+chk+"f5f5"+data_str+chk2+"f5"

        else:
            return "f5"+cmd_str+arg1+arg2+arg3+"00"+chk+"f5"

    def de_cmd(self, data_str):
        """
        解析返回的数据包
        数据由两部分组成：数据头+数据包
        数据头第3-4个字节代表数据包的长度
        数据包:2-len+1个字节
        :param data: 返回数据 数据头+数据包
        """
        data_str_len = len(data_str)
        if data_str_len==16:
            pass
        self.data_len = data_str[3:6]
        self.Data = data_str[18:self.data_len+18]



if __name__ == "__main__":
    cmd = CMD()
    print cmd.cmd("02","00","01","00")
    print cmd.cmd("02","00","01","00","1001")


