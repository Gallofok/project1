from tkinter import *


class round_controller:

    def __init__(self, root, frame):

        self.root = root
        self.frame = frame

        self.canvas = Canvas(self.frame, width=400, height=400, borderwidth=0, highlightthickness=0)

        self.centrepos = (200, 200)
        self.tri1, self.tri2, self.tri3, self.tri4 = self.createfourtriangle(centerpos=self.centrepos)
        self.rad = (60, 40, 20)
        self.angstart = (45, 135, 225, -45)
        self.angend = (135, 225, 315, 45)
        self.arclise = []
        self.colorlis = ["#2ECC71", "#F4D03F", "#5DADE2"]  # green yellow blue
        self.colorlishighlight = ["#28B463", "#F1C40F", "#3498DB"]  # corresponding colors

        for j in range(4):
            for i in range(3):
                self.arclise.append(
                    self.circle_arcit(self.centrepos[0], self.centrepos[1], self.rad[i], fill=self.colorlis[i],
                                      start=self.angstart[j], end=self.angend[j],
                                      activefill=self.colorlishighlight[i]))

        self.canvas.tag_bind(self.arclise[0], '<Button-1>', self.cli)

        self.canvas.tag_bind(self.arclise[1], '<Button-1>', self.cli2)

        self.canvas.tag_bind(self.arclise[2], '<Button-1>', self.cli3)

        self.canvas.grid()


    def cli(self, event):
        print("HI1")

    def cli2(self, event):
        print("HI2")

    def cli3(self, event):
        print("HI3")

    def createfourtriangle(self, centerpos, distance=110):

        tri1pts = [centerpos[0] - distance, centerpos[1] - 10, centerpos[0] - distance, centerpos[1] + 10,
                   centerpos[0] - distance - 20, centerpos[1]]
        tri2pts = [centerpos[0] + distance, centerpos[1] - 10, centerpos[0] + distance, centerpos[1] + 10,
                   centerpos[0] + distance + 20, centerpos[1]]
        tri3pts = [centerpos[0], centerpos[1] - 20 - distance, centerpos[0] - 10, centerpos[1] - distance,
                   centerpos[0] + 10, centerpos[1] - distance]
        tri4pts = [centerpos[0], centerpos[1] + 20 + distance, centerpos[0] - 10, centerpos[1] + distance,
                   centerpos[0] + 10, centerpos[1] + distance]
        self.tri1 = self.canvas.create_polygon(tri1pts, fill='#E74C3C', activefill="red")
        self.tri2 = self.canvas.create_polygon(tri2pts, fill='#E74C3C', activefill="red")
        self.tri3 = self.canvas.create_polygon(tri3pts, fill='#E74C3C', activefill="red")
        self.tri4 = self.canvas.create_polygon(tri4pts, fill='#E74C3C', activefill="red")
        self.canvas.create_text(centerpos[0] - distance - 40, centerpos[1], text="-x")
        self.canvas.create_text(centerpos[0] + distance + 40, centerpos[1], text="+x")
        self.canvas.create_text(centerpos[0], centerpos[1] - distance - 40, text="+y")
        self.canvas.create_text(centerpos[0], centerpos[1] + distance + 40, text="-y")
        return self.tri1, self.tri2, self.tri3, self.tri4

    def circle_arcit(self, x, y, r, **kwargs):
        if "start" in kwargs and "end" in kwargs:
            kwargs["extent"] = kwargs["end"] - kwargs["start"]
            del kwargs["end"]
        return self.canvas.create_arc(x - r, y - r, x + r, y + r, **kwargs)

    def circleit(self, x, y, r, **kwargs):
        return self.canvas.create_oval(x - r, y - r, x + r, y + r, **kwargs)


if __name__ == "__main__":
    root = Tk()
    frame = Frame(root)

    round_controller(root, root)

    root.mainloop()
