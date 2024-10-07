# -*- coding: utf-8 -*-
"""
Created on Sat May 18 21:25:59 2024

@author: vicky
"""

import geopandas as gpd
from shapely.strtree import STRtree
from shapely.ops import linemerge

# 讀取 shapefile
gdf = gpd.read_file(r"C:\Users\vicky\Desktop\python project\w3_vector\arcgis project\line_try.shp")

lines = []
# 從 GeoDataFrame 中提取線段並存儲到列表中
for geom in gdf.geometry:
    if geom.geom_type == 'LineString':
        lines.append(geom)
    elif geom.geom_type == 'MultiLineString':
        lines.extend(geom)

# 創建 STR 樹
tree = STRtree(lines)

# 查詢所有相鄰的線段組合(不管怎樣就是要用遞迴就對了)
def find_intersection_lines(line, tree, lines, visited):
    intersecting_lines = [line]
    stack = [line]
    while stack:
        current_line = stack.pop()
        intersections = tree.query(current_line)
        for j in intersections:
            if j in visited:
                continue
            candidate_line = lines[j]
            if current_line.touches(candidate_line) or current_line.intersects(candidate_line):
                intersecting_lines.append(candidate_line)
                stack.append(candidate_line)
                visited.add(j)
    return intersecting_lines


visited = set() #檢查重複
merged_lines = []
for i, line in enumerate(lines):
    if i in visited:
        continue
    intersecting_lines = find_intersection_lines(line, tree, lines, visited)
    if len(intersecting_lines) > 1:
        merged_line = linemerge(intersecting_lines)
        merged_lines.append(merged_line)
    else:
        merged_lines.append(line)

# 創建 GeoDataFrame 並保存到新的 shapefile
merged_gdf = gpd.GeoDataFrame(geometry=merged_lines, crs=gdf.crs)
merged_gdf.to_file("merged_lines.shp")
