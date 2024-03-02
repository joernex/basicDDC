"""
basicDDC – A very basic Tk-based program to control the brightness and contrast of your monitors using ddccontrol.
Dependency: ddccontrol
OS: Linux

Copyright (C) 2024 enigamus
This program is free software: you can redistribute it and/or modify it under the terms of the
GNU General Public License as published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
"""

__version__ = "0.1.0"

import re
import subprocess
import tkinter as tk


class Monitor:
    def __init__(self, id_: str, **kwargs):
        self.device = id_
        self.brightness = kwargs.get("brightness", 0x10)
        self.contrast = kwargs.get("contrast", 0x12)
        self.comment = kwargs.get("comment", "")

    def get_value(self, key: str):
        return re.search(
            r"\+\/(\d{1,3})\/100 C",
            subprocess.run(
                ["ddccontrol", "-r", str(getattr(self, key)), "dev:/dev/i2c-" + self.device],
                shell=False, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
            ).stdout.decode("utf-8").strip()
        ).group(1)

    def set_value(self, key: str, val):
        subprocess.run(
            ["ddccontrol", "-r", str(getattr(self, key)), "-w", val, "dev:/dev/i2c-" + self.device],
            shell=False, capture_output=True
        )


if __name__ == "__main__":
    monitors = [Monitor(id_="9", comment="read if cute", ), ]  # edit here

    window = tk.Tk()
    window.title("basicDDC")
    window.resizable(False, False)

    for i, monitor in enumerate(monitors):
        if monitor.comment:
            label = tk.Label(window, text=monitor.comment, font=("TkTextFont", 10), fg="black")
            label.pack(anchor='w')

        brightness = tk.Scale(window, from_=1, to=100, orient=tk.HORIZONTAL, command=lambda val: monitor.set_value("brightness", val))
        contrast = tk.Scale(window, from_=1, to=100, orient=tk.HORIZONTAL, command=lambda val: monitor.set_value("contrast", val))

        brightness.set(monitor.get_value("brightness"))
        contrast.set(monitor.get_value("contrast"))

        brightness.pack()
        contrast.pack()

        if (i + 1) != len(monitors):
            separator = tk.Frame(window, height=1, bg="black")
            separator.pack(fill="x", padx=5, pady=5)

    window.mainloop()
