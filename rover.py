from os import getloadavg
import rospy
from std_msgs.msg import String
import re
import time as time

def drive_data(drive):
    global drive_data
    drive_data = str(drive.data)
    

def arm_data(arm):
    global arm_data
    arm_data = str(arm.data)
    
# 4 karakter bir veri grubu olacak sekilde ayiracak bir fonksiyon tanimliyoruz.
def split_each(data,n):
    
    return [data[i:i+n] for i in range(0, len(data), n)]
# Enkoder verisi A ile baslayip B ile bitenler oldugundan dolayi yalnizca bu verileri secip ayiracak olan fonksiyona yollayacagiz.
def check_data(data,n):
    if data[0]=="A" and data[-1]=="B":
        return split_each((data[1:-1]),n)
    

def check_value(value_list):
    
    for i in range(len(value_list)):
         # Bu asamada mutlak degeri 255'ten buyuk olanlari degerlendirmeye aliyoruz.
       
        if int(value_list[i][1:4])>255:
            
            # 255 sinir degerine esitliyoruz.
            if int(value_list[i][0])==0:
                value_list[i]="0255"

            if int(value_list[i][0])==1:
                value_list[i]="1255"
                
    return value_list

# Uygun aralikta olanlar icin yalnizca isaret tahlili yapiyoruz.    
def str_data(liste):
    str_send = ""

    for i in range(len(liste)):

        if int(liste[i][0])==0:
            str_send=str_send+str(int(liste[i][1:4]))+" "

        else:
            str_send=str_send+"-"+str(int(liste[i][1:4]))+" "
            
    return str_send


if __name__== "__main__":

    rospy.init_node("drive_echo")
    rate = rospy.Rate(0.5)

    rospy.Subscriber("/serial/drive",String,callback=drive_data)
    rospy.Subscriber("/serial/robotic_arm",String,callback=arm_data)
    time.sleep(4)

    ack_pub_drive = rospy.Publisher("/position/drive", String,queue_size= 10)
    ack_pub_arm = rospy.Publisher("/position/arm", String, queue_size= 10)

    while not rospy.is_shutdown():
        
        
        try:
            a=check_data(drive_data,4)
            
            b=check_value(a)
            
            c= str_data(b)
            
            data_drive = String()
            data_drive.data = c
            ack_pub_drive.publish(data_drive)

            x=check_data(arm_data,4)
            
            y=check_value(x)
            
            z= str_data(y)
            
            data_arm = String()
            data_arm.data = z
            ack_pub_arm.publish(data_arm)

        except:
            pass   
        rate.sleep()    

   
