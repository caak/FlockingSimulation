import matplotlib.pyplot as plt

layout = 'hourglass'
intruder_type = 'nonflocker'


cs = []
FPRs = []
TPRs = []

filename = layout + '/' + intruder_type + '/roc_1_0.01.dat'
# filename = layout + '/' + intruder_type + '/results_5_5.dat'



with open(filename, 'r') as f:
    line = f.readline()
    title = 'p_std, v_std = ' + line
    line = f.readline()
    line = f.readline()
    while line != '':
        values = line.split(',')
        cs.append(float(values[0].strip()))
        FPRs.append(float(values[2].strip()))
        TPRs.append(float(values[1].strip()))
        line = f.readline()

plt.ylim((0, 1))
plt.plot(FPRs, TPRs, marker='o')

x_offset = 25
y_offset = -25
c_labels = [1.0, 1.3, 2.0]

for x,y,c in zip(FPRs,TPRs, cs):
    if round(c, 2) not in c_labels:
        continue
    label = "{:.2f}".format(c)

    plt.annotate(label, # this is the text
                 (x,y), # this is the point to label
                 textcoords="offset points", # how to position the text
                 xytext=(x_offset,y_offset), # distance from text to points (x,y)
                 ha='center', # horizontal alignment can be left, right or center
                 size =20)
    if int(c*10) == 15:
        y_offset = -5
        x_offset = 35
        print('gotem')

ax = plt.gca()
ax.tick_params(labelsize='20')
plt.title(title, size= 20)
plt.show()