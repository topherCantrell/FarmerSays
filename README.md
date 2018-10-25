![](https://github.com/topherCantrell/FarmerSays/blob/master/art/warp.jpg)

As seen on show and tell:

https://youtu.be/2_tfuIpfjrw?t=206

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

## Switches and the motor

The [hdw_farmer_says.py](src/hdw_farmer_says.py) module contains the code for the animal-switches and the motor driver.

The module includes names for the individual GPIO pins. For instance, `S_12_00 = 4` means that the switch at the 12:00 position is connected to GPIO 4. And `S_4_00 = 22` means the switch at the 4:00 position is connected to GPIO 22.

The `init` function initializes all the pins and registers a callback on each rising edge. The physical buttons are fairly "bouncy", so the code uses a 1-second debounce time.

The `spin_motor` function simulates the spinning action of the pointer. The code controls the motor for several seconds to spin it up and back down like the original toy.

## Audio

The [farm_audio.py](src/farm_audio.py) module manages the audio prompts. There are two types of files: prompt files like "The cow says ...", and sound files like "Mooooo".

You can have as many audio files of each type as you like. The files are named with the animal name like:

  - cow_prompt_1.wav
  - cow_1.wav

The code loads and sorts the audo files from the "audio" directory.

The `get_animal_prompt(animal)` function returns the pygame sound object for the requested animal prompt. The code cycles through the files one by one with each call.

The `get_animal_sound(animal)` function returns the pygame animal sound. Again, the code cycles through all the files one by one.

The `prompt_and_play(animal)` function plays a prompt and a sound for the given animal. The function does not return until the sounds are played.
  
## Adafruit feeds

The [farm_adafruit_io.py](src/farm_adafruit_io.py) module reads and writes animal entries from an adafruit.io feed. The secret AIO key is kept in a separate file `credentials.py` that is not checked in to the repo.

The `get_last_animal(feed_url)` reads the very last entry in the given feed.

The `post_animal(feed_url,animal)` posts the given animal entry to the given feed.

The `wait_for_new_animal(feed_url)` waits for a new animal to appear in the given feed. This function does not return until a new value appears.

The module includes named values for two feeds: FARM_CHRIS and FARM_GARY.

## Main (Solo)

The [main_solo.py](src/main_solo.py) module is the application entry for the stand-alone toy. The user turns the pointer to an animal and pulls the string. The spinner spins and the sound plays.

The GPIO library calls `switch_changed()` when a button is pressed (when the string is pulled). This function starts two threads: one to spin the motor and one to play the sound.

## Main (Network)

The [main_solo.py](src/main_solo.py) module is the application entry for the network version of the toy. When the user pulls the string, the code posts the animal to my own adafruit.io feed for Gary's unit to see.

The code watches Gary's adafruit.io feed for new animals. When a new animal comes in, the spinner turns and the sound plays.


