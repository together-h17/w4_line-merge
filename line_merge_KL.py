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

merged_lines = []
# 找相交的所有線段
for i, line1 in enumerate(lines):
    intersections = tree.query(line1)
    for j in intersections:
        line2 = lines[j]
        # 向下查詢(避免重複)
        if j > i:
            # using 'touches' instead of 'intersects'
            if line1.intersects(line2) or line1.touches(line2):
                print("Line 1:", line1)
                print("Line 2:", line2)
                print()
                merge_it = linemerge((line1, line2))
                merged_lines.append(merge_it)
                break
        merged_lines.append(line1)




merged_gdf = gpd.GeoDataFrame(geometry=merged_lines, crs=gdf.crs)
merged_gdf.to_file("merged_lines.shp")


