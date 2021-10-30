from matplotlib.pyplot import cm 
color=cm.rainbow(np.linspace(0,1,len(emotions)))
color = dict(zip(emotions, color))
color