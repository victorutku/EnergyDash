import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import matplotlib.dates as mdates
from data_generator import ElectricityDataGenerator
from anomaly_detector import AnomalyDetector

# Sayfa yapılandırması
st.set_page_config(
    page_title="Ev Elektrik Tüketimi Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Matplotlib Türkçe karakter sorunu için
plt.rcParams['font.family'] = ['DejaVu Sans']

def load_or_generate_data(data_type, period):
    """Veri yükle veya üret"""
    
    generator = ElectricityDataGenerator()
    
    if data_type == "Saatlik":
        # Son 24-168 saat arası veri
        hours = min(168, max(24, period))
        start_date = datetime.now() - timedelta(hours=hours)
        df = generator.generate_hourly_data(start_date, hours)
    else:
        # Günlük veri
        days = min(365, max(7, period))
        df = generator.generate_daily_data(days)
    
    # Anomali ekle
    df = generator.add_anomalies(df, anomaly_rate=0.08)
    
    return df

def create_consumption_chart(df, show_anomalies=True):
    """Tüketim grafiği oluştur"""
    
    fig, ax1 = plt.subplots(figsize=(14, 6))
    
    # Ana tüketim grafiği
    ax1.plot(df.index, df['consumption_kwh'], 
             label='Tüketim (kWh)', color='#1f77b4', linewidth=2)
    
    # Anomalileri vurgula
    if show_anomalies and 'anomaly' in df.columns:
        anomaly_data = df[df['anomaly']]
        if not anomaly_data.empty:
            ax1.scatter(anomaly_data.index, anomaly_data['consumption_kwh'], 
                       color='red', s=50, label='Anomali', zorder=5, alpha=0.8)
    
    ax1.set_xlabel('Tarih/Saat')
    ax1.set_ylabel('Tüketim (kWh)', color='#1f77b4')
    ax1.tick_params(axis='y', labelcolor='#1f77b4')
    ax1.grid(True, alpha=0.3)
    
    # İkinci y ekseni - Maliyet
    ax2 = ax1.twinx()
    ax2.plot(df.index, df['cost_TL'], 
             color='#ff7f0e', alpha=0.7, linewidth=2, label='Maliyet (TL)')
    ax2.set_ylabel('Maliyet (TL)', color='#ff7f0e')
    ax2.tick_params(axis='y', labelcolor='#ff7f0e')
    
    # Tarih formatı
    if len(df) > 7:
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
        ax1.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, len(df)//10)))
    else:
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m %H:%M'))
        ax1.xaxis.set_major_locator(mdates.HourLocator(interval=max(1, len(df)//10)))
    
    plt.xticks(rotation=45)
    
    # Legendler
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    plt.title('Elektrik Tüketimi ve Maliyeti', fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    
    return fig

def create_pattern_analysis(df):
    """Tüketim paterni analizi"""
    
    if 'datetime' not in df.columns:
        df_copy = df.copy()
        df_copy['datetime'] = df_copy.index
    else:
        df_copy = df.copy()
    
    # Saatlik analiz
    if len(df_copy) > 24:
        df_copy['hour'] = df_copy['datetime'].dt.hour
        hourly_avg = df_copy.groupby('hour')['consumption_kwh'].mean()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        
        # Saatlik ortalama
        ax1.bar(hourly_avg.index, hourly_avg.values, color='skyblue', alpha=0.7)
        ax1.set_title('Saatlik Ortalama Tüketim')
        ax1.set_xlabel('Saat')
        ax1.set_ylabel('Ortalama Tüketim (kWh)')
        ax1.grid(True, alpha=0.3)
        
        # Haftalık analiz (eğer yeterli veri varsa)
        if len(df_copy) > 7:
            df_copy['weekday'] = df_copy['datetime'].dt.day_name()
            weekday_avg = df_copy.groupby('weekday')['consumption_kwh'].mean()
            
            # Haftanın günlerini sırala
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            weekday_avg = weekday_avg.reindex([day for day in day_order if day in weekday_avg.index])
            
            ax2.bar(range(len(weekday_avg)), weekday_avg.values, color='lightcoral', alpha=0.7)
            ax2.set_title('Haftalık Ortalama Tüketim')
            ax2.set_xlabel('Gün')
            ax2.set_ylabel('Ortalama Tüketim (kWh)')
            ax2.set_xticks(range(len(weekday_avg)))
            ax2.set_xticklabels([day[:3] for day in weekday_avg.index], rotation=45)
            ax2.grid(True, alpha=0.3)
        else:
            ax2.text(0.5, 0.5, 'Haftalık analiz için\nyeterli veri yok', 
                    transform=ax2.transAxes, ha='center', va='center', fontsize=12)
            ax2.set_title('Haftalık Analiz')
        
        plt.tight_layout()
        return fig
    
    return None

def main():
    """Ana uygulama"""
    
    # Başlık
    st.title("⚡ Ev Elektrik Tüketimi Dashboard")
    st.markdown("---")
    
    # Sidebar kontrolleri
    st.sidebar.header("📊 Analiz Ayarları")
    
    # Veri tipi seçimi
    data_type = st.sidebar.selectbox(
        "Veri Tipi:",
        ["Saatlik", "Günlük"]
    )
    
    # Zaman aralığı
    if data_type == "Saatlik":
        period = st.sidebar.slider("Saat Sayısı:", 24, 168, 48)
        period_text = f"Son {period} saat"
    else:
        period = st.sidebar.slider("Gün Sayısı:", 7, 365, 30)
        period_text = f"Son {period} gün"
    
    # Anomali tespit ayarları
    st.sidebar.subheader("🔍 Anomali Tespiti")
    anomaly_method = st.sidebar.selectbox(
        "Yöntem:",
        ["iqr", "zscore", "rolling"],
        format_func=lambda x: {
            "iqr": "IQR (Çeyrekler Arası)",
            "zscore": "Z-Score",
            "rolling": "Hareketli Ortalama"
        }[x]
    )
    
    sensitivity = st.sidebar.slider("Hassasiyet:", 0.5, 3.0, 1.5, 0.1)
    show_anomalies = st.sidebar.checkbox("Anomalileri Göster", True)
    
    # Veri yükle
    with st.spinner('Veri yükleniyor...'):
        df = load_or_generate_data(data_type, period)
        df.set_index('datetime', inplace=True)
    
    # Anomali tespiti
    detector = AnomalyDetector(method=anomaly_method, sensitivity=sensitivity)
    detected_anomalies = detector.detect_anomalies(df)
    df['detected_anomaly'] = detected_anomalies
    
    # Ana metrikler
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_consumption = df['consumption_kwh'].sum()
        st.metric(
            f"Toplam Tüketim ({period_text})", 
            f"{total_consumption:.2f} kWh"
        )
    
    with col2:
        total_cost = df['cost_TL'].sum()
        st.metric(
            f"Toplam Maliyet ({period_text})", 
            f"{total_cost:.2f} TL"
        )
    
    with col3:
        if 'anomaly' in df.columns:
            actual_anomalies = int(df['anomaly'].sum())
        else:
            actual_anomalies = 0
        st.metric(
            "Gerçek Anomali Sayısı", 
            actual_anomalies
        )
    
    with col4:
        detected_anomaly_count = int(df['detected_anomaly'].sum())
        st.metric(
            "Tespit Edilen Anomali", 
            detected_anomaly_count
        )
    
    # Ana grafik
    st.subheader("📈 Tüketim Trendi")
    
    # Anomali gösterme seçeneği
    if show_anomalies:
        display_df = df.copy()
        display_df['anomaly'] = df['detected_anomaly']
    else:
        display_df = df.copy()
        display_df['anomaly'] = False
    
    fig = create_consumption_chart(display_df, show_anomalies)
    st.pyplot(fig)
    
    # Pattern analizi
    st.subheader("📊 Tüketim Paterni Analizi")
    pattern_fig = create_pattern_analysis(df)
    if pattern_fig:
        st.pyplot(pattern_fig)
    else:
        st.info("Pattern analizi için daha fazla veri gerekiyor.")
    
    # Detaylı istatistikler
    st.subheader("📋 Detaylı İstatistikler")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Tüketim İstatistikleri:**")
        stats_data = {
            "Ortalama (kWh)": f"{df['consumption_kwh'].mean():.2f}",
            "Medyan (kWh)": f"{df['consumption_kwh'].median():.2f}",
            "Standart Sapma": f"{df['consumption_kwh'].std():.2f}",
            "Minimum (kWh)": f"{df['consumption_kwh'].min():.2f}",
            "Maksimum (kWh)": f"{df['consumption_kwh'].max():.2f}"
        }
        for key, value in stats_data.items():
            st.text(f"{key}: {value}")
    
    with col2:
        st.write("**Anomali Analizi:**")
        if 'anomaly' in df.columns:
            anomaly_stats = detector.get_anomaly_statistics(df, 'detected_anomaly')
            for key, value in anomaly_stats.items():
                key_tr = {
                    'toplam_veri_noktasi': 'Toplam Veri Noktası',
                    'anomali_sayisi': 'Tespit Edilen Anomali',
                    'anomali_orani': 'Anomali Oranı (%)',
                    'ortalama_anomali_tuketim': 'Ort. Anomali Tüketim (kWh)',
                    'ortalama_normal_tuketim': 'Ort. Normal Tüketim (kWh)',
                    'anomali_etkisi_yuzde': 'Anomali Etkisi (%)'
                }.get(key, key)
                st.text(f"{key_tr}: {value}")
    
    # Veri tablosu (son kayıtlar)
    with st.expander("📄 Veri Detayları (Son 20 Kayıt)"):
        display_columns = ['consumption_kwh', 'cost_TL', 'detected_anomaly']
        if 'anomaly' in df.columns:
            display_columns.append('anomaly')
        
        recent_data = df[display_columns].tail(20).copy()
        recent_data.columns = ['Tüketim (kWh)', 'Maliyet (TL)', 'Tespit Edilen Anomali'] + (['Gerçek Anomali'] if 'anomaly' in df.columns else [])
        
        st.dataframe(recent_data, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "*Dashboard güncelleme zamanı: " + 
        datetime.now().strftime('%d/%m/%Y %H:%M:%S') + "*"
    )

if __name__ == "__main__":
    main()
