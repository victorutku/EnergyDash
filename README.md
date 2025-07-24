# EnergyDash
## Overview

This is a Streamlit-based dashboard application for monitoring and analyzing household electricity consumption. The system generates realistic electricity usage data, detects anomalies in consumption patterns, and provides interactive visualizations for energy monitoring. The application is designed to help users understand their electricity usage patterns and identify unusual consumption behaviors.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web framework for rapid prototyping and deployment
- **Visualization**: Matplotlib for creating consumption charts and graphs
- **UI Components**: Streamlit's built-in widgets for interactive controls and data display
- **Layout**: Wide layout with expandable sidebar for configuration options

### Backend Architecture
- **Data Processing**: Pandas for data manipulation and analysis
- **Statistical Analysis**: NumPy and SciPy for numerical computations and anomaly detection
- **Data Generation**: Custom classes for generating realistic electricity consumption patterns
- **Real-time Updates**: Streamlit's reactive framework for automatic UI updates

### Data Storage Solutions
- **In-Memory Storage**: Data is generated and stored in pandas DataFrames during runtime
- **No Persistent Database**: Currently uses synthetic data generation rather than persistent storage
- **Session State**: Streamlit session state for maintaining data across user interactions

## Key Components

### 1. Data Generator (`data_generator.py`)
- **Purpose**: Generates realistic electricity consumption data
- **Features**:
  - Hourly and daily consumption patterns
  - Time-based multipliers for different periods (morning, evening, night)
  - Weekend/weekday variations
  - Random noise for realistic fluctuations
  - Configurable anomaly injection

### 2. Anomaly Detector (`anomaly_detector.py`)
- **Purpose**: Identifies unusual consumption patterns
- **Methods**:
  - IQR (Interquartile Range) method
  - Z-Score statistical analysis
  - Rolling window anomaly detection
- **Configurable Sensitivity**: Adjustable thresholds for different detection requirements

### 3. Main Application (`app.py`)
- **Purpose**: Streamlit dashboard interface
- **Features**:
  - Interactive data visualization
  - Real-time anomaly highlighting
  - Configurable time periods and detection methods
  - User-friendly controls and displays

## Data Flow

1. **Data Generation**: ElectricityDataGenerator creates synthetic consumption data based on realistic patterns
2. **Anomaly Injection**: Artificial anomalies are added to simulate real-world irregularities
3. **Anomaly Detection**: AnomalyDetector analyzes the data using selected statistical methods
4. **Visualization**: Matplotlib renders consumption charts with anomaly highlights
5. **User Interaction**: Streamlit handles user inputs and updates visualizations reactively

## External Dependencies

### Core Libraries
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Matplotlib**: Plotting and visualization
- **SciPy**: Statistical functions and analysis

### Python Standard Library
- **datetime/timedelta**: Date and time handling
- **random**: Random number generation for data simulation

## Deployment Strategy

### Local Development
- Standard Python environment with pip requirements
- Streamlit development server for local testing
- No external database or service dependencies

### Production Considerations
- **Containerization**: Application is suitable for Docker deployment
- **Cloud Platforms**: Compatible with Streamlit Cloud, Heroku, or similar platforms
- **Scalability**: Currently designed for single-user sessions
- **Data Persistence**: Future enhancement could include database integration for historical data storage

### Configuration
- Environment-specific settings can be managed through Streamlit's configuration system
- No external configuration files currently required
- Settings are managed through the UI interface

## Technical Decisions

### Data Generation Approach
- **Problem**: Need realistic electricity consumption data for demonstration
- **Solution**: Algorithmic generation with time-based patterns and random variations
- **Rationale**: Allows for controlled testing without requiring real consumption data
- **Trade-offs**: Synthetic data may not capture all real-world complexities

### Anomaly Detection Methods
- **Problem**: Multiple approaches needed for different types of anomalies
- **Solution**: Pluggable detector system with IQR, Z-Score, and rolling window methods
- **Rationale**: Different methods excel at detecting different anomaly types
- **Trade-offs**: Multiple methods increase complexity but improve detection coverage

### Streamlit Framework Choice
- **Problem**: Need rapid development of interactive dashboard
- **Solution**: Streamlit for Python-native web applications
- **Rationale**: Minimal web development overhead, excellent for data science applications
- **Trade-offs**: Less customization flexibility compared to full web frameworks
