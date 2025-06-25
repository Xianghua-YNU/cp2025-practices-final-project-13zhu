    def create_interface(self):
        # 左侧参数控制框架
        param_frame = ttk.LabelFrame(self.root, text="实验参数调节")
        param_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # 双缝间距滑块
        ttk.Label(param_frame, text="双缝间距 d (0.2~1 mm):").pack(anchor=tk.W, pady=5)
        self.d_scale = ttk.Scale(param_frame, from_=0.2, to=1.0, orient=tk.HORIZONTAL,
                                 length=300, command=self.update_params)
        self.d_scale.set(self.d)
        self.d_scale.pack(pady=5)
        self.d_label = ttk.Label(param_frame, text=f"当前 d: {self.d} mm")
        self.d_label.pack(anchor=tk.W)

        # 波长滑块 - 添加颜色提示
        ttk.Label(param_frame, text="入射光波长 λ (400~700 nm):").pack(anchor=tk.W, pady=5)
        self.lambda_scale = ttk.Scale(param_frame, from_=400, to=700, orient=tk.HORIZONTAL,
                                      length=300, command=self.update_params)
        self.lambda_scale.set(self.lambda_val)
        self.lambda_scale.pack(pady=5)
        self.lambda_label = ttk.Label(param_frame, text=f"当前 λ: {self.lambda_val} nm")
        self.lambda_label.pack(anchor=tk.W)

        # 屏幕距离滑块
        ttk.Label(param_frame, text="缝到屏幕距离 D (500~2000 mm):").pack(anchor=tk.W, pady=5)
        self.D_scale = ttk.Scale(param_frame, from_=500, to=2000, orient=tk.HORIZONTAL,
                                 length=300, command=self.update_params)
        self.D_scale.set(self.D)
        self.D_scale.pack(pady=5)
        self.D_label = ttk.Label(param_frame, text=f"当前 D: {self.D} mm")
        self.D_label.pack(anchor=tk.W)

        # 缝宽滑块
        ttk.Label(param_frame, text="缝宽 b (0~0.1 mm):").pack(anchor=tk.W, pady=5)
        self.b_scale = ttk.Scale(param_frame, from_=0.0, to=0.1, orient=tk.HORIZONTAL,
                                 length=300, command=self.update_params)
        self.b_scale.set(self.b)
        self.b_scale.pack(pady=5)
        self.b_label = ttk.Label(param_frame, text=f"当前 b: {self.b} mm")
        self.b_label.pack(anchor=tk.W)

        # 拟合开关
        self.fit_var = tk.BooleanVar(value=self.fit_enable)
        fit_check = ttk.Checkbutton(param_frame, text="显示衍射包络线",
                                    variable=self.fit_var, command=self.toggle_fit)
        fit_check.pack(pady=10, anchor=tk.W)

        # 右侧图像显示框架
        plot_frame = ttk.Frame(self.root)
        plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 创建Matplotlib图像
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # 添加交互按钮
        btn_frame = ttk.Frame(plot_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        ttk.Button(btn_frame, text="保存图像", command=self.save_image).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="重置视图", command=self.reset_view).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="重置参数", command=self.reset_params).pack(side=tk.LEFT, padx=5)

        # 状态显示
        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
