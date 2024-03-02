## basicDDC

- A very basic Tk-based program to control the brightness and contrast of your monitors using ddccontrol.
- Motivation: gddccontrol is too powerful and a bit slow (because it scans for monitor buses on every startup, which has its advantages) and requires extra clicks.
- Be warned, the GUI and functionality are very minimalistic:
  - Currently only for brightness and contrast, RGB max/min level could be added, but I haven't needed it yet.
  - You have to quickly configure it in code for your monitor setup, and it will most likely not work for other setups.

#### Getting Started  

1. Fulfill the dependency [ddccontrol](https://github.com/ddccontrol/ddccontrol?tab=readme-ov-file#installation).
2. Configure – in code:
   1. identify the ID of the compatible monitors: look for "dev:/dev/i2c-ID" in the output of ```ddccontrol -p```
   2. edit/add "Monitor" object in/to "monitors" list with the respective ID
   3. define the order of the slider pairs (brightness, contrast) of multiple monitors (from top to bottom) according to the order of the Monitor in the list (from left to right)
   4. define optional text describing each monitor
   5. (error when moving a slider:) the address for brightness, contrast might vary from the default – check ```ddccontrol -p```
   6. ... tweak the code to your liking, get inspired, or burn it all down
3. Execute on Linux ```python basicddc.py```, or wherever you get ddccontrol and Python to run.

*hmpf, too much doc for so little code*
