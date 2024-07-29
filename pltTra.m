function x = pltTra(filename)
    path = readmatrix(filename);
    x = path(:,1);
    y = path(:,2);
    z = path(:,3);
    % 将三个行向量合并成一个矩阵M
    M = [x, y, z];
    
    % 自动生成时间向量t
    t = linspace(0, 1, length(x));
    
    % 将x、y、z分别进行一维插值，生成更多的点
    n_interp = 10; % 设置每个点的插值数
    x_interp = interp1(t, x, linspace(t(1), t(end), length(t)*n_interp), 'linear');
    y_interp = interp1(t, y, linspace(t(1), t(end), length(t)*n_interp), 'linear');
    z_interp = interp1(t, z, linspace(t(1), t(end), length(t)*n_interp), 'linear');
    
    % 将插值后的点合并成一个矩阵M_interp
    M_interp = ['x_interp', y_interp', z_interp'];
    
    % 生成时间向量t_interp
    t_interp = linspace(0, 1, length(x_interp));
    
    % 使用scatter3函数画出轨迹，并使用colormap函数设置渐变色
    cmap = jet(length(t_interp)); % 生成颜色矩阵
    colormap(cmap); % 设置colormap
    
    scatter3(M_interp(:,1), M_interp(:,2), M_interp(:,3), 6, t_interp, 'filled');

    
    hold on;
    plot3(M(1,1), M(1,2), M(1,3), 'o', 'MarkerSize', 8, 'MarkerEdgeColor', 'k', 'MarkerFaceColor', 'b');
    hold on;
    plot3(M(end,1), M(end,2), M_interp(end,3), 'o', 'MarkerSize', 8, 'MarkerEdgeColor', 'k', 'MarkerFaceColor', 'r');

end