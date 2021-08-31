import numpy as np
import pandas as pd
import time as clock
from math import radians, cos, sin, asin, sqrt, atan2, degrees

"""
I 得到地铁经纬度 关注5,14号
II 查看周围150m的公交站
III 查看该站点的下行方向的所有OD 计算他们的距离和角度
IV 对比修建之前的虚拟站点范围OD
"""

# 定义变量
TIME_PERIOD = "morning"
START_DATE = 20191002
END_DATA = 20191008
REQUEST_LINE = 5

pd.set_option("display.max_columns", None)
np.set_printoptions(suppress=True)  # 解决numpy用科学计数法表达问题


def geodistance(lng1, lat1, lng2, lat2):
    """ return km """
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
    dlon = lng2 - lng1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    distance = 2 * asin(sqrt(a)) * 6371
    distance = round(distance, 1)  # 单位是km
    return distance


def geoangle(lng1, lat1, lng2, lat2):
    """ return [0,360] """
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
    dlng = lng2 - lng1
    y = sin(dlng) * cos(lat2)
    x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dlng)
    angle = degrees(atan2(y, x))
    angle = (angle + 180) % 360  # 单位是度
    return angle


vector_geodistance = np.vectorize(geodistance)
vector_geoangle = np.vectorize(geoangle)


def read():
    """ read """
    metro = pd.read_csv("data/metro_5.csv", encoding="ANSI")
    bus_od = pd.read_csv("data/bus_od.csv", encoding="ANSI")
    station_coordinates = pd.read_csv("data/station_coordinates.csv", encoding="ANSI")
    return metro, bus_od, station_coordinates


def filtering(metro, bus_od, TIME_PERIOD, START_DATE, END_DATA):
    """ filtering bus_od table
        based on date, time and these stations
        time flag: morning evening others
        start data：int
        end data: int """

    # 删选满足3个条件的
    if TIME_PERIOD == "morning":
        time_set = {7, 8, 9}

    elif TIME_PERIOD == "evening":
        time_set = {17, 18, 19}

    else:
        time_set = set(range(24))
        time_set = time_set - {7, 8, 9} - {17, 18, 19}

    time_set = list(time_set)
    station_set = list(metro["BUS_STATION_ID"])

    bus_od = bus_od[bus_od["ALLOT_TIME"] >= START_DATE]
    bus_od = bus_od[bus_od["ALLOT_TIME"] <= END_DATA]
    bus_od = bus_od[bus_od["HOUR"].isin(time_set)]
    bus_od = bus_od[bus_od["STATION_ID_O"].isin(station_set)]

    bus_od.to_csv("data/bus_od_filtered.csv", encoding="ANSI", header=True, index=False)
    return bus_od


def calculate(metro, bus_od, station_coordinates, time, start, end):
    """ calculate flow, dist, angle """
    """ 查表顺序metro--> bus_od--> station_coordinates """
    res = []

    # 地铁站
    for i in metro.groupby("METRO_STATION_ID"):  # 对LINE_NO 进行归类
        metro_station_id = i[0]
        j = i[1]["BUS_STATION_ID"]

        # 在这一步初始化 每个站点清零
        flow = [0] * 8
        dist = [0] * 8

        # 地铁口 多个点的OD
        for station in j:

            if station > 10000000:  # 排除地铁换乘点
                pass

            else:
                station1 = station
                # 一个出发点对应多个目标点 1个点的OD
                station1_to_station2_df = bus_od[bus_od["STATION_ID_O"].isin([station1])]

                for row in station1_to_station2_df.itertuples():
                    station2 = row[7]
                    passenger = row[9]

                    lng1 = station_coordinates[station_coordinates["STATION_ID"].isin([station1])]["LNG"]
                    lat1 = station_coordinates[station_coordinates["STATION_ID"].isin([station1])]["LAT"]
                    lng2 = station_coordinates[station_coordinates["STATION_ID"].isin([station2])]["LNG"]
                    lat2 = station_coordinates[station_coordinates["STATION_ID"].isin([station2])]["LAT"]

                    lng1, lat1, lng2, lat2 = map(float, [lng1, lat1, lng2, lat2])
                    od_dist = vector_geodistance(lng1, lat1, lng2, lat2)
                    od_angle = vector_geoangle(lng1, lat1, lng2, lat2)

                    bin = int(od_angle // 45)  # angle = [0] * 8  # [(0,45),...,(315,360)] 分为8个bins

                    flow[bin] += passenger
                    dist[bin] += od_dist * passenger

                flow = np.array(flow, dtype=float)
                dist = np.array(dist, dtype=float)
                dist = np.divide(dist, flow, out=np.zeros_like(dist), where=flow != 0)
                flow = [int(i) for i in flow]
                dist = np.around(dist, 3)

                flow = list(flow)
                dist = list(dist)
        res.append([metro_station_id, flow, dist])

    res = pd.DataFrame(res)
    res.columns = ["METRO_STATION_ID", "COUNTS", "MEAN_DIST"]
    res.to_csv(f'result/metro-{REQUEST_LINE}-{start}-{end}-{time}.csv', encoding="ANSI", header=True, index=False)


def main(TIME_PERIOD, START_DATE, END_DATA):
    t1 = clock.time()
    metro, bus_od, station_coordinates = read()
    bus_od = filtering(metro, bus_od, TIME_PERIOD, START_DATE, END_DATA)
    calculate(metro, bus_od, station_coordinates, TIME_PERIOD, START_DATE, END_DATA)
    t2 = clock.time()
    print(t2 - t1)


if __name__ == "__main__":
    main(TIME_PERIOD, START_DATE, END_DATA)
