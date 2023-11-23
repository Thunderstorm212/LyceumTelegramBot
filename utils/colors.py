class Colors:
    def __init__(self, string, color: str):
        colors_list = {
            "black": f"\033[30m",
            "red": f"\033[31m",
            "green": f"\033[32m",
            "yalow": f"\033[33m",
            "blue": f"\033[34m",
            "violet": f"\033[35m",
            "turquoise": f"\033[36m"
        }
        self.color = color.lower()
        self.string = string
        if self.color in colors_list.keys():
            colors_list.get(self.color)
        if self.color[0] == "#":
            self.hex_color()
        else:
            exit()

    def __repr__(self):
        return str(self.string)

    def hex_color(self):
        if len(self.color[1:]) == 3:
            self.color = "#" + (self.color[1] * 2) + (self.color[2] * 2) + (self.color[3] * 2)
        r = int(self.color[1:3], 16)
        g = int(self.color[3:5], 16)
        b = int(self.color[5:7], 16)

        ansi_code = 16 + (36 * int(r / 255 * 5)) + (6 * int(g / 255 * 5)) + int(b / 255 * 5)

        self.string = f"\033[38;5;{ansi_code}m{self.string}\033[0m"


