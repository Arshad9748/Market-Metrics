import React, { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';
import 'plotly.js/dist/plotly';
import '../styles/Analytics.css';

const Analytics = () => {
  const [visualizations, setVisualizations] = useState({
    dashboard: null,
    forecast: null,
    heatmap: null
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('dashboard');

  useEffect(() => {
    const fetchAllData = async () => {
      try {
        const endpoints = [
          'sales-dashboard',
          'sales-forecast',
          'sales-heatmap',
          'price-forecast'
        ];

        const results = await Promise.all(
          endpoints.map(async endpoint => {
            try {
              const response = await fetch(`http://localhost:5000/api/analytics/${endpoint}`, {
                headers: {
                  'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
              });
              const data = await response.json();
              if (!data.success) {
                console.error(`API Error for ${endpoint}:`, data.error);
                return { success: false, error: data.error };
              }
              return data;
            } catch (err) {
              console.error(`Error fetching ${endpoint}:`, err);
              return { success: false, error: err.message };
            }
          })
        );

        const newVisualizations = {};
        endpoints.forEach((endpoint, index) => {
          const key = endpoint === 'top-categories' ? 'categories' : endpoint.replace('sales-', '');
          
          if (results[index].success) {
            const data = results[index].data;

            if (key === 'dashboard') {
              if (data && data.data) {
                newVisualizations[key] = {
                  data: Array.isArray(data.data) ? data.data : [data.data],
                  layout: {
                    ...data.layout,
                    title: 'Sales Dashboard',
                    height: 600,
                    margin: { l: 50, r: 50, t: 80, b: 50 },
                    showlegend: true,
                    legend: {
                      orientation: 'h',
                      y: -0.2
                    },
                    xaxis: {
                      ...data.layout?.xaxis,
                      gridcolor: '#E5E5E5',
                      zerolinecolor: '#E5E5E5'
                    },
                    yaxis: {
                      ...data.layout?.yaxis,
                      gridcolor: '#E5E5E5',
                      zerolinecolor: '#E5E5E5'
                    },
                    plot_bgcolor: '#FFFFFF',
                    paper_bgcolor: '#FFFFFF'
                  }
                };
              } else {
                console.error('Invalid dashboard data structure:', data);
              }
            } else if (key === 'categories') {
              if (data?.data) {
                newVisualizations[key] = {
                  data: data.data.data,
                  layout: {
                    ...data.data.layout,
                    title: data.data.title?.text || 'Top Categories Analysis',
                    height: 600,
                    margin: { l: 50, r: 50, t: 80, b: 100 },
                    showlegend: true,
                    legend: {
                      orientation: 'h',
                      y: -0.2
                    },
                    xaxis: {
                      ...data.data.xaxis,
                      title: data.data.xaxis?.title?.text || 'Category',
                      tickangle: -45,
                      automargin: true,
                      gridcolor: '#E5E5E5',
                      zerolinecolor: '#E5E5E5'
                    },
                    yaxis: {
                      ...data.data.yaxis,
                      title: data.data.yaxis?.title?.text || 'Quantity Sold (kg)',
                      gridcolor: '#E5E5E5',
                      zerolinecolor: '#E5E5E5'
                    },
                    yaxis2: {
                      ...data.data.yaxis2,
                      title: data.data.yaxis2?.title?.text || 'Revenue (RMB)',
                      overlaying: 'y',
                      side: 'right',
                      gridcolor: '#E5E5E5',
                      zerolinecolor: '#E5E5E5'
                    },
                    plot_bgcolor: '#FFFFFF',
                    paper_bgcolor: '#FFFFFF'
                  }
                };
              } else {
                console.error('Invalid categories data structure:', data);
              }
            } else if (key === 'forecast') {
              const plotData = data?.data?.data || data?.data || data;
              if (plotData) {
                newVisualizations[key] = {
                  data: Array.isArray(plotData) ? plotData : [plotData],
                  layout: {
                    title: 'Sales Forecast',
                    height: 600,
                    margin: { l: 50, r: 50, t: 80, b: 50 },
                    hovermode: 'closest',
                    hoverlabel: {
                      bgcolor: 'white',
                      font: { size: 12 }
                    },
                    xaxis: {
                      gridcolor: '#E5E5E5',
                      zerolinecolor: '#E5E5E5'
                    },
                    yaxis: {
                      gridcolor: '#E5E5E5',
                      zerolinecolor: '#E5E5E5'
                    },
                    plot_bgcolor: '#FFFFFF',
                    paper_bgcolor: '#FFFFFF'
                  }
                };
              } else {
                console.error('Invalid performance data structure:', data);
              }
            } else if (key === 'priceForecast') {
              const plotData = data?.data?.data || data?.data || data;
              if (plotData) {
                newVisualizations[key] = {
                  data: Array.isArray(plotData) ? plotData : [plotData],
                  layout: {
                    title: 'Price Forecast',
                    height: 600,
                    margin: { l: 50, r: 50, t: 80, b: 50 },
                    hovermode: 'closest',
                    hoverlabel: {
                      bgcolor: 'white',
                      font: { size: 12 }
                    },
                    xaxis: {
                      gridcolor: '#E5E5E5',
                      zerolinecolor: '#E5E5E5'
                    },
                    yaxis: {
                      gridcolor: '#E5E5E5',
                      zerolinecolor: '#E5E5E5'
                    },
                    plot_bgcolor: '#FFFFFF',
                    paper_bgcolor: '#FFFFFF'
                  }
                };
              } else {
                console.error('Invalid price forecast data structure:', data);
              }
            } else {
              newVisualizations[key] = data;
            }
          } else {
            console.error(`Failed to load ${key} visualization:`, results[index].error);
          }
        });
        setVisualizations(newVisualizations);
      } catch (err) {
        console.error('Error in fetchAllData:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchAllData();
  }, []);

  const renderVisualization = () => {
    const currentViz = visualizations[activeTab];
    
    if (!currentViz) {
      return (
        <div className="error-container">
          <p>No data available for this visualization.</p>
          <p>Please check the console for more details.</p>
        </div>
      );
    }
    if (!currentViz.data || !currentViz.layout) {
      return (
        <div className="error-container">
          <p>Invalid visualization data structure.</p>
          <p>Please check the console for more details.</p>
        </div>
      );
    }

    return (
      <Plot
        data={currentViz.data}
        layout={currentViz.layout}
        style={{ width: '100%', height: '600px' }}
        config={{ responsive: true }}
      />
    );
  };

  if (loading) return (
    <div className="loading-container">
      <div className="loading-spinner"></div>
      <p className='font-bold text-white' >Loading analytics data...</p>
    </div>
  );
  
  if (error) return (
    <div className="error-container">
      <h2>Error Loading Analytics</h2>
      <p>{error}</p>
      <button onClick={() => window.location.reload()}>Retry</button>
    </div>
  );

  return (
    <div className="analytics-container">
      <h1>Sales Analytics Dashboard</h1>
      <div className="tabs-container">
        <button 
          className={`tab-button ${activeTab === 'dashboard' ? 'active' : ''}`}
          onClick={() => setActiveTab('dashboard')}
        >
          Sales Overview
        </button>
        <button 
          className={`tab-button ${activeTab === 'forecast' ? 'active' : ''}`}
          onClick={() => setActiveTab('forecast')}
        >
          Sales Forecast
        </button>
        <button 
          className={`tab-button ${activeTab === 'heatmap' ? 'active' : ''}`}
          onClick={() => setActiveTab('heatmap')}
        >
          Sales Heatmap
        </button>
      </div>

      <div className="visualization-container">
        {renderVisualization()}
      </div>
    </div>
  );
};

export default Analytics; 