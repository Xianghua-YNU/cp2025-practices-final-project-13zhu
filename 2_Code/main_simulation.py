class DoubleSlitSimulation:
    def __init__(self, root):
        self.root = root
        self.root.title("杨氏双缝干涉和衍射仿真模拟")
        self.root.geometry("1200x800")

        # 初始化参数
        self.d = 0.4  # 双缝间距(mm)
        self.lambda_val = 590  # 波长(nm)
        self.D = 2000  # 缝到屏幕距离(mm)
        self.b = 0.05  # 缝宽(mm) 初始值设为0.05mm，避免初始状态为纯干涉
        self.fit_enable = False  # 拟合开关状态

        # 创建界面
        self.create_interface()
        # 初始绘图
        self.plot_simulations()
