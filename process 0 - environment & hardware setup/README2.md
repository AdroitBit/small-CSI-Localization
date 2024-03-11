# Laptop dependencies

run `pip install -r requirements.txt` to install required python dependencies.

## ESP32-CSI-Tool

It would be such a long documentation on how to setup ESP32.

So please follow the instruction of this repo and practice with it first until you get used to it. (play around one pair of ESP32 should be enough)

[StevenMHernandez/ESP32-CSI-Tool: Extract Channel State Information from WiFi-enabled ESP32 Microcontroller. Active and Passive modes available. (https://stevenmhernandez.github.io/ESP32-CSI-Tool/)](https://github.com/StevenMHernandez/ESP32-CSI-Tool)

After that, flash all 4 ESP32 with data on post-it accordingly like STA, AP and channel.

And also don't forget about Packet rate settings for STA (The value should be 100)

If you test ESP32 and there is the problem with consistency of CSI sending over serial. This is fine.

Because in the other process we can write the code to handle this problem easily.

## React & yarn

Later at the process 3. We will display our ML's prediction on frontend webpage.

So React (from Node.js) is needed.

And yarn is a library manager. So with it installed everything should be easier.

After all that. Now we're ready for process 1

# ESP32 setup

Assuming you have followed above instruction. The configuration should be correct by now.

Let's setup ESP32 TX first

* cd to the repo of ESP32-CSI-Tool
* cd to ./active_sta
* idf.py menuconfig
* config with the following
  * `ESP32 CSI Tool Config` > `WiFi Channel`
    * set to 4 for pair 2 (top-left)
    * set to 11 for pair 1 (top-right)
  * `ESP32 CSI Tool Config` > `Packet TX Rate`
    * set it to 100
* repeat the steps to flash both pair 1 and pair 2

Now let's setup ESP32 RX next

* cd to the repo of ESP32-CSI-Tool
* cd to ./active_ap
* idf.py menuconfig
* config with the following
  * `ESP32 CSI Tool Config` > `WiFi Channel`
    * set to 4 for pair 2 (bottom-right)
    * set to 11 for pair 1 (bottom-left)
* repeat the steps to flash both pair 1 and pair 2

# ESP32 Test

* Connect both TX (top) ESP32s to powerbank
* Connect both RX (bottom) ESP32s to Laptop


to see if ESP32 is working.

You can use simple application to Serial Monitor ESP32 RX like `CoolTerm.exe` (don't forget to set baudrate to 921600)

But I recommend using `idf.py -p {PORT}` as it is faster.

To see if whole system works. In serial monitor you must see the frames of CSI_Data getting sent continuously in high speed.

If it's not sending continuously that probably is ESP32-CSI-Tool's bug.

You can only temporary fix this by hitting reset button on RX or TX. It's quite annoying. Hopefully they fix this bug in the future.

Or We will fix it together with you guys one day. idk.
