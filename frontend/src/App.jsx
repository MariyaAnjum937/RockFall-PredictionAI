import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import MapView from './components/MapView';
import RiskPanel from './components/RiskPanel';
import LandingPage from './components/LandingPage';
import { Activity, LogOut } from 'lucide-react';

function Dashboard({ onExit }) {
  const [selectedArea, setSelectedArea] = useState(null);
  const [rainfall, setRainfall] = useState(50);
  const [loading, setLoading] = useState(false);

  // Simulated prediction trigger
  const handleLocationSelect = (lat, lng) => {
    setLoading(true);
    // Simulate API Call
    setTimeout(() => {
      setSelectedArea({
        lat, lng,
        risk: Math.floor(Math.random() * 3), // 0: Low, 1: Med, 2: High
        slope: (25 + Math.random() * 15).toFixed(1) + "°",
        elevation: (1000 + Math.random() * 2000).toFixed(0) + "m",
        roughness: "High"
      });
      setLoading(false);
    }, 800);
  };

  return (
    <div className="flex h-screen w-full bg-slate-950 text-slate-100 overflow-hidden font-sans">
      <Sidebar rainfall={rainfall} setRainfall={setRainfall} />
      
      <main className="relative flex-1 flex flex-col">
        {/* Header */}
        <header className="p-4 bg-slate-900/80 border-b border-slate-800 backdrop-blur-md flex justify-between items-center z-[1001]">
          <h1 className="text-xl font-black tracking-tight text-emerald-400">
            GEO-SHIELD <span className="text-slate-500 font-light ml-2 border-l border-slate-700 pl-2">Rockfall Prediction AI</span>
          </h1>
          <div className="flex gap-4 text-xs font-mono items-center">
            <span className="flex items-center gap-2 bg-emerald-500/10 text-emerald-500 px-3 py-1 rounded-full border border-emerald-500/20">
              <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"/> 
              SYSTEM LIVE
            </span>
            <button 
              onClick={onExit}
              className="flex items-center gap-2 text-slate-400 hover:text-white bg-slate-800/50 hover:bg-slate-700 p-1.5 px-3 rounded-full transition-colors border border-slate-700"
            >
              <LogOut size={14} /> EXIT
            </button>
          </div>
        </header>

        {/* Map Area */}
        <div className="relative flex-1 bg-slate-950">
          <MapView onSelectLocation={handleLocationSelect} selectedArea={selectedArea} />
          
          {/* Overlay Risk Panel */}
          {selectedArea && (
            <RiskPanel data={selectedArea} rainfall={rainfall} loading={loading} />
          )}
          
          {/* Legend/Help Text Overlay */}
          {!selectedArea && !loading && (
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-center pointer-events-none z-[1000]">
              <div className="bg-slate-900/80 backdrop-blur-xl p-8 rounded-3xl border border-slate-700 shadow-2xl">
                <div className="w-16 h-16 bg-emerald-500/20 rounded-full flex items-center justify-center mx-auto mb-4 border border-emerald-500/30">
                  <Activity className="text-emerald-500" size={32} />
                </div>
                <h2 className="text-2xl font-bold mb-2">Ready to Analyze</h2>
                <p className="text-slate-400 max-w-xs">
                  Click anywhere on the map to run a terrain risk analysis for that specific coordinate.
                </p>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default function App() {
  const [hasStarted, setHasStarted] = useState(false);

  return hasStarted ? (
    <Dashboard onExit={() => setHasStarted(false)} />
  ) : (
    <LandingPage onLaunch={() => setHasStarted(true)} />
  );
}
