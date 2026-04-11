import React from 'react';
import { CloudRain, Mountain, Activity, Settings } from 'lucide-react';

export default function Sidebar({ rainfall, setRainfall }) {
  return (
    <aside className="w-80 bg-slate-900 border-r border-slate-800 p-6 flex flex-col gap-8 flex-shrink-0">
      <section>
        <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-widest mb-4">Parameters</h2>
        
        <div className="space-y-6">
          {/* Rainfall Slider */}
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <label className="text-sm flex items-center gap-2 text-slate-300">
                <CloudRain size={16} className="text-emerald-400" /> 
                Rainfall (mm/h)
              </label>
              <span className="text-emerald-400 font-mono font-bold">{rainfall}</span>
            </div>
            <input 
              type="range" 
              className="w-full h-1.5 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-emerald-500"
              value={rainfall}
              min="0"
              max="200"
              onChange={(e) => setRainfall(Number(e.target.value))}
            />
          </div>

          <div className="p-4 bg-slate-800/50 rounded-xl border border-slate-700">
            <div className="flex items-center gap-3 mb-2">
              <Mountain size={18} className="text-slate-400" />
              <span className="text-sm text-slate-200">Terrain Analysis</span>
            </div>
            <p className="text-xs text-slate-500 italic">DEM Data: OpenTopography Global 30m</p>
          </div>
        </div>
      </section>

      <section className="mt-auto">
        <button className="w-full py-3 bg-emerald-600 hover:bg-emerald-500 transition-all duration-300 rounded-lg font-bold flex items-center justify-center gap-2 text-white shadow-lg shadow-emerald-900/20 active:scale-95">
          <Activity size={18}/> RUN GLOBAL SCAN
        </button>
      </section>
    </aside>
  );
}
