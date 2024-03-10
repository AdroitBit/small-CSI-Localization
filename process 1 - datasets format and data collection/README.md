# Intro

Localization is not possible by just analyze CSI data alone As it is complex number and rotated by times.

Therefore we need to utilize machine learning for CSI localization

# ML model task given

We have to define the input and output for the machine learning model.

The input will be two sets of csi datas

* The array of 20 csi datas that represent X-axis

  * ```
    ex.
    [
    	[84,0,0,0,0 ...],
    	[84,0,0,0,0 ...],
    	...
    	...
    ]

    ```
* The array of 20 csi datas that represent Y-axis

  * ```
    ex.
    [
    	[84,0,0,0,1 ...],
    	[84,0,0,0,8 ...],
    	...
    	...
    ]

    ```

The output from model will be will be 16 members array with 0 and 1 value ex. `[1,0,0,0,1,0,0,1,0,0,0...]` and will be converted to 2d array of 4x4

```
[
    [1,0,0,0],
    [0,1,0,0],
    [0,0,0,0],
    [0,0,1,1]
]
```

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

For the simpleness of data collection.

We should collect CSI data and current map data with json file. And attached with the image file for verification

* proposed json file format

  * ```
    {
      "UTC_Time": "2021-01-01 00-00-00-000000",
      "CSI_Datas_X": [
        [84,0,0,0,0 ...],
        [84,0,0,0,0 ...],
        ...
        ...
      ],
      "CSI_Datas_Y": [
        [84,0,0,0,1 ...],
        [84,0,0,0,8 ...],
        ...
        ...
      ],
      "Map_Data": [
        [1,0,0,0],
        [0,1,0,0],
        [0,0,0,0],
        [0,0,1,1]
      ],
      "Image_URL": "2021-01-01 00-00-00-000000.jpg"
    }
    ```

  ```

  ```

# Data collection method design/rule/protocol

For Data collection method. We must obtain CSI data like the way we gonna obtain csi data for prediction process.

That is

* if data collection method written in Python. The program that used the model must be written in Python too.
* if data collection method written in C++. The program that used the model must be written in C++ too.
* If the program that used model obtain CSI data from serial port. The data collector must obtain CSI data from serial port too.
* If the program that used model reset serial every interval. The data collector must reset serial every interval too.
* same packet rate for step 1 and step 3 process
* same set's length of csi data used for step 1,2,3

## Automatic labelling method

For this method I design this way.

* The object is not moving in the area
* you run the program
* enter the input
* making sure RX and TX communicate and continuously through my serial monitor UI
  * It is normal to see some missing string in serial monitor because I flush it every loop (so the csi data is always the newest)

It would takes long to explain how the code works. So let's continue with how to use the program in `README2.md`
