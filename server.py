# Created by Youssef Elashry to allow two-way communication between Python3 and Unity to send and receive strings

# Feel free to use this in your individual or commercial projects BUT make sure to reference me as: Two-way communication between Python 3 and Unity (C#) - Y. T. Elashry
# It would be appreciated if you send me how you have used this in your projects (e.g. Machine Learning) at youssef.elashry@gmail.com

# Use at your own risk
# Use under the Apache License 2.0

# Example of a Python UDP server

import UdpComms as U
import time
import __common
import math

def ObjectMsg(cat,px,py,pz,rx,ry,rz,sx,sy,sz):
    res = "{Object Detection}\n"
    res += cat + "\n"
    res += str(px) + "\n"
    res += str(py) + "\n"
    res += str(pz) + "\n"
    res += str(rx) + "\n"
    res += str(ry) + "\n"
    res += str(rz) + "\n"
    res += str(sx) + "\n"
    res += str(sy) + "\n"
    res += str(sz)
    return res

def RealJointAnglesMsg(data_tuple):
    # 提取元组中的第二个元素
    joint_angles = data_tuple[1]
    
    # 检查数组的长度是否为6
    if len(joint_angles) != 6:
        raise ValueError("数组长度不等于6")
    
    # 创建字符串格式
    formatted_string = "{Current Joint}\n"
    for angle in joint_angles:
        # 将弧度转化为角度并保留两位小数
        angle_in_degrees = round(math.degrees(angle), 1)
        formatted_string += f"{angle_in_degrees}\n"
    
    #print(formatted_string)
    return formatted_string

def is_joint_angle(data_str):
    lines = data_str.strip().split('\n')
    
    # 检查是否有7行内容（包括标题）
    if lines[0] != 7:
        return True
    else:
        return False

def parse_joint_angles(data_str):
    # 分割字符串并去掉空行
    lines = data_str.strip().split('\n')
    
    # 检查是否有7行内容（包括标题）
    if len(lines) != 7:
        raise ValueError("字符串格式不正确或行数不正确")
    
    # 提取并转换角度值
    angles_radius = []
    angles = []
    for line in lines[1:]:
        angles_radius.append(math.radians(float(line)))
        angles.append(float(line))

    print(angles)
    
    # 检查数组长度是否为6
    if len(angles_radius) != 6:
        raise ValueError("提取的角度数量不等于6")
    
    return angles_radius

def main():
    # Create UDP socket to use for sending (and receiving)
    sock = U.UdpComms(udpIP="127.0.0.1", portTX=8000, portRX=8001, enableRX=True, suppressWarnings=True)

    cat = "cat MIAO~"
    pos = [-0.2,1.7,0.2]
    rot = [0,0,0]
    size = [0.1,0.1,0.1]
    direction = -1

    rc = jkrc.RC("192.168.2.7")
    print(rc.login())
    print(rc.power_on())
    print(rc.enable_robot())
        

    
    while True:

        # object detection -> Unity
        sock.SendData(ObjectMsg(cat, pos[0], pos[1], pos[2], rot[0], rot[1], rot[2], size[0], size[1], size[2])) # Send this string to other application
        rot[1] += 1
        #pos[0] += 0.002*direction

        if pos[0] > 1:
            direction = -1
        elif pos[0] < -1:
            direction = 1

        # robot arm DT info -> Unity
        dt_info = rc.get_joint_position()
        sock.SendData(RealJointAnglesMsg(dt_info))
        angles = [1.2, 1.8, -1.8, 1.57, 1.57, 1.57]
        #rc.joint_move(angles, 0, True, 0.1)
        # receive
        
        data = sock.ReadReceivedData() # read data
        if data != None: # if NEW data has been received since last ReadReceivedData function call
            #print(data) # print new received data
            if is_joint_angle(data):
                angles = parse_joint_angles(data)
                print(angles)
                rc.joint_move(angles, 0, False, 0.2)
        

        time.sleep(0.05)

        


if __name__ == '__main__':
    __common.init_env()
    import jkrc

    print("jkrc import successful")

    main()