![地铁站点周围公交站的OD数量的统计](https://user-images.githubusercontent.com/18719360/131454246-82f11820-e33b-4156-9e3f-a80758d1350b.png)
# Metro
对地铁站点进行分析

算法：
对地铁站周围的公交站点的OD进行统计 数据来自OD反推 检测在一条公交线的OD
观察地铁修建前后的客流变化 i 幅值 ii 方向

需要注意的问题：
i 分时段进行处理 早晚高峰 平峰
ii 地铁开放一周 群众的反应程度
iii 注意OD方向的变化
iv 对比那些有地铁换乘的和无地铁换乘的地铁站 它们的变化

最后生成的表格应该是:
地铁站名 经纬度 周围公交站数量 建站前客流量 建站前方向主值取前三  建站后客流量 建站后方向主值取前三 是否有地铁换乘站

字段说明
BUS_LINE			公交线
METRO_LINE		地铁线
METRO_STATION_ID	地铁站
METRO_STATION_NAME	地铁站中文
METRO_GATE_ID		地铁口
METRO_GATE_NAME	地铁口中文
BUS_STATION_ID		公交站
BUS_STATION_NAME	公交站中文
INS_TIME			打卡时间 （上还是下）
PASS			流量
SURROUNDING_STATION	周围的公交站点 (多个）
SURROUNDING_LINE	周围的公交线路 (多个）



