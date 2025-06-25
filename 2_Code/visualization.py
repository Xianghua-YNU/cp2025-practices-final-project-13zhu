    def plot_simulations(self):
        """绘制光强分布和条纹图"""
        self.ax1.clear()
        self.ax2.clear()

        x, intensity = self.calculate_intensity()

        # 绘制光强分布图（左图）
        self.ax1.plot(x * 1e3, intensity) 
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
           
            stripe_img[:, i] = [c * intens for c in color]

        self.ax2.imshow(stripe_img, extent=[x[0] * 1e3, x[-1] * 1e3, 0, 100], aspect='auto')
        self.ax2.set_xlabel("位置 x (mm)")
        self.ax2.set_ylabel("条纹高度")
        self.ax2.set_title("干涉/衍射条纹")

        # 绘制衍射包络线（如果开启）
        if self.fit_enable and self.b > 0:
            x_mm = x * 1e3
            d = self.d * 1e-3
            b = self.b * 1e-3
            lambda_m = self.lambda_val * 1e-9
            D = self.D * 1e-3
            theta = np.arctan(x / D)
            alpha = (np.pi * b * np.sin(theta)) / lambda_m
            alpha[alpha == 0] = 1e-10
            envelope = (np.sin(alpha) / alpha) ** 2
            fit_x = np.linspace(min(x_mm), max(x_mm), 500)
            fit_func = interp1d(x_mm, envelope, kind='cubic')
            fit_envelope = fit_func(fit_x)
            self.ax1.plot(fit_x, fit_envelope, 'r--', label="衍射包络线")
            self.ax1.legend()

        self.fig.tight_layout()
        self.canvas.draw()

    def wavelength_to_rgb(self, wavelength):
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
