# study_in_entropy

A Raspberry Pi pico project running Micropython which interrogates the NIST randomness beacon and displays the interpreted output on a series of 42 WS2812B RGB LEDs

![photo_new](https://github.com/user-attachments/assets/26def34b-f47a-4962-a53e-559a804cdda8)



The project uses an API call to the NIST Interoperable Randomness Beacon https://csrc.nist.gov/projects/interoperable-randomness-beacons/ and uses the 512bit number to map to the RGB of 42 LEDs

## Project Code

The project code can be found here: https://github.com/bigcrimping/study_in_entropy/tree/main/code

You will need to load Micropython onto the Raspberry Pi Pico and add your own WiFI details to the secrets file then upload the two .py to the board (I use Thonny)

The lights turn on RED when the unit starts up to signify it has not connected to WiFI, turns GREEN once WiFi is connected then updates the display every ~60 seconds for fresh data



https://github.com/user-attachments/assets/d2951986-0e88-45ad-b2fb-9b8995b4adb6



## Wiring

Pretty simple wiring, the LEDs are powered off the board 5V and the data pin is connected to pin16 in my case

![PXL_20241208_183550397](https://github.com/user-attachments/assets/8205d631-c448-4963-a02e-ccc2876c934c)

The LEDs are in rows of 7 and need to be joined between rows

![leds](https://github.com/user-attachments/assets/d84263f3-3c0e-4c1b-b9ac-a2d2a1e6bca2)

## Mechanical Files

The mechanical files can be found here: https://github.com/bigcrimping/study_in_entropy/tree/main/mech

Hopefully the files are explanatory, the front friction fits onto the back, the stand is attached with M3 DIN912 caphead into M3 threaded inserts.

![mech](https://github.com/user-attachments/assets/47684f5b-1c22-4c9e-87ec-452cd7ebce41)


The Raspberry Pi Pico uses M1.6 threaded inserts and cross head screws


![insert](https://github.com/user-attachments/assets/3d1da86b-5eef-41c8-ad0e-7fff1fe37c25)
