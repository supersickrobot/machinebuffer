from matplotlib import pyplot as plt
import matplotlib; matplotlib.use("TkAgg")
from matplotlib import animation

def run():
    #attendance vs autonomoy
    mb1 = {'b0': {'size': 100, 'type': 'buffer', 'point': 'm1'},
           'm1': {'batch': 10, 'rate': 1, 'type': 'machine', 'point': 'b1'},
           'b1': {'size': 10, 'type': 'buffer', 'point': 'm2'},
           'm2': {'batch': 4, 'rate': 2, 'type': 'machine', 'point': 'b2'},
           'b2': {'size': 100, 'type': 'buffer', 'point': 'm3'},
           'm3': {'batch': 2, 'rate': 1, 'type': 'machine', 'point': 'b3'},
           'b3': {'size': 100, 'type': 'buffer', 'point': 'end'}}

    maxtime = 100
    # print(len(mb1)
    mbspace = [[0 for x in range(len(mb1))] for y in range(maxtime)]
    for ele in mb1:
        mb1[ele]['timer'] = 0
        mb1[ele]['space'] = 0
        if ele == 'b0':
            mb1[ele]['space'] = mb1[ele]['size']
    for i in range(0, maxtime):
        for iter, j in enumerate(mb1):
            if mb1[j]['type'] == 'machine':
                # if the element is a machine
                if mb1[j]['timer'] <= 0:
                    # if the timer is zero
                    if mb1[j]['space'] > 0:
                        for ele, info in mb1.items():
                            if mb1[j]['point'] == ele:
                                mb1[ele]['space'] = mb1[ele]['space'] + mb1[j]['space']
                                mb1[j]['space'] = 0
                                break

                    for ele, info in mb1.items():
                        if j == info['point']:
                            btc = mb1[j]['batch']
                            if mb1[ele]['space'] >= btc:
                                mb1[ele]['space'] = mb1[ele]['space']-btc
                                mb1[j]['space'] = btc
                                mb1[j]['timer'] = mb1[j]['rate']
                            break
                mb1[j]['timer'] = mb1[j]['timer']-1
            number = mb1[j]['space']
            mbspace[i][iter] = int(number)
        # print(mbspace)


    def barlist(n):
        return mbspace[n]

    fig, ax = plt.subplots(2)
    nums=[2, 22]
    x = mb1.keys()
    barcollection = ax[1].bar(x, barlist(1))
    pie = ax[0].pie(nums)
    xx = [[''] for i in range(0, len(mb1))]
    nl = '\n'
    for iter, i in enumerate(mb1):
        if mb1[i]['type'] == 'machine':
            xx[iter]=f'{i},{nl} {mb1[i]["batch"]}p / {mb1[i]["rate"]}hrs'
        else:
            xx[iter]=f'{i}'

    ax[1].set_xticklabels(xx)
    for item in barcollection[1::2]:
        item.set_color('g')
    colors = ['black', 'gold']
    def animate(i):
        y = barlist(i)
        ax[0].clear
        nums = [24-(i % 24), i % 24]
        ax[0].pie(nums, colors=colors)
        for i, b in enumerate(barcollection):
            b.set_height(y[i])

    anim = animation.FuncAnimation(fig, animate, repeat=True, blit=False, frames=maxtime, interval=100)

    plt.show()




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run()

