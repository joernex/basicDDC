"""
basicDDC – A very basic Tk-based program to control the brightness and contrast of your monitors using ddccontrol.
Dependency: ddccontrol
OS: Linux

Copyright (C) 2024 joernex
This program is free software: you can redistribute it and/or modify it under the terms of the
GNU General Public License as published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
"""

__version__ = "0.1.1"

import argparse
import re
import subprocess
import tkinter as tk


class Monitor:
    def __init__(self, id_: str, **kwargs):
        self.device = id_
        self.brightness = kwargs.get("brightness", 0x10)
        self.contrast = kwargs.get("contrast", 0x12)
        self.comment = kwargs.get("comment", "")

    def get_value(self, key: str) -> int:
        return int(re.search(
            r"\+\/(\d{1,3})\/100 C",
            subprocess.run(
                ["ddccontrol", "-r", str(getattr(self, key)), "dev:/dev/i2c-" + self.device],
                shell=False, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
            ).stdout.decode("utf-8").strip()
        ).group(1))

    def set_value(self, key: str, val):
        subprocess.run(
            ["ddccontrol", "-r", str(getattr(self, key)), "-w", str(max(min(int(val), 100), 0)), "dev:/dev/i2c-" + self.device],
            shell=False, capture_output=True
        )

    def get_id(self):
        return self.device


if __name__ == "__main__":
    monitors = [Monitor(id_="9", comment="read if cute", ), ]  # edit here

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--brightness",
        dest="brightness",
        type=int,
        choices=range(-100, 101),
        metavar="[-100, 100]",
    )
    parser.add_argument(
        "--contrast",
        dest="contrast",
        type=int,
        choices=range(-100, 101),
        metavar="[-100, 100]",
    )
    parser.add_argument(
        "--id",
        dest="id",
        type=str,
        nargs="+",
    )
    args = parser.parse_args()

    if args.id:
        for id_ in args.id:
            monitor = [m for m in monitors if m.get_id() == id_][0]
            if args.brightness:
                monitor.set_value("brightness", monitor.get_value("brightness") + args.brightness)
            if args.contrast:
                monitor.set_value("contrast", monitor.get_value("contrast") + args.contrast)
    else:
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
