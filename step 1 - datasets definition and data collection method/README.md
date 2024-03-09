# Intro

Localization is not possible by just analyze CSI data alone As it is complex number and rotated by times.

Therefore we need to utilize machine learning for CSI localization

# ML model task given

We have to define the input and output for the machine learning model.

The input will be two sets of csi datas

* The set of 20 csi datas that represent X-axis

  * ```
    ex.
    [
    	[84 0 0 0 0 ...],
    	[84 0 0 0 0 ...],
    	...
    	...
    ]

    ```
* The set of 20 csi datas that represent Y-axis

  * ```
    ex.
    [
    	[84 0 0 0 0 ...],
    	[84 0 0 0 0 ...],
    	...
    	...
    ]

    ```

The output from model will be will be 16 members array with 0 and 1 value ex. `[1,0,0,0,1,0,0,1,0,0,0...]`

1= object in there

0= object not in there

# We must costomize data collection method

According to [StevenMHernandez/ESP32-CSI-Tool: Extract Channel State Information from WiFi-enabled ESP32 Microcontroller. Active and Passive modes available. (https://stevenmhernandez.github.io/ESP32-CSI-Tool/)](https://github.com/StevenMHernandez/ESP32-CSI-Tool)

You can use these command to collect CSI-Data

```
# macOS or Linux
idf.py monitor | grep "CSI_DATA" > my-experiment-file.csv

# Windows
idf.py monitor | findstr "CSI_DATA" > my-experiment-file.csv 

# Or this
idf.py monitor | python ../python_utils/serial_append_time.py > my-experiment-file.csv
```

However these will create a lot of problem if you happen to collect two axis of CSI_Data where it needed to matched up together.

And at the same time we should also check whether RX sending data to serial or not. The root cause of this problem might have something with TX or RX but those commands really block us from managing these problem effectively.

The method of collecting data to sd card sounds like a good idea. But your data will lack global UTC Time. aka. You will lack the information on how to pair csi data together.

# Datasets definition

For the speed of data processing we should collect CSI as .csv file obviously.

* 1st column will be global UTC Time string
* 2nd column will be "20 sets of csi_datas_x" and actually contains 20x128 array
* 3nd column will be "20 sets of csi_datas_x" and actually contains 20x128 array
* That is length of CSI_data is 128 and go along for 20 csi_data
* 4th column will contain 4x4 2d array named "map_data"
* 5th column might contain url of the image

# Data collection method

For data collector program that obtain CSI data by reading the serial. It might have to be written in C++.

But I'll make sure the code is easy to read and compile.
