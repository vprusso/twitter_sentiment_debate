import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style 
import time 

style.use("ggplot")

fig = plt.figure()
fig.canvas.set_window_title('Clinton tweet sentiment')

plt.title('Clinton tweet sentiment')
plt.suptitle('Clinton tweet sentiment')
plt.xlabel('Number of tweets')
plt.ylabel('Sentiment polarity')
ax1 = fig.add_subplot(1,1,1)

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def animate(i):
    pull_data = open("clinton_tweets.txt", "r").read()
    lines = pull_data.split("\n")

    xar = []
    yar = []

    x = 0
    y = 0

    for l in lines:
        x += 1    
        try:
            y += float(find_between(l, "POLARITY::", ","))
        except:
            y += 0
        xar.append(x)
        yar.append(y)

    ax1.clear()

    ax1.set_xlabel('Number of Tweets')
    ax1.set_ylabel('Tweet Sentiment')
    ax1.plot(xar,yar,color='b')

ani = animation.FuncAnimation(fig, animate, interval = 1000)
plt.show()