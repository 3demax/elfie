# Eachine E10 drone controller

This project emerged from my wish to control my E10 drone more comfortably with controller, because touchscreen control in official application sucks. Besides, it's always fun to hack your gadgets :)

# Pre-requisites

For this to work, you need computer that can run python, RaspberryPi or any other mini-computer with Linux would do.
Also, you need two-axis game controller.

# Dependencies

Create your virtual environment and run
```
pip install -r requirements.txt
```

# Running

Connect to drone's wifi AP

```
python2 kbd_flight.py
```

Make sure you have switched your controller into analog mode, so that axis produce values between -1.0 and 1.0

Enjoy!

# Acknowledgements

Big thanks to adria.junyent-ferre and his [project on reverse-engineering exactly same drone, but branded by JJRC](https://hackaday.io/project/19680-controlling-a-jjrc-h37-elfie-quad-from-a-pc) 