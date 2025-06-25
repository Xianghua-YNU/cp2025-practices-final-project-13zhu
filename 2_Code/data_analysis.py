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
            delta = (d * x) / D 
            phase = (2 * np.pi * delta) / lambda_m
            intensity = 4 * np.cos(phase / 2) ** 2
        else:
            # 衍射模型
            delta = (d * x) / D  
            phase = (2 * np.pi * delta) / lambda_m
            theta = np.arctan(x / D)
            alpha = (np.pi * b * np.sin(theta)) / lambda_m
            # 避免除零错误
            alpha[alpha == 0] = 1e-10
            diffraction_factor = (np.sin(alpha) / alpha) ** 2
            intensity = 4 * diffraction_factor * np.cos(phase / 2) ** 2

        return x, intensity
