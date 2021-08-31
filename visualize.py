import webbrowser
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
from pyecharts.charts import Pie
from pyecharts.charts import Bar3D
from pyecharts import options as opts

plt.rc("font", family="SimHei", size="12")  # 解决画图中文字体问题


def read():
    """ read """
    flow = pd.read_csv("result/metro-5-20191002-20191008-evening.csv", encoding="ANSI")
    name = pd.read_csv("txt/五号线站名.txt", encoding="ANSI", names=["STATION"])

    return flow, name


def add_statation_name(flow, name):
    # 经北二路站 这一站是不存在的 重新进行排列
    name = list(name["STATION"])
    name = name[::-1]
    flow["METRO_STATION_NAME"] = name

    return flow


def add_total_max(flow):
    x = []
    y = []
    total_max_counts = 0

    for i in flow.itertuples():
        counts = eval(i[2])
        total_counts = sum(counts)
        max_counts = max(counts)
        total_max_counts = max(max_counts, total_max_counts)
        angle = eval(i[3])
        max_flow_angle = angle.index(max(angle))

        if sum(angle) == 0:
            max_flow_angle = 8

        x.append(total_counts)
        y.append(max_flow_angle)

    flow["TOTAL_COUNTS"] = x
    flow["MAX_FLOW_ANGLE"] = y
    flow.to_csv("result/demo.csv", encoding='ANSI', index=False)

    angle_count = Counter(y)
    angle = []
    count = []

    for i in range(9):
        angle.append(str(i * 45))
        count.append(angle_count[i])

    return flow, angle, count, total_max_counts


def plot_2D(flow, angle, count):
    # 第一个图 输入dataframe xy 为其中的两列
    plt.figure('Flow_2D', figsize=(20, 10))
    sns.barplot(x="METRO_STATION_ID", y="TOTAL_COUNTS", data=flow, palette="hls")
    plt.xlabel("站序")
    plt.ylabel("人数")
    plt.title('地铁站点周围公交站的OD数量的统计')
    plt.savefig('地铁站点周围公交站的OD数量的统计')

    # 第二个图 输入 angle, count 构成的 zip 列表
    def pie_base() -> Pie:
        data = [list(z) for z in zip(angle, count)]
        c = (
            Pie()
                .add("", data)
                # 竖着显示label
                .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="地铁站点周围公交站的OD方向最多的统计"),
                legend_opts=opts.LegendOpts(
                    orient="vertical", pos_top="15%", pos_left="2%"))
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        )
        return c

    c = pie_base()
    webbrowser.open(c.render('地铁站点周围公交站的OD方向最多的统计.html'))


def plot_3D(flow, total_max_counts):
    def bar3d_flow():
        data = []

        for i in flow.itertuples():
            station = int(i[1])
            counts = eval(i[2])

            for direction in range(len(counts)):
                count = counts[direction]
                cell = [station, direction, count]
                data.append(cell)

        x_label = range(len(flow))
        y_label = range(8)
        x_label = [str(i) for i in x_label]
        y_label = [str(i) for i in y_label]

        c = (
            Bar3D()
                .add(
                "乘客数量",
                data,
                xaxis3d_opts=opts.Axis3DOpts(x_label, interval=0, type_="category"),
                yaxis3d_opts=opts.Axis3DOpts(y_label, interval=0, type_="category"),
                zaxis3d_opts=opts.Axis3DOpts(type_="value"),
            )
                .set_global_opts(
                visualmap_opts=opts.VisualMapOpts(max_=total_max_counts),
                title_opts=opts.TitleOpts(title="地铁线各站点8个方向的客流人数"),
            )
        )
        return c

    c = bar3d_flow()
    webbrowser.open(c.render('地铁线各站点8个方向的客流人数.html'))

    def bar3d_dist():
        data = []

        for i in flow.itertuples():
            station = int(i[1])
            counts = eval(i[3])

            for direction in range(len(counts)):
                count = counts[direction]
                cell = [station, direction, count]
                data.append(cell)

        x_label = range(len(flow))
        y_label = range(8)
        x_label = [str(i) for i in x_label]
        y_label = [str(i) for i in y_label]

        c = (
            Bar3D()
                .add(
                "平均距离",
                data,
                xaxis3d_opts=opts.Axis3DOpts(x_label, type_="category"),
                yaxis3d_opts=opts.Axis3DOpts(y_label, type_="category"),
                zaxis3d_opts=opts.Axis3DOpts(type_="value"),
            )
                .set_global_opts(
                visualmap_opts=opts.VisualMapOpts(max_=10),
                title_opts=opts.TitleOpts(title="地铁线各站点8个方向的平均距离"),
            )
        )
        return c

    c = bar3d_dist()
    webbrowser.open(c.render('地铁线各站点8个方向的平均距离.html'))


def main():
    flow, name = read()
    flow = add_statation_name(flow, name)
    flow, angle, count, total_max_counts = add_total_max(flow)
    plot_2D(flow, angle, count)
    plot_3D(flow, total_max_counts)


if __name__ == "__main__":
    main()
