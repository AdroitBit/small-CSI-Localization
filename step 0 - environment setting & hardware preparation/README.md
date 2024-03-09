# Environment Design & setup

Prepare some solid board and tape the border of area in each position.

In this case

* I use Future board (That is what Thai people called it) which is the size of 61x65 cm
* Label the the corner of each area with simple post-it note and tape it down using scotch-tape
* Also gives some room for ESP32 placement, as you can see I don't use entire space.
* Lastly label the number on each area with marker pen

![alt text](image/empty_layout.jpg)

Attach 4 ESP32 to some foam like this.

For this project I use ESP32 WROVER B  and the foam is thickness is around 1.5cm

Be noted that ESP32 is just all the same anyway.

# How ESP32 placement can affect ESP32 communication (theorically)

Let's back down and think for a little bit. We don't really have clue how ESP32 emit the CSI data

But theorically ESP32 should emit the wave most intensely in front more than the side. And emit the signal very small in the back of ESP32. And please note that wifi emission is in spherical shape with cone-shape of intensity.

So we can roughly classify each area like this
