# -*- coding: utf-8 -*-
"""
Created on Thu May 23 08:44:02 2024

@author: AC927
"""

import geopandas as gpd
from shapely.strtree import STRtree
from shapely.geometry import LineString, Point
from shapely.ops import linemerge
import matplotlib.pyplot as plt

def search(line, searched_lines_id, searched_lines):
    queried_lines = [rivers[idx] for idx in tree.query(line.buffer(0.1))]
    for queried_line in queried_lines:
        if queried_line.intersects(line.buffer(0.1)) and id(queried_line) not in searched_lines_id:
            searched_lines_id.append(id(queried_line))
            searched_lines.append(queried_line)
            searched_lines_id = search(queried_line, searched_lines_id, searched_lines)
    
    return searched_lines_id
    

# 讀取河流的 shapefile
gdf = gpd.read_file(r'D:\河道密合檢查\溝渠小區.shp', encoding='utf-8')

# 提取河流線段幾何
rivers = gdf.geometry

# 取出所有河流的起點和終點坐標
points = set()
for river in rivers:
    points.add(Point(river.coords[0]))
    points.add(Point(river.coords[-1]))
    
# 建立空間索引
tree = STRtree(rivers)

####
output_dict = dict()
count = 0

for index, row in gdf.iterrows():
    searched_lines_id = [id(row['geometry'])]
    searched_lines = []
    searched_lines.append(row['geometry'])
    searched_lines_id = search(row['geometry'], searched_lines_id, searched_lines)
    
    merged_line = linemerge(searched_lines)
    new_row = row.copy()
    new_row['geometry'] = merged_line
    output_dict[count] = new_row
    count += 1

output = gpd.GeoDataFrame.from_dict(output_dict, orient = 'index')
output.to_file(r'D:\河道密合檢查\溝渠小區_merged.shp', encoding = 'utf-8')

####
# =============================================================================
# 
# # 用來存儲合併後的線段
# merged_lines = []
# check = []
# 
# for point in points:
#     
#     if point in check:
#         continue
#     check.append(point)
#     query_geom = point.buffer(0.1)  # 緩衝區 
#     intersect = [rivers[idx] for idx in tree.query(query_geom)]
#     
#     if len(intersect) < 2:
#         continue
#     elif len(intersect) >= 2:
#         merged_line_1 = linemerge(intersect) 
#         # merged_lines.append(merged_line_1)
#         
#         merge_points = []
#         merge_points.append(Point(merged_line_1.coords[0]))
#         merge_points.append(Point(merged_line_1.coords[-1]))
#         
#         for a in merge_points:
#             if a in check:
#                 continue
#             check.append(a)
#             query_geom1 = a.buffer(0.1)
#             intersect1 = [rivers[idx] for idx in tree.query(query_geom1)]
#             if len(intersect1) < 2:
#                 continue
#             elif len(intersect1) >= 2:
#                   for line in intersect1:
#                       if line not in intersect:
#                           merged_line_2 = linemerge([merged_line_1, line])
#             merged_lines.append(merged_line_2)
#                          
#                          
#                          
#                          
# fig, ax = plt.subplots()
# ax.set_aspect('equal', 'datalim') 
# result = merged_line_2
# ax.plot(*result.xy, color='green', linewidth = 2)
# plt.show()
# =============================================================================
