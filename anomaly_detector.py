import pandas as pd
import numpy as np
from scipy import stats

class AnomalyDetector:
    """Elektrik tüketiminde anomali tespit sınıfı"""
    
    def __init__(self, method='iqr', sensitivity=1.5):
        """
        method: 'iqr', 'zscore', 'isolation_forest'
        sensitivity: Hassasiyet seviyesi (düşük = daha hassas)
        """
        self.method = method
        self.sensitivity = sensitivity
    
    def detect_iqr_anomalies(self, data):
        """IQR (Interquartile Range) yöntemi ile anomali tespiti"""
        
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - self.sensitivity * IQR
        upper_bound = Q3 + self.sensitivity * IQR
        
        anomalies = (data < lower_bound) | (data > upper_bound)
        
        return anomalies
    
    def detect_zscore_anomalies(self, data, threshold=3):
        """Z-Score yöntemi ile anomali tespiti"""
        
        z_scores = np.abs(stats.zscore(data))
        anomalies = z_scores > (threshold / self.sensitivity)
        
        return anomalies
    
    def detect_rolling_anomalies(self, data, window=24):
        """Hareketli ortalama bazlı anomali tespiti"""
        
        if len(data) < window:
            window = max(3, len(data) // 2)
        
        rolling_mean = data.rolling(window=window, center=True).mean()
        rolling_std = data.rolling(window=window, center=True).std()
        
        # NaN değerleri doldur
        rolling_mean = rolling_mean.fillna(data.mean())
        rolling_std = rolling_std.fillna(data.std())
        
        upper_bound = rolling_mean + (self.sensitivity * rolling_std)
        lower_bound = rolling_mean - (self.sensitivity * rolling_std)
        
        anomalies = (data > upper_bound) | (data < lower_bound)
        
        return anomalies
    
    def detect_anomalies(self, df, column='consumption_kwh'):
        """Ana anomali tespit fonksiyonu"""
        
        data = df[column].copy()
        
        if self.method == 'iqr':
            anomalies = self.detect_iqr_anomalies(data)
        elif self.method == 'zscore':
            anomalies = self.detect_zscore_anomalies(data)
        elif self.method == 'rolling':
            anomalies = self.detect_rolling_anomalies(data)
        else:
            # Varsayılan: IQR
            anomalies = self.detect_iqr_anomalies(data)
        
        return anomalies
    
    def get_anomaly_statistics(self, df, anomaly_column='anomaly'):
        """Anomali istatistikleri"""
        
        total_points = len(df)
        anomaly_count = df[anomaly_column].sum()
        anomaly_rate = (anomaly_count / total_points) * 100
        
        if anomaly_count > 0:
            avg_anomaly_consumption = df[df[anomaly_column]]['consumption_kwh'].mean()
            avg_normal_consumption = df[~df[anomaly_column]]['consumption_kwh'].mean()
            anomaly_impact = ((avg_anomaly_consumption - avg_normal_consumption) / avg_normal_consumption) * 100
        else:
            avg_anomaly_consumption = 0
            avg_normal_consumption = df['consumption_kwh'].mean()
            anomaly_impact = 0
        
        stats_dict = {
            'toplam_veri_noktasi': total_points,
            'anomali_sayisi': int(anomaly_count),
            'anomali_orani': round(anomaly_rate, 2),
            'ortalama_anomali_tuketim': round(avg_anomaly_consumption, 2),
            'ortalama_normal_tuketim': round(avg_normal_consumption, 2),
            'anomali_etkisi_yuzde': round(anomaly_impact, 2)
        }
        
        return stats_dict
