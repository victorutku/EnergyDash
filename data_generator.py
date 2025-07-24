import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class ElectricityDataGenerator:
    """Gerçekçi elektrik tüketim verisi üretici sınıfı"""
    
    def __init__(self):
        self.base_consumption = 2.5  # Temel tüketim (kWh)
        self.price_per_kwh = 2.85    # TL/kWh (2025 Türkiye ortalaması)
        
    def generate_hourly_data(self, start_date, hours=24):
        """Saatlik elektrik tüketim verisi üret"""
        
        timestamps = []
        consumption_data = []
        
        current_time = start_date
        
        for hour in range(hours):
            timestamps.append(current_time)
            
            # Saatlik tüketim paterni (gerçekçi ev tüketimi)
            hour_of_day = current_time.hour
            
            # Temel saatlik çarpanlar
            if 6 <= hour_of_day <= 8:  # Sabah yoğunluğu
                multiplier = 1.8
            elif 12 <= hour_of_day <= 14:  # Öğle yoğunluğu
                multiplier = 1.5
            elif 18 <= hour_of_day <= 22:  # Akşam yoğunluğu
                multiplier = 2.2
            elif 23 <= hour_of_day or hour_of_day <= 5:  # Gece düşük tüketim
                multiplier = 0.6
            else:  # Normal saatler
                multiplier = 1.0
            
            # Rastgele varyasyon ekle
            variation = np.random.normal(1.0, 0.15)
            
            # Haftasonu etkisi
            if current_time.weekday() >= 5:  # Cumartesi/Pazar
                multiplier *= 1.2
            
            consumption = self.base_consumption * multiplier * variation
            
            # Negatif değerleri önle
            consumption = max(0.1, consumption)
            
            consumption_data.append(consumption)
            current_time += timedelta(hours=1)
        
        # DataFrame oluştur
        df = pd.DataFrame({
            'datetime': timestamps,
            'consumption_kwh': consumption_data
        })
        
        # Maliyet hesapla
        df['cost_TL'] = df['consumption_kwh'] * self.price_per_kwh
        
        return df
    
    def generate_daily_data(self, days=30):
        """Günlük elektrik tüketim verisi üret"""
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        timestamps = []
        consumption_data = []
        
        current_date = start_date
        
        for day in range(days + 1):
            timestamps.append(current_date)
            
            # Günlük tüketim (24 saatlik toplam)
            daily_base = 35  # Günlük ortalama kWh
            
            # Mevsimsel etki
            month = current_date.month
            if month in [12, 1, 2]:  # Kış
                seasonal_multiplier = 1.4  # Isıtma
            elif month in [6, 7, 8]:  # Yaz
                seasonal_multiplier = 1.2  # Klima
            else:  # İlkbahar/Sonbahar
                seasonal_multiplier = 0.9
            
            # Haftasonu etkisi
            if current_date.weekday() >= 5:
                weekend_multiplier = 1.15
            else:
                weekend_multiplier = 1.0
            
            # Rastgele varyasyon
            variation = np.random.normal(1.0, 0.1)
            
            daily_consumption = daily_base * seasonal_multiplier * weekend_multiplier * variation
            daily_consumption = max(15, daily_consumption)  # Minimum tüketim
            
            consumption_data.append(daily_consumption)
            current_date += timedelta(days=1)
        
        df = pd.DataFrame({
            'datetime': timestamps,
            'consumption_kwh': consumption_data
        })
        
        df['cost_TL'] = df['consumption_kwh'] * self.price_per_kwh
        
        return df
    
    def add_anomalies(self, df, anomaly_rate=0.05):
        """Veri setine anomaliler ekle"""
        
        df = df.copy()
        df['anomaly'] = False
        
        n_anomalies = int(len(df) * anomaly_rate)
        
        if n_anomalies > 0:
            # Rastgele anomali indeksleri seç
            anomaly_indices = np.random.choice(df.index, n_anomalies, replace=False)
            
            for idx in anomaly_indices:
                # Anomali türü: yüksek tüketim (2-4x normal)
                anomaly_multiplier = np.random.uniform(2.5, 4.0)
                df.loc[idx, 'consumption_kwh'] *= anomaly_multiplier
                df.loc[idx, 'cost_TL'] = df.loc[idx, 'consumption_kwh'] * self.price_per_kwh
                df.loc[idx, 'anomaly'] = True
        
        return df
