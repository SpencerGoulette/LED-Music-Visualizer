# LED-Music-Visualizer
LED Music Visualizer Project created over the Winter Break of 2018-2019. The idea for the project was obtained from Devon Crawford. His project can be seen here:
https://www.youtube.com/watch?v=lU1GVVU9gLU

# Equipment
- WS2812B LEDS
https://www.amazon.com/dp/B01CDTEG1O/ref=pd_luc_rh_sspa_dk_huc_pt_expsub_0?psc=1

- Raspberry Pi 3 Model B+
https://www.amazon.com/Raspberry-Pi-RASPBERRYPI3-MODB-1GB-Model-Motherboard/dp/B01CD5VC92/ref=sr_1_12?s=electronics&ie=UTF8&qid=1546032686&sr=1-12&keywords=raspberry+pi+3+b%2B

- Frequency to Voltage Circuit (multiple components needed)
    
    MCP6004 Op-amp
    https://www.microchip.com/wwwproducts/en/MCP6004
    
    MCP3008 ADC
    https://www.adafruit.com/product/856
    
    2N3906 BJT
    https://www.digikey.com/product-detail/en/micro-commercial-co/2N3906-AP/2N3906-APCT-ND/950592
    
    1N914 Diode
    https://www.digikey.com/product-detail/en/microsemi-corporation/1N914/1N914MS-ND/4377361
    
    4 Screw Terminal Male and Female Headphone Balum Converter Adapter
    https://www.amazon.com/Cerrxian-Terminal-Headphone-Converter-Adapter/dp/B06W2K9XMM/ref=pd_day0_hl_23_2?_encoding=UTF8&pd_rd_i=B06W2K9XMM&pd_rd_r=edcaf6bd-0ae9-11e9-91e2-f976ad544836&pd_rd_w=pbfS1&pd_rd_wg=tJ8cY&pf_rd_p=ad07871c-e646-4161-82c7-5ed0d4c85b07&pf_rd_r=DXZPK6682GCNRN6YPEPQ&psc=1&refRID=DXZPK6682GCNRN6YPEPQ
    
    https://www.amazon.com/Cerrxian-Terminal-Headphone-Converter-Adapter/dp/B07BHBQ5YV/ref=pd_bxgy_23_img_2?_encoding=UTF8&pd_rd_i=B07BHBQ5YV&pd_rd_r=604189a5-0aef-11e9-ba23-290598a1709c&pd_rd_w=YpJGU&pd_rd_wg=HQRdB&pf_rd_p=6725dbd6-9917-451d-beba-16af7874e407&pf_rd_r=AQX47WZ76403PVH8KJ8Y&psc=1&refRID=AQX47WZ76403PVH8KJ8Y
    
    1K Ohm Resistor
    https://www.digikey.com/product-detail/en/stackpole-electronics-inc/CF14JT1K00/CF14JT1K00CT-ND/1830350
    
    2.2K Ohm Resistor
    https://www.digikey.com/product-detail/en/stackpole-electronics-inc/CF14JT2K20/CF14JT2K20CT-ND/1830358
    
    10K Ohm Resistor
    https://www.digikey.com/product-detail/en/stackpole-electronics-inc/CF14JT10K0/CF14JT10K0CT-ND/1830374
    
    1uF Capacitor
    https://www.digikey.com/product-detail/en/nichicon/UMA1H010MCD2TP/493-10419-1-ND/4312678
    
    100uF Capacitor
    https://www.digikey.com/product-detail/en/rubycon/35ZLH100MEFC6.3X11/1189-1300-ND/3134256

# Frequency to Voltage Circuit
Below is the circuit used to convert the frequency of the audio to voltage.
![alt text](https://github.com/SpencerGoulette/LED-Music-Visualizer/blob/master/FreqtoVolt.JPG)

The input to the circuit is the audio. I used just the RIGHT audio for the input audio. The 5V pin from the Raspberry Pi was used for the MCP6004 quad op-amp's power supply and for the voltage at the gate of the 2N3906 PNP BJT. A 1N914 diode was used in the circuit.

# How it Works
The audio input went through a 4 screw terminal male headphone balum converter adapter and the output for a speaker went through a 4 screw terminal female headphone balum converter adapter. A splitter could have been used to get rid of one of the adapters. The 4 terminals are for GND, BLANK, RIGHT, and LEFT. The RIGHT audio was taken and connected up to a negative feedback op-amp. This was done due to the audio's voltage being too small to affect the circuit. The audio's peak when tested was around 500mV, instead of the desired ~5V. So, a 1k and 10k were placed in the feedback of the op-amp to give it a theoretical gain of 11. The output from the op-amp was then used to switch a capacitor from charging to discharging. The more frequent the switching, the higher the voltage the capacitor would charge to. The voltage on the output of the frequency to voltage circuit was then read by an MCP3008 ADC. The Raspberry Pi used SPI to communicate with the ADC to get the voltage from the ADC. Then using python, the voltage was used to determine the color of the LEDs to be displayed. The colors were then displayed on the LED strip.

- The 1k resistor was replaced with a potentiometer to adjust the amplification based off of the differing volume inputs.

# Future Work
Currently, there is a small window for frequencies (~200Hz to ~700 Hz). I want to get this sweet spot larger and have it so that the colors will change more noticeably from small changes in the frequency. I would like to get the LEFT audio too, which I can just do by running through the circuit and having it on channel 2 (RIGHT audio is on channel 1). I do not know how I would use both the left and right audio yet. A big issue I need to fix is that as you lower the volume, the less it affects the circuit and changes the voltage. I usually have to play it at the max on my headphones for it to work. So, I would like to somehow have the circuit figure out what the peak amplitude of the audio is and then amplify accordingly to get it ~5V. This way, no matter what the volume, there will be an output voltage and the LEDs will work. The last thing I want to work on is have the code all in C. I am currently working on that, but I am having issues with the Pi not being able to transmit data to the LEDs fast enough. Lastly, I have been requested to do a FFT to get the frequencies and then display them as a frequency bar visual using the LEDs.
