import struct
import pandas as pd
import pickle
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

src_addrs = set()  # 使用集合存储不同的 srcAddr


"""
传入参数：
DataFrame中的一行

返回值：
位置信息的字典{srcAddr,x,y,z}

函数作用：
1.将DataFrame中的一行数据解析出srcAddr,x,y,z
2.将srcAddr添加到集合之中,对于src_Addrs集合赋值
"""
def getInfoPosition(row):
    # format_string = '<HHQHQHQHQHQHhhhfH?BHHfff'#侯
    format_string = '<HHQQQhhhffffH?BHH'#刘
    # header = struct.unpack(format_string, row['bin_data'][0:84])#侯
    header = struct.unpack(format_string, row['bin_data'][0:58])#刘
    # position = {
    #     'srcAddr': header[0],
    #     'x': header[21],
    #     'y': header[22],
    #     'z': header[23],
    # }#侯
    position = {
        'srcAddr': header[0],
        'x': header[10],
        'y': header[11],
        'z': header[12],
    }#刘
    src_addrs.add(header[0])  # 将 srcAddr 添加到集合中
    return position


# 示例读取 pkl 文件
# with open('data/2024-07-18-21-44-41-v2.pkl', 'rb') as file:#飞行效果还行
# with open('data/2024-07-18-21-00-18-v1.pkl', 'rb') as file:飞行效果不是很好
# with open('data/2024-07-18-22-17-41-v5.pkl', 'rb') as file:#飞行效果还行
with open('data/2024-07-17-21-42-01-v3.pkl', 'rb') as file:#飞行效果还行
    data = pickle.load(file)

# 转换为 DataFrame二维表格
data = pd.DataFrame(data)

# 提取所有位置信息
positions = data.apply(getInfoPosition, axis=1)#按行来处理数据

# 打印所有不同的 srcAddr
print("所有无人机的编号为:", src_addrs)

"""  
传入参数：
1.position:传入的DataFrame二维数组
2.srcAddr:指定的无人机编号

函数作用：
1.提取DataFrame二维数组中对应x,y,z坐标
2.为对应的x,y,z坐标,以时间为基准进行插值
3.绘制对应的图像

"""
def pltTra(positions, srcAddr):
    # 筛选特定 srcAddr 的位置数据
    filtered_positions = positions[positions.apply(lambda pos: pos['srcAddr'] == srcAddr)]
    
    # 提取 x, y, z 坐标
    x = filtered_positions.apply(lambda pos: pos['x']).values
    y = filtered_positions.apply(lambda pos: pos['y']).values
    z = filtered_positions.apply(lambda pos: pos['z']).values
    
    # 将三个行向量合并成一个矩阵 M
    M = np.column_stack((x, y, z))
    
    # 自动生成时间向量 t，这个时间向量通常用于参数化其他数据，例如在插值、绘图等操作中用作标准化的时间轴，t向量长度的点数,TODO:修改为飞行时间
    t = np.linspace(0, 20, len(x))
    
    # 设置每个点之间的插值数
    n_interp = 10
    
    # 将 x, y, z 分别进行一维插值，生成更多的点，对于时间进行插值，三维坐标对于时间都是有关系的
    t_interp = np.linspace(t[0], t[-1], len(t) * n_interp)
    x_interp = interp1d(t, x, kind='linear')(t_interp)
    y_interp = interp1d(t, y, kind='linear')(t_interp)
    z_interp = interp1d(t, z, kind='linear')(t_interp)
    
    # 将插值后的点合并成一个矩阵 M_interp
    M_interp = np.column_stack((x_interp, y_interp, z_interp))
    
    fig = plt.figure() #创建一个图对象
    ax = fig.add_subplot(111, projection='3d')#仅仅添加一个子图
    
    scatter = ax.scatter(M_interp[:, 0], M_interp[:, 1], M_interp[:, 2], c=t_interp, cmap='jet', s=6)
    #jet渐变色， 表示由蓝到绿再到红
    
    # 起始点
    ax.plot([M[0, 0]], [M[0, 1]], [M[0, 2]], 'o', markersize=8, markeredgecolor='k', markerfacecolor='b')
    
    # 终止点
    ax.plot([M[-1, 0]], [M[-1, 1]], [M[-1, 2]], 'o', markersize=8, markeredgecolor='k', markerfacecolor='r')
    
    # 显示 colorbar
    fig.colorbar(scatter, ax=ax)
    # ax=ax：指定颜色条与哪个子图（轴）关联。在这段代码中，ax 是三维子图对象。
    # scatter：散点图对象，表示颜色条与该散点图对象的颜色映射相关联。
    
    plt.show()



# 指定要绘制的 srcAddr
# set_srcAddr_to_plot = set([0,1,2,5,7])  # 替换为你要绘制的 srcAddr
srcAddr_to_plot =2
print("当前无人机编号:",srcAddr_to_plot)
if srcAddr_to_plot in src_addrs:
    print()
else:
    print(srcAddr_to_plot,"号无人机未参与飞行，出错,请更换序号") 


# 调用 pltTra 函数进行绘图
# for srcAddr_to_plot in set_srcAddr_to_plot:
pltTra(positions, srcAddr_to_plot)
