from random import shuffle as importedShuffle
import colorsys
#import pandas as pd
#import plotly.express as px
from matplotlib import pyplot as plt
from PIL import Image

class sortable():
    def __init__(self, size: int, visual=False, showAccesses=False, printConsole=False, gif=False):
        self.size = size
        self.__list = list(range(1, size+1))
        self.visual = visual
        self.printConsole = printConsole
        self.lastgotten = 0
        self.showAccesses = showAccesses
        self.step = 0
        #self.series = pd.DataFrame([[str(self.step), str(i), self.__list[i]] for i in range(self.size)], columns = ['step', 'bar', 'value'])
        self.bars = plt.bar(list(range(size)), self.__list, width=1)
        self.images = []
        self.gif = gif
        self.widHig = (0, 0)

        if self.gif:
            plt.gcf().canvas.draw()
            self.widHig = plt.gcf().canvas.get_width_height()
            self.images.append(Image.frombytes('RGB', plt.gcf().canvas.get_width_height(), plt.gcf().canvas.tostring_rgb()))

    def shuffle(self):
        importedShuffle(self.__list)
        if self.visual:
            self.step += 1
            #self.series = self.series.append(pd.DataFrame([[str(self.step), str(i), self.__list[i]] for i in range(self.size)], columns = ['step', 'bar', 'value']), ignore_index=True)
            for i in range(self.size):
                self.bars[i].set_height(self.__list[i])
                self.bars[i].set_color(colorsys.hsv_to_rgb(self.bars[i].get_height()/self.size,1,1))
                plt.pause(0.0000000001)
                if self.gif:
                    plt.gcf().canvas.draw()
                    self.images.append(Image.frombytes('RGB', plt.gcf().canvas.get_width_height(), plt.gcf().canvas.tostring_rgb()))
        if self.printConsole:
            print(self.__list)

    def shuffleFast(self):
        importedShuffle(self.__list)
        if self.visual:
            self.step += 1
            #self.series = self.series.append(pd.DataFrame([[str(self.step), str(i), self.__list[i]] for i in range(self.size)], columns = ['step', 'bar', 'value']), ignore_index=True)
            for i in range(self.size):
                self.bars[i].set_height(self.__list[i])
                self.bars[i].set_color(colorsys.hsv_to_rgb(self.bars[i].get_height()/self.size,1,1))
            plt.pause(0.0000000001)
            if self.gif:
                plt.gcf().canvas.draw()
                self.images.append(Image.frombytes('RGB', plt.gcf().canvas.get_width_height(), plt.gcf().canvas.tostring_rgb()))
        if self.printConsole:
            print(self.__list)

    def swap(self, pos1: int, pos2: int):
        self.__list[pos1], self.__list[pos2] = self.__list[pos2], self.__list[pos1]

        if self.visual:
            self.step += 1
            #self.series = self.series.append(pd.DataFrame([[str(self.step), str(i), self.__list[i]] for i in range(self.size)], columns = ['step', 'bar', 'value']), ignore_index=True)
            self.bars[pos1].set_height(self.__list[pos1])
            self.bars[pos1].set_color(colorsys.hsv_to_rgb(self.bars[pos1].get_height()/self.size,1,1))
            self.bars[pos2].set_height(self.__list[pos2])
            self.bars[pos2].set_color(colorsys.hsv_to_rgb(self.bars[pos2].get_height()/self.size,1,1))
            plt.pause(0.0000000001)
            if self.gif:
                plt.gcf().canvas.draw()
                self.images.append(Image.frombytes('RGB', plt.gcf().canvas.get_width_height(), plt.gcf().canvas.tostring_rgb()))
        if self.printConsole:
            print(self.__list)

    def set(self, pos:int, val: int):
        self.__list[pos] = val

        if self.visual:
            self.step += 1
            #self.series = self.series.append(pd.DataFrame([[str(self.step), str(i), self.__list[i]] for i in range(self.size)], columns = ['step', 'bar', 'value']), ignore_index=True)
            self.bars[pos].set_height(self.__list[pos])
            self.bars[pos].set_color(colorsys.hsv_to_rgb(self.bars[pos].get_height()/self.size,1,1))
            if self.gif:
                self.images.append(Image.frombytes('RGB', plt.gcf().canvas.get_width_height(), plt.gcf().canvas.tostring_rgb()))

    def get(self, pos: int):
        if self.visual:
            if self.showAccesses:
                self.bars[self.lastgotten].set_color(colorsys.hsv_to_rgb(self.bars[self.lastgotten].get_height()/self.size,1,1))
                self.bars[pos].set_color("0")
                self.lastgotten = pos
                plt.pause(0.0000000001)
        return self.__list[pos]

    def checkSorted(self):
        return self.__list == list(range(1, self.size + 1))

    def getList(self):
        return self.__list

    def closePlt(self):
        plt.close()
