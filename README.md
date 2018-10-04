![](https://github.com/topherCantrell/FarmerSays/blob/master/art/warp.jpg)

# A tale of two farms

Mr. Gary Dion had a vision, and now it has come true! He dreamed of two "Farmer Says" toys connected over the Internet through [adafruit.io](https://io.adafruit.com/) feeds.

He and I went different directions in our implementations. I used his design (and motor) to spin the pointer. Check out his awesome project:

https://github.com/garydion/FarmerSays

# The Farmer Says

This is what it looks like opened up. It is quite a mechanical marvel. The string pulls back a spring connected to a gear arm. When the string is released, the spring pulls the gear arm over a gear that spins the pointer.

When the string is pulled all the way out, the motion lifts the center wheel that pushes one of the 12 switches on the circuit board. Each switch is a different animal.

![](https://github.com/topherCantrell/FarmerSays/blob/master/art/FarmerSays.jpg)

# Accessing the switches

The rubber ring holds switches that press down onto finger pads on the circuit board. Each pad has an exposed
metal test point. I drilled a hole in the board and soldered wires to the test pads. The red wire is the
common connection to all the switches.

I used an exacto knife to cut all the traces from the switches to the original circuit:

![](https://github.com/topherCantrell/FarmerSays/blob/master/art/top.jpg)

I used superglue to hold the wires in place on the bottom of the board:

![](https://github.com/topherCantrell/FarmerSays/blob/master/art/bottom.jpg)

Then I replaced the rubber switch ring completing the board. 

![](https://github.com/topherCantrell/FarmerSays/blob/master/art/switches.jpg)

# Adding a motor

Gary gave me a small 5V friendly motor. Just like he did, I mounted the motor in the plastic case. I used a rubber band as a belt to turn the spinner with the motor.

I removed the gear arms and many of the screw towers. I moved the orange lever around closer to the string exit. This lever lifts the wheel to push the button on the circuit board. You can see the plastic nub that pushes the buttons when it lifts.

![](https://github.com/topherCantrell/FarmerSays/blob/master/art/motor.png)

I used a Raspberry Pi Zero as the brain in my implementation. I used the motor hat from Adafruit to drive the motor:

Motor Hat
https://www.adafruit.com/product/2348

Tutorial
https://learn.adafruit.com/adafruit-dc-and-stepper-motor-hat-for-raspberry-pi

# Audio

I dug the guts out of a mini speaker amplifier to use in my project. The speaker is powered by USB, and I took the built-in battery off the circuit board. I connected the amp to the 5V rails powering my project.

![](https://github.com/topherCantrell/FarmerSays/blob/master/art/audio.jpg)

The PiZero has no built-on audio support. I used a phat-dac to generate audio:

https://pinout.xyz/pinout/phat_dac

# Switches to the Pi

One side of every switch on the original circuit board connects to a common ground. I connected it to 3.3V on the Pi instead. Then I connected the other side of each switch to a GPIO pin on the Pi. I used the Pi's built-in pull-down resistors on each input.

![](https://github.com/topherCantrell/FarmerSays/blob/master/art/piswitches.jpg)

# Schematic

Here is the final circuit for my implementation.

![](https://github.com/topherCantrell/FarmerSays/blob/master/art/schematic.jpg)

# Final placement

The case is surprisingly spacious. There was plenty of room for all the boards.

The hole in the bottom of the case was for a failed external-motor to drive the spinner. Thanks to Gary for the idea and motor to mount inside the case.

![](https://github.com/topherCantrell/FarmerSays/blob/master/art/final.jpg)

# Software

The [hdw_farmer_says.py](src/hdw_farmer_says.py) file contains the code for the animal-switches and the motor driver.