from cmath import log10
import numpy as np
import math
import os
import matplotlib.pyplot as plt
import matplotlib.transforms
# import latex
import matplotlib
from matplotlib.offsetbox import AnchoredOffsetbox, TextArea, HPacker, VPacker

class ChartGenerator:
    # data檔名 Y軸名稱 X軸名稱 Y軸要除多少(10的多少次方) Y軸起始座標 Y軸終止座標 Y軸座標間的間隔
    def __init__(self, dataName, Xlabel, Ylabel, Xpow, Ypow, Ystart, Yend, Yinterval):
        filename = './data/' + dataName

        if not os.path.exists(filename):
            print("file doesn't exist")
            return
        
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        print("start generate", filename)
        
        
        # Ydiv, Ystart, Yend, Yinterval

        # color = [
        #     "#000000",
        #     "#006400",
        #     "#FF1493",
        #     "#7FFF00",   
        #     "#900321",
        # ]
        color = [
            "#FF0000",
            "#00FF00",   
            "#0000FF",
            "#000000",
            "#900321",
        ]
        # matplotlib.rcParams['text.usetex'] = True

        fontsize = 35
        Xlabel_fontsize = fontsize
        Ylabel_fontsize = fontsize
        Xticks_fontsize = fontsize
        Yticks_fontsize = fontsize
            
        # fig, ax = plt.subplots(figsize=(8, 6), dpi=600) 
        
        andy_theme = {
        # "axes.grid": True,
        # "grid.linestyle": "--",
        # "legend.framealpha": 1,
        # "legend.facecolor": "white",
        # "legend.shadow": True,
        # "legend.fontsize": 14,
        # "legend.title_fontsize": 16,
        "xtick.labelsize": 20,
        "ytick.labelsize": 20,
        "axes.labelsize": 20,
        "axes.titlesize": 20,
        "font.family": "Times New Roman",
        "mathtext.default": "default"
        # "text.usetex": True,
        # "figure.dpi": 100,
        }
        
        matplotlib.rcParams.update(andy_theme)
        fig, ax1 = plt.subplots(figsize = (8, 7), dpi = 600)
        # ax1.spines['top'].set_linewidth(1.5)
        # ax1.spines['right'].set_linewidth(1.5)
        # ax1.spines['bottom'].set_linewidth(1.5)
        # ax1.spines['left'].set_linewidth(1.5)
        ax1.tick_params(direction = "in")
        ax1.tick_params(bottom = True, top = True, left = True, right = True)
        ax1.tick_params(pad = 15)


        ##data start##
        x = []
        _y = []
        numOfData = 0

        for line in lines:
            line = line.replace('\n','')
            data = line.split(' ')
            numOfline = len(data)
            numOfData += 1
            for i in range(numOfline):
                if i == 0:
                    x.append(data[i])
                else:
                    _y.append(data[i])        
        
        numOfAlgo = len(_y) // numOfData

        y = [[] for _ in range(numOfAlgo)]
        for i in range(numOfData * numOfAlgo):
            y[i % numOfAlgo].append(_y[i])

        # print(x)
        # print(y)

        maxData = 0
        minData = math.inf

        Ydiv = float(10 ** Ypow)
        Xdiv = float(10 ** Xpow)
        
        for i in range(numOfData):
            x[i] = float(x[i]) / Xdiv

        for i in range(numOfAlgo):
            for j in range(numOfData):
                y[i][j] = float(y[i][j]) / Ydiv
                maxData = max(maxData, y[i][j])
                minData = min(minData, y[i][j])

        marker = ['o', 's', 'v', 'x', 'd']
        for i in range(numOfAlgo):
            ax1.plot(x, y[i], color = color[i], lw = 2.5, linestyle = "-", marker = marker[i], markersize = 20, markerfacecolor = "none", markeredgewidth = 2.5)
        # plt.show()

        plt.xticks(fontsize = Xticks_fontsize)
        plt.yticks(fontsize = Yticks_fontsize)
        
        AlgoName = ["SEER", "Greedy", "Q-CAST", "REPS"]

        leg = plt.legend(
            AlgoName[0 : numOfAlgo],
            loc = 10,
            bbox_to_anchor = (0.4, 1.2),
            prop = {"size": fontsize, "family": "Times New Roman"},
            frameon = "False",
            labelspacing = 0.2,
            handletextpad = 0.2,
            handlelength = 1,
            columnspacing = 0.2,
            ncol = 2,
            facecolor = "None",
        )

        leg.get_frame().set_linewidth(0.0)
        Ylabel += self.genMultiName(Ypow)
        Xlabel += self.genMultiName(Xpow)
        
        plt.yticks(np.arange(Ystart, Yend + Yinterval, step = Yinterval), fontsize = Yticks_fontsize)
        plt.ylabel(Ylabel, fontsize = Ylabel_fontsize, labelpad = 50)
        plt.xlabel(Xlabel, fontsize = Xlabel_fontsize, labelpad = 10)
        # plt.show()
        plt.tight_layout()
        pdfName = dataName[0:-4].replace('#', '')
        plt.savefig('./pdf/Q_{}.eps'.format(pdfName)) 
        plt.savefig('./pdf/Q_{}.jpg'.format(pdfName)) 
        # Xlabel = Xlabel.replace(' (%)','')
        # Xlabel = Xlabel.replace('# ','')
        # Ylabel = Ylabel.replace('# ','')
        plt.close()

    def genMultiName(self, multiple):
        if multiple == 0:
            return str()
        else:
            return "($" + "10" + "^{" + str(multiple) + "}" + "$)"

    def myRound(self, x):
        if x < 1:
            return x
        x = int(x)
        head = int(str(x)[0])
        digit = len(str(x))
        return int((head + 1) * (10 ** (digit - 1)))

def getFilename(x, y):
    Xlabels = ["#RequestPerRound", "totalRequest", "#nodes", "r", "swapProbability", "alpha", "SocialNetworkDensity"]
    Ylabels = ["algorithmRuntime", "waitingTime", "idleTime", "usedQubits", "temporaryRatio"]
    return Xlabels[x] + "_" + Ylabels[y] + ".txt"

if __name__ == "__main__":
    # data檔名 Y軸名稱 X軸名稱 Y軸要除多少(10的多少次方) Y軸起始座標 Y軸終止座標 Y軸座標間的間隔
    # ChartGenerator("numOfnodes_waitingTime.txt", "need #round", "#Request of a round", 0, 0, 25, 5)
    Xlabels = ["#RequestPerRound", "totalRequest", "#nodes", "r", "swapProbability", "alpha", "SocialNetworkDensity"]
    Ylabels = ["algorithmRuntime", "waitingTime", "idleTime", "usedQubits", "temporaryRatio"]
    
    # Xlabel
    # 0 #RequestPerRound
    # 1 totalRequest
    # 2 #nodes
    # 3 r
    # 4 swapProbability
    # 5 alpha
    # 6 SocialNetworkDensity

    # Ylabel
    # 0 algorithmRuntime 
    # 1 waitingTime
    # 2 idleTime
    # 3 usedQubits
    # 4 temporaryRatio


    # rpr + waitingtime
    ChartGenerator(getFilename(0, 1), "$\\beta$(#requests / time slots)", "Waiting Time", 0, 0, 0, 15, 3)
    
    # alpha + ratio
    ChartGenerator(getFilename(5, 4), "$\\alpha$", "Temporary Ratio", -4, 0, 0, 1, 0.2)
    