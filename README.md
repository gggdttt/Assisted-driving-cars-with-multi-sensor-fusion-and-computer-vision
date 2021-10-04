

# Assisted-Driving System with Multi-sensor Fusion and Computer Vision

## 1.Project Introduction

* Project Name: The Assisted-Driving System
* Project Aim: This system would help a running 'car' to detect the concrete type of an obstacle and then could help it to take different approaches according to the 'type'  detected by multi-sensor fusion.

### 1.1 Display of Hardware

<img src="https://raw.githubusercontent.com/gggdttt/ImageBeds/master/img/202110050009182.png" alt="Design" style="zoom:67%;" />

![image-20211005005709824](https://raw.githubusercontent.com/gggdttt/ImageBeds/master/img/202110050057194.png)

![image-20211005005813810](https://raw.githubusercontent.com/gggdttt/ImageBeds/master/img/202110050058105.png)

![image-20211005005830907](https://raw.githubusercontent.com/gggdttt/ImageBeds/master/img/202110050058137.png)

![image-20211005005843700](https://raw.githubusercontent.com/gggdttt/ImageBeds/master/img/202110050058991.png)

![image-20211005005901268](https://raw.githubusercontent.com/gggdttt/ImageBeds/master/img/202110050059601.png)



### 1.2 Software Display

**User Application Overview:**

![img](https://raw.githubusercontent.com/gggdttt/ImageBeds/master/img/202110050017866.gif)

**Detection Result:**

<img src="https://raw.githubusercontent.com/gggdttt/ImageBeds/master/img/202110050023287.png" alt="Detection result" style="zoom:80%;" />   



<img src="https://raw.githubusercontent.com/gggdttt/ImageBeds/master/img/202110050025016.gif" alt="img" style="zoom:150%;" /><img src="https://raw.githubusercontent.com/gggdttt/ImageBeds/master/img/202110050025705.gif" alt="img" style="zoom:150%;" />





## 2. Designing Outline(Hardware+Software)

* Hardware Designing
  * This system used `raspberry pi 4B+` ,`L298N driving module`,`CSI camera`,`Lazer rader`,`Infrared ranging module`. It is convenient for you to add additional approaches to detect the potential obstacles.

![image-20210923145852461](https://raw.githubusercontent.com/gggdttt/ImageBeds/master/img/202109231458577.png)

* Software Outline:

  The whole system could be divided into 3 parts of this system shown in the image following:

  ![image-20211004234348530](https://raw.githubusercontent.com/gggdttt/ImageBeds/master/img/202110042343675.png)

  > Reasons for designing the video recognition server:
  > (1) Insufficient hardware performance
  > (2) The distribution of the entire system is more flexible(Could set the detection server anywhere you want)

## 3.Hardware Realization

### 3.1 Hardware Connection Description



![image-20211004235511359](https://raw.githubusercontent.com/gggdttt/ImageBeds/master/img/202110042355455.png)

### 3.2 Wiring Diagram of Raspberry Pi and Motor Drive Module

![](https://raw.githubusercontent.com/gggdttt/ImageBeds/master/img/202110042358950.png)

### 3.3 Introduction to 2D Rader 

![image-20211005000005577](https://raw.githubusercontent.com/gggdttt/ImageBeds/master/img/202110050000666.png)

**Parameters of 2D Rader** 

| ByteRate             | 230400                                |
| -------------------- | ------------------------------------- |
| Operating mode       | 8-bit data, 1 stop bit, no parity bit |
| Output high level(V) | 2.9~3.5                               |
| Output low level(V)  | <0.4                                  |

**Detection Precision**

| Measurement item                                  | Precision | Range        | Unit   |
| ------------------------------------------------- | --------- | ------------ | ------ |
| Current angle (compared to initial point)         | 0.01      | 0~36000      | degree |
| Corresponding distance (compared to radar center) | 0.025     | 0~32,000,000 | mm     |

