

# Assisted-Driving System with Multi-sensor Fusion and Computer Vision

## 1.Project Introduction

* Project Name: The Assisted-Driving System
* Project Aim: This system would help a running 'car' to detect the concrete type of an obstacle and then could help it to take different approaches according to the 'type'  detected by multi-sensor fusion.

**Hardware Configuration**:

| Name                         | Edition               |
| ---------------------------- | --------------------- |
| CPU                          | i7-8565u              |
| GPU                          | GeForce MX150         |
| Operation System             | Windows 10 Home 64bit |
| CUDA                         | 10.2                  |
| CUDNN                        | 7.6.4                 |
| OpenCV                       | 3.2                   |
| Microsoft Visual studio 2019 | 16.4.1                |

### 1.1 Display of Hardware

<img src="https://raw.githubusercontent.com/gggdttt/ImageBeds/master/img/202110050009182.png" alt="Design" style="zoom:67%;" />

![image-20211005012237881](https://raw.githubusercontent.com/gggdttt/ImageBeds/master/img/202110050122179.png)

![image-20211005012401632](https://raw.githubusercontent.com/gggdttt/ImageBeds/master/img/202110050124977.png)

![image-20211005012518141](https://raw.githubusercontent.com/gggdttt/ImageBeds/master/img/202110050125424.png)

### 1.2 Software Display

**User Application Overview:**

![image-20211005012749968](https://raw.githubusercontent.com/gggdttt/ImageBeds/master/img/202110050127078.png)

**Detection Result:**

![image-20211005012925709](https://raw.githubusercontent.com/gggdttt/ImageBeds/master/img/202110050129962.png)

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

## 4 Software Realization

### 4.1 

