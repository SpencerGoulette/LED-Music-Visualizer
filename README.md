# LED-Music-Visualizer
LED Music Visualizer Project created over the Winter Break of 2018-2019. The idea for the project was obtained from Devon Crawford. His project can be seen here:
https://www.youtube.com/watch?v=lU1GVVU9gLU

# Equipment
- WS2812B LEDS
https://www.amazon.com/dp/B01CDTEG1O/ref=pd_luc_rh_sspa_dk_huc_pt_expsub_0?psc=1

- Raspberry Pi 3 Model B+
https://www.amazon.com/Raspberry-Pi-RASPBERRYPI3-MODB-1GB-Model-Motherboard/dp/B01CD5VC92/ref=sr_1_12?s=electronics&ie=UTF8&qid=1546032686&sr=1-12&keywords=raspberry+pi+3+b%2B

- Frequency to Voltage Circuit (multiple components needed)

# Frequency to Voltage Circuit
Below is the circuit used to convert the frequency of the audio to voltage.
![alt text](https://github.com/SpencerGoulette/LED-Music-Visualizer/blob/master/FreqtoVolt.JPG)

The input to the circuit is the audio. I used just the right audio for the input audio. The 5V pin from the Raspberry Pi was used for the MCP6004 quad op-amp's power supply and for the voltage at the gate of the 2N3906 PNP BJT. A 1N914 diode was used in the circuit.

# How it Works
The audio input went through a 4 screw terminal male headphone balum converter adapter and the output for a speaker went through a 4 screw terminal female headphone balum converter adapter. A splitter could have been used to get rid of one of the adapters. The 4 terminals are for GND, BLANK, RIGHT, and LEFT. The RIGHT audio was taken and connected up to a negative feedback op-amp. This was done due to the audio's voltage being too small to affect the circuit. The audio's peak when tested was around 500mV, instead of the desired ~5V. So, a 1k and 10k were placed in the feedback of the op-amp to give it a theoretical gain of 11. The output from the op-amp was then used to switch a capacitor from charging to discharging. The more frequent the switching, the higher the voltage the capacitor would charge to. The voltage on the output of the frequency to voltage circuit was then read by an MCP3008 ADC. The Raspberry Pi used SPI to communicate with the ADC to get the voltage from the ADC. Then using python, the voltage was used to determine the color of the LEDs to be displayed. The colors were then displayed on the LED strip.

# Future Work
