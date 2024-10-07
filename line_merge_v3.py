# -*- coding: utf-8 -*-
"""
Created on Sat May 18 23:12:35 2024

@author: vicky
"""

import geopandas as gpd
from shapely.strtree import STRtree
from shapely.ops import linemerge

# 讀取 shapefile
gdf = gpd.read_file(r"C:\Users\vicky\Desktop\python project\w3_vector\arcgis project\line_try.shp")

lines = []
# 從 GeoDataFrame 中找linestring
for geom in gdf.geometry:
    if geom.geom_type == 'LineString':
        lines.append(geom)
    elif geom.geom_type == 'MultiLineString':
        lines.extend(geom)

# 創建 STR 樹
tree = STRtree(lines)

# 存儲所有要合併的線段
groups = []

# 標記跑過的線段
chk = [False] * len(lines)

for i, line1 in enumerate(lines):
    if chk[i]:
        continue
    group = [line1]
    chk[i] = True
    queue = [line1]
    
    while queue:
        current_line = queue.pop(0)
        intersections = tree.query(current_line)
        for j in intersections:
            line2 = lines[j]
            if not chk[j] and (current_line.touches(line2) or current_line.intersects(line2)):
                group.append(line2)
                chk[j] = True
                queue.append(line2)
    
    groups.append(group)

# 合併線段
merged_lines = []
for group in groups:
    merged_line = linemerge(group)
    merged_lines.append(merged_line)

# 創GeoDataFrame存到新的shp
merged_gdf = gpd.GeoDataFrame(geometry=merged_lines, crs=gdf.crs)
merged_gdf.to_file("merged_lines.shp")
