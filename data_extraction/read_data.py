import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

main_window = tk.Tk()

def new_temperature():
    base_temp = 25
    random_number = np.random.randint(0,10)
    if random_number%2==0:
        return base_temp + base_temp*random_number
    return base_temp - base_temp*random_number

def plot_graph(x,y):
    ax.clear()
    ax.scatter(x,y)
    plot_canvas.draw()


frame = tk.Frame(main_window)
label = tk.Label(text="Monitoramento do sistema", font=("Courier",32))
label.pack()
fig, ax = plt.subplots()
plot_canvas = FigureCanvasTkAgg(fig, master=frame)
plot_canvas.get_tk_widget().pack()

x_values = []
y_values = []
for i in range(10):
    x_values.append(new_temperature())
    y_values.append(i)
    ax.clear()
    ax.scatter(x_values,y_values)
    plot_canvas.draw()
    # plt.sleep(0.001)


frame.pack()

tk.Button(frame, text="Plot a graph", command=plot_graph).pack(pady=10)

main_window.mainloop()
