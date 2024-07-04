
import __common
import time
import math

def main():
    jstep_pos = [1.57, 1.57, -1.57, 1.57, 1.57 + 5 / 180.0 * math.pi, 0]
    jstep_neg = [1.57, 1.57, -1.57, 1.57, 1.57 - 5 / 180.0 * math.pi, 0]
    rc = jkrc.RC("10.5.5.100")
    print(rc.login())
    print(rc.power_on())
    print(rc.enable_robot())
    

    while True:
        #print('joint_move {}'.format(rc.joint_move(jstep_pos, 0, True, 2 * math.pi)))
        #time.sleep(1)
        #print('joint_move {}'.format(rc.joint_move(jstep_neg, 0, True, 2 * math.pi)))
        print(rc.get_joint_position())
        time.sleep(1)

    rc.logout()

if __name__ == '__main__':
    __common.init_env()
    import jkrc

    print("jkrc import successful")

    main()