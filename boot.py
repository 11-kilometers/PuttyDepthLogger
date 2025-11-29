import board, digitalio, storage, usb_cdc
usb_cdc.enable(console=True, data=False)

mode = digitalio.DigitalInOut(board.D9)
mode.switch_to_input(pull=digitalio.Pull.UP)

if mode.value:
    storage.remount("/", readonly=True)        # Host RW CIRCUITPY
    storage.remount("/sd", readonly=False)     # CP RW SD (Host RO)
    print("Mode: HIGH → Host RW CIRCUITPY | CP RW SD")
else:
    storage.remount("/sd", readonly=True)      # Host RW SD
    storage.remount("/", readonly=False)       # CP RW CIRCUITPY (Host RO)
    print("Mode: LOW → Host RW SD | CP RW CIRCUITPY")
