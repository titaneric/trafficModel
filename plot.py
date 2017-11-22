import csv
import os
import math

import matplotlib.pyplot as plt
import matplotlib.pylab as plab


def stat():
    exp_list = list()
    exp_dir = os.path.join(os.getcwd(), "data")
    for f in sorted(os.listdir(exp_dir)):
        f_path = os.path.join(exp_dir, f)
        with open(f_path) as csvfile:
            reader = csv.DictReader(csvfile)
            total_speed = 0.0
            total_flow = 0
            total_density = 0.0
            for row in reader:
                total_speed += float(row["avgSpeed"])
                total_flow += int(row["flow"])
                total_density += float(row["avgDensity"])
            avg_speed = total_speed / 10000
            avg_flow = total_flow / 10000
            avg_density = total_density / 10000
            exp_list.append({"avgSpeed": avg_speed, 
                            "avgFlow": avg_flow,
                            "avgDensity": avg_density})
            csvfile.close()

    with open(os.path.join(os.getcwd(), "result", "stat.csv"), "w") as f:
        colName = ["avgSpeed", "avgFlow", "avgDensity"]
        fwriter = csv.DictWriter(f, fieldnames=colName)
        fwriter.writeheader()
        fwriter.writerows(exp_list)
        f.close()
    
def plot():
    with open(os.path.join(os.getcwd(), "result", "stat.csv"), "r") as f:
        reader = csv.DictReader(f)
        speed_list = []
        flow_list = []
        density_list = []
        for row in reader:
            speed_list.append(float(row["avgSpeed"]))
            flow_list.append(float(row["avgFlow"]))
            density_list.append(float(row["avgDensity"]))
        f.close()
    plt.plot(density_list, speed_list, "r+")
    plt.xlabel("Network density")
    plt.ylabel("Network speed")
    plt.axis([0, 0.02, 0, 5])
    plab.savefig(os.path.join(os.getcwd(), "result", "density_speed.png"))

    plt.plot(density_list, flow_list, "r+")
    plt.xlabel("Network density")
    plt.ylabel("Network flow")
    plt.axis([0, 0.02, 0, 0.7])
    plab.savefig(os.path.join(os.getcwd(), "result", "density_flow.png"))

    plt.plot(flow_list, speed_list, "r+")
    plt.xlabel("Network flow")
    plt.ylabel("Network speed")
    plt.axis([0, 0.7, 0, 5])
    plab.savefig(os.path.join(os.getcwd(), "result", "flow_speed.png"))

if __name__ == "__main__":
    stat()
    plot()

    