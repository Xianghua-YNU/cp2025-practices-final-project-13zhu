import numpy as np
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.interpolate import interp1d
import matplotlib

matplotlib.use("TkAgg")

# 确保中文显示正常
plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题


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

    def update_params(self, event=None):
        """更新参数并重新绘图"""
        self.d = float(self.d_scale.get())
        self.lambda_val = int(self.lambda_scale.get())
        self.D = int(self.D_scale.get())
        self.b = float(self.b_scale.get())

        self.d_label.config(text=f"当前 d: {self.d:.2f} mm")
        self.lambda_label.config(text=f"当前 λ: {self.lambda_val} nm")
        self.D_label.config(text=f"当前 D: {self.D} mm")
        self.b_label.config(text=f"当前 b: {self.b:.3f} mm")

        self.plot_simulations()
        self.status_var.set(f"参数更新: d={self.d}mm, λ={self.lambda_val}nm, D={self.D}mm, b={self.b}mm")

    def toggle_fit(self):
        """切换拟合包络线显示"""
        self.fit_enable = self.fit_var.get()
        self.plot_simulations()
        self.status_var.set(f"拟合开关: {'开启' if self.fit_enable else '关闭'}")

    def calculate_intensity(self):
        """计算光强分布"""
        # 转换单位：mm→m，nm→m
        d = self.d * 1e-3
        lambda_m = self.lambda_val * 1e-9
        D = self.D * 1e-3
        b = self.b * 1e-3

        # 生成x轴坐标（单位：m），覆盖±50mm范围
        x = np.linspace(-50e-3, 50e-3, 1000)

        if b == 0:
            # 理想干涉模型
            delta = (d * x) / D  # 近似光程差
            phase = (2 * np.pi * delta) / lambda_m
            intensity = 4 * np.cos(phase / 2) ** 2
        else:
            # 衍射模型
            delta = (d * x) / D  # 干涉光程差
            phase = (2 * np.pi * delta) / lambda_m
            theta = np.arctan(x / D)  # 衍射角度
            alpha = (np.pi * b * np.sin(theta)) / lambda_m
            # 避免除零错误
            alpha[alpha == 0] = 1e-10
            diffraction_factor = (np.sin(alpha) / alpha) ** 2
            intensity = 4 * diffraction_factor * np.cos(phase / 2) ** 2

        return x, intensity

    def plot_simulations(self):
        """绘制光强分布和条纹图"""
        self.ax1.clear()
        self.ax2.clear()

        x, intensity = self.calculate_intensity()

        # 绘制光强分布图（左图）
        self.ax1.plot(x * 1e3, intensity)  # 转换回mm单位显示
        self.ax1.set_xlabel("位置 x (mm)")
        self.ax1.set_ylabel("相对光强")
        self.ax1.set_title("光强分布")
        self.ax1.grid(True)

        # 绘制条纹图（右图），使用彩色显示
        intensity_norm = intensity / np.max(intensity)
        stripe_img = np.zeros((100, len(x), 3))

        # 根据波长计算颜色
        color = self.wavelength_to_rgb(self.lambda_val)

        for i, intens in enumerate(intensity_norm):
            # 使用计算出的颜色，根据强度调整亮度
            stripe_img[:, i] = [c * intens for c in color]

        self.ax2.imshow(stripe_img, extent=[x[0] * 1e3, x[-1] * 1e3, 0, 100], aspect='auto')
        self.ax2.set_xlabel("位置 x (mm)")
        self.ax2.set_ylabel("条纹高度")
        self.ax2.set_title("干涉/衍射条纹")

        # 绘制衍射包络线（如果开启）
        if self.fit_enable and self.b > 0:
            x_mm = x * 1e3
            # 提取包络线（单缝衍射因子）
            d = self.d * 1e-3
            b = self.b * 1e-3
            lambda_m = self.lambda_val * 1e-9
            D = self.D * 1e-3
            theta = np.arctan(x / D)
            alpha = (np.pi * b * np.sin(theta)) / lambda_m
            alpha[alpha == 0] = 1e-10
            envelope = (np.sin(alpha) / alpha) ** 2
            # 插值拟合包络线
            fit_x = np.linspace(min(x_mm), max(x_mm), 500)
            fit_func = interp1d(x_mm, envelope, kind='cubic')
            fit_envelope = fit_func(fit_x)
            self.ax1.plot(fit_x, fit_envelope, 'r--', label="衍射包络线")
            self.ax1.legend()

        self.fig.tight_layout()
        self.canvas.draw()

    def wavelength_to_rgb(self, wavelength):
        """将波长转换为RGB颜色"""
        wavelength = float(wavelength)
        if wavelength >= 380 and wavelength <= 440:
            attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
            r = ((-(wavelength - 440) / (440 - 380)) * attenuation)
            g = 0.0
            b = (1.0 * attenuation)
        elif wavelength >= 440 and wavelength <= 490:
            r = 0.0
            g = ((wavelength - 440) / (490 - 440))
            b = 1.0
        elif wavelength >= 490 and wavelength <= 510:
            r = 0.0
            g = 1.0
            b = (-(wavelength - 510) / (510 - 490))
        elif wavelength >= 510 and wavelength <= 580:
            r = ((wavelength - 510) / (580 - 510))
            g = 1.0
            b = 0.0
        elif wavelength >= 580 and wavelength <= 645:
            r = 1.0
            g = (-(wavelength - 645) / (645 - 580))
            b = 0.0
        elif wavelength >= 645 and wavelength <= 780:
            attenuation = 0.3 + 0.7 * (780 - wavelength) / (780 - 645)
            r = (1.0 * attenuation)
            g = 0.0
            b = 0.0
        else:
            r = 0.0
            g = 0.0
            b = 0.0
        return (r, g, b)

    def save_image(self):
        """保存当前图像"""
        try:
            self.fig.savefig(f"双缝干涉衍射仿真_d{self.d}_lambda{self.lambda_val}.png")
            self.status_var.set("图像保存成功")
        except Exception as e:
            self.status_var.set(f"保存失败: {str(e)}")

    def reset_view(self):
        """重置视图"""
        self.ax1.set_xlim(-50, 50)
        self.ax1.set_ylim(0, 1.1)
        self.ax2.set_xlim(-50, 50)
        self.canvas.draw()

    def reset_params(self):
        """重置所有参数到初始值"""
        self.d = 0.4
        self.lambda_val = 590
        self.D = 2000
        self.b = 0.05
        self.fit_enable = False

        self.d_scale.set(self.d)
        self.lambda_scale.set(self.lambda_val)
        self.D_scale.set(self.D)
        self.b_scale.set(self.b)
        self.fit_var.set(self.fit_enable)

        self.update_params()
        self.status_var.set("参数已重置为默认值")


if __name__ == "__main__":
    root = tk.Tk()
    app = DoubleSlitSimulation(root)
    root.mainloop()
