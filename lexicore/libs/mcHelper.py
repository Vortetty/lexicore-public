from PIL import Image

def front(sim, slim):
    im = Image.new("RGBA", (16, 32*3+2))

    def cp(x1, y1, w, h, x2, y2, xoffset=0, yoffset=0):
        tim = sim.crop((x1, y1, x1+w, y1+h))
        im.paste(tim, (x2+xoffset, y2+yoffset), mask=tim)

    def cmp():
        tim = im.crop((0, 0, 16, 32))
        im.paste(tim, (0, 66), mask=tim)
        tim = im.crop((0, 33, 16, 66))
        im.paste(tim, (0, 66), mask=tim)

    if sim.size[1] == 32:
        cp(8, 8, 8, 8, 4, 0)  # head
        cp(20, 20, 8, 12, 4, 8)  # body
        cp(44, 20, 4, 12, 12, 8)  # right arm
        cp(44, 20, 4, 12, 0, 8)  # left arm
        cp(4, 20, 4, 12, 4, 20)  # right leg
        cp(4, 20, 4, 12, 8, 20)  # left leg

        cp(40, 8, 8, 8, 4, 0, yoffset=33)  # hat

        cmp()
    elif sim.size[1] == 64:
        cp(8, 8, 8, 8, 4, 0)  # head
        cp(20, 20, 8, 12, 4, 8)  # body
        cp(44, 20, 4, 12, 12, 8)  # right arm
        cp(36, 52, 4, 12, 0, 8)  # left arm
        cp(4, 20, 4, 12, 4, 20)  # right leg
        cp(20, 52, 4, 12, 8, 20)  # left leg

        cp(40, 8, 8, 8, 4, 0, yoffset=33)  # hat
        cp(20, 36, 8, 12, 4, 8, yoffset=33)  # jacket
        cp(44, 36, 4, 12, 12, 8, yoffset=33)  # right sleeve
        cp(52, 52, 4, 12, 0, 8, yoffset=33)  # left sleeve
        cp(4, 36, 4, 12, 4, 20, yoffset=33)  # right leg sleeve
        cp(4, 52, 4, 12, 8, 20, yoffset=33)  # left leg sleeve

        cmp()

    return im


def back(sim, slim):
    im = Image.new("RGBA", (16, 32*3+2))

    def cp(x1, y1, w, h, x2, y2, xoffset=0, yoffset=0):
        tim = sim.crop((x1, y1, x1+w, y1+h))
        im.paste(tim, (x2+xoffset, y2+yoffset), mask=tim)

    def cmp():
        tim = im.crop((0, 0, 16, 32))
        im.paste(tim, (0, 66), mask=tim)
        tim = im.crop((0, 33, 16, 66))
        im.paste(tim, (0, 66), mask=tim)

    if sim.size[1] == 32:
        cp(8, 8, 8, 8, 4, 0)  # head
        cp(32, 20, 8, 12, 4, 8)  # body
        cp(52, 20, 4, 12, 12, 8)  # right arm
        cp(52, 20, 4, 12, 0, 8)  # left arm
        cp(12, 20, 4, 12, 4, 20)  # right leg
        cp(12, 20, 4, 12, 8, 20)  # left leg

        cp(40, 8, 8, 8, 4, 0, yoffset=33)  # hat

        cmp()
    elif sim.size[1] == 64:
        cp(24, 8, 8, 8, 4, 0)  # head
        cp(32, 20, 8, 12, 4, 8)  # body
        cp(44, 20, 4, 12, 12, 8)  # right arm
        cp(36, 52, 4, 12, 0, 8)  # left arm
        cp(12, 20, 4, 12, 4, 20)  # right leg
        cp(28, 52, 4, 12, 8, 20)  # left leg

        cp(56, 8, 8, 8, 4, 0, yoffset=33)  # hat
        cp(28, 36, 8, 12, 4, 8, yoffset=33)  # jacket
        cp(52, 36, 4, 12, 12, 8, yoffset=33)  # right sleeve
        cp(60, 52, 4, 12, 0, 8, yoffset=33)  # left sleeve
        cp(12, 36, 4, 12, 4, 20, yoffset=33)  # right leg sleeve
        cp(12, 52, 4, 12, 8, 20, yoffset=33)  # left leg sleeve

        cmp()

    return im

def right(sim, slim):
    im = Image.new("RGBA", (8, 32*3+2))

    def cp(x1, y1, w, h, x2, y2, xoffset=0, yoffset=0):
        tim = sim.crop((x1, y1, x1+w, y1+h))
        im.paste(tim, (x2+xoffset, y2+yoffset), mask=tim)

    def cmp():
        tim = im.crop((0, 0, 8, 32))
        im.paste(tim, (0, 66), mask=tim)
        tim = im.crop((0, 33, 8, 66))
        im.paste(tim, (0, 66), mask=tim)

    if sim.size[1] == 32:
        cp(0, 8, 8, 8, 0, 0)  # head
        cp(40, 20, 4, 12, 2, 8)  # arm
        cp(0, 20, 4, 12, 2, 20)  # leg

        cp(32, 8, 8, 8, 0, 0, yoffset=33)  # hat

        cmp()
    elif sim.size[1] == 64:
        cp(0, 8, 8, 8, 0, 0)  # head
        cp(40, 20, 4, 12, 2, 8)  # arm
        cp(0, 20, 4, 12, 2, 20)  # leg

        cp(32, 8, 8, 8, 0, 0, yoffset=33)  # hat
        cp(40, 36, 4, 12, 2, 8, yoffset=33)  # sleeve
        cp(0, 36, 4, 12, 2, 20, yoffset=33)  # leg sleeve

        cmp()

    return im

def left(sim, slim):
    im = Image.new("RGBA", (8, 32*3+2))

    def cp(x1, y1, w, h, x2, y2, xoffset=0, yoffset=0):
        tim = sim.crop((x1, y1, x1+w, y1+h))
        im.paste(tim, (x2+xoffset, y2+yoffset), mask=tim)

    def cmp():
        tim = im.crop((0, 0, 8, 32))
        im.paste(tim, (0, 66), mask=tim)
        tim = im.crop((0, 33, 8, 66))
        im.paste(tim, (0, 66), mask=tim)

    if sim.size[1] == 32:
        cp(16, 8, 8, 8, 0, 0)  # head
        cp(48, 20, 4, 12, 2, 8)  # arm
        cp(8, 20, 4, 12, 2, 20)  # leg

        cp(48, 8, 8, 8, 0, 0, yoffset=33)  # hat

        cmp()
    elif sim.size[1] == 64:
        cp(16, 8, 8, 8, 0, 0)  # head
        cp(36, 52, 4, 12, 2, 8)  # arm
        cp(24, 52, 4, 12, 2, 20)  # leg

        cp(48, 8, 8, 8, 0, 0, yoffset=33)  # hat
        cp(56, 52, 4, 12, 2, 8, yoffset=33)  # sleeve
        cp(8, 52, 4, 12, 2, 20, yoffset=33)  # leg sleeve

        cmp()

    return im
