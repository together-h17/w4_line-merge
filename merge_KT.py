# -*- coding: utf-8 -*-
"""
Created on Fri May 17 14:03:35 2024

@author: AC927
"""

import geopandas as gpd
from shapely.strtree import STRtree
from shapely.ops import linemerge
import matplotlib.pyplot as plt
from shapely.geometry import LineString
# 讀取 shapefile 檔案
rivers = gpd.read_file(r'D:\河道密合檢查\溝渠_小區.shp', encoding='utf-8')

# 獲取幾何列
river = rivers.geometry

# 設置座標參考系
river = river.set_crs(epsg=3826)

# 創建 STRtree 空間索引
tree = STRtree(river)


# 設置查詢的幾何對象
query_geom = river.iloc[0]

# 查詢接近的幾何對象
result = [river.iloc[idx] for idx in tree.query(query_geom)]

all_coords = []

for geom in result:
    all_coords.extend(list(geom.coords))

unique_coords = list(set(all_coords))

# 創建 LineString
merged_line = LineString(unique_coords)

# 將 LineString 轉換為 GeoDataFrame
line_gdf = gpd.GeoDataFrame(geometry=[merged_line], crs="EPSG:3826")

# 顯示結果
print(line_gdf)

# 繪製 LineString
fig, ax = plt.subplots()
line_gdf.plot(ax=ax, color='blue', linewidth=2)
plt.show()
# merged_line = LineString(all_coords)

# # 將 LineString 轉換為 GeoDataFrame
# line_gdf = gpd.GeoDataFrame(geometry=[merged_line], crs="EPSG:3826")

# # 顯示結果
# print(line_gdf)

# # 繪製 LineString
# fig, ax = plt.subplots()
# line_gdf.plot(ax=ax, color='blue', linewidth=2)
# plt.show()
# # 去除無效的幾何對象
# # valid_result = [geom for geom in result if geom.is_valid]

# # 將有效的幾何對象進行合併
# # merged_line = linemerge(valid_result)




