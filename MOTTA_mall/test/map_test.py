# import cartopy
# import time
# print(cartopy.config['data_dir'])
#
# import numpy as np
# import matplotlib.pyplot as plt
# import cartopy.crs as ccrs
# import cartopy.feature as cfeature
# from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
#
# plt.clf()
# fig = plt.figure(dpi=200)
#
# # set the projection to PlateCarree
# proj = ccrs.PlateCarree()
#
# ax = fig.add_subplot(1, 1, 1, projection = proj)
# ax.set_global()
#
# # set the gridlines to dashed line and the transparency to 0.7
# gl = ax.gridlines(ylocs=np.arange(-90,90+30,30),xlocs=np.arange(-180,180+60,60),draw_labels=True,linestyle='--',alpha=0.7)
# gl.xlabels_top = False
# gl.ylabels_right = False
# gl.xformatter = LONGITUDE_FORMATTER
# gl.yformatter = LATITUDE_FORMATTER
#
# # set background image to 50-natural-earth-1-downsampled.png
# ax.stock_img()
#
# ax.add_feature(cfeature.COASTLINE)
# ax.add_feature(cfeature.RIVERS)
# ax.add_feature(cfeature.LAKES)
#
# plt.savefig('./')




# ___________________________________________
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature

fig = plt.figure()

# set the projection to Orthographic
proj = ccrs.Orthographic(central_longitude=100, central_latitude=30)
ax = fig.add_subplot(1, 1, 1, projection = proj)

# set the extent to global
ax.set_global()

# set the gridlines
ax.gridlines(color='gray', linestyle = '--', xlocs = np.arange(0,360,30), ylocs = np.linspace(-80,80,9))

ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.RIVERS)
ax.add_feature(cfeature.LAKES)

#
# print("111111111111111111")
print(plt.show())
print("111111111111111111")
print(plt.savefig("./home/python/Desktop/tt.jpg"))
print("222222222222222222222")