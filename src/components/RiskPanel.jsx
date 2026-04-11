import React from 'react';
import { AlertTriangle, Info, TrendingUp } from 'lucide-react';

export default function RiskPanel({ data, rainfall, loading }) {
  const risks = [
    { 
      label: 'LOW', 
      color: 'text-emerald-400', 
      bg: 'bg-emerald-500/10', 
      border: 'border-emerald-500/20',
      shadow: 'shadow-emerald-900/10'
    },
    { 
      label: 'MEDIUM', 
      color: 'text-amber-400', 
      bg: 'bg-amber-500/10', 
      border: 'border-amber-500/20',
      shadow: 'shadow-amber-900/10'
    },
    { 
      label: 'HIGH', 
      color: 'text-rose-500', 
      bg: 'bg-rose-500/15', 
      border: 'border-rose-500/40',
      shadow: 'shadow-rose-900/30'
    }
  ];

  const currentRisk = rainfall > 80 ? risks[2] : (data ? risks[data.risk] : risks[0]);

  if (loading) return (
    <div className="absolute bottom-8 right-8 w-72 p-6 bg-slate-900 border border-slate-700 rounded-2xl animate-pulse shadow-2xl z-[1000]">
      <div className="h-4 bg-slate-700 rounded w-1/2 mb-4"></div>
      <div className="h-8 bg-slate-700 rounded mb-2"></div>
      <div className="h-4 bg-slate-700 rounded w-3/4"></div>
    </div>
  );

  if (!data) return null;

  return (
    <div className={`absolute bottom-8 right-8 w-80 p-6 backdrop-blur-xl border-2 rounded-2xl shadow-[0_0_50px_-12px] transition-all duration-700 ease-in-out z-[1000] ${currentRisk.bg} ${currentRisk.border} ${currentRisk.shadow}`}>
      <div className="flex items-center justify-between mb-4">
        <span className={`text-xs font-black tracking-tighter uppercase p-1 px-2 rounded ${currentRisk.bg} ${currentRisk.color} border ${currentRisk.border}`}>
          {currentRisk.label} RISK
        </span>
        <AlertTriangle className={`${currentRisk.color} ${currentRisk.label === 'HIGH' ? 'animate-bounce' : ''}`} size={20} />
      </div>

      <div className="space-y-4">
        <div>
          <h3 className="text-2xl font-bold text-white tracking-tight">Analysis Result</h3>
          <p className="text-slate-400 text-sm mt-1 font-mono">
            LOC: {data.lat.toFixed(4)}, {data.lng.toFixed(4)}
          </p>
        </div>

        <div className="grid grid-cols-2 gap-2 text-xs font-mono">
          <div className="p-2 bg-slate-950/60 rounded border border-white/5">
            <p className="text-slate-500">SLOPE</p>
            <p className="text-slate-200">{data.slope}</p>
          </div>
          <div className="p-2 bg-slate-950/60 rounded border border-white/5">
            <p className="text-slate-500">ELEV</p>
            <p className="text-slate-200">{data.elevation}</p>
          </div>
        </div>

        <div className="pt-4 border-t border-white/10">
          <p className={`text-xs flex items-start gap-2 ${currentRisk.label === 'HIGH' ? 'text-rose-200' : 'text-slate-300'}`}>
            <Info size={14} className="mt-0.5 flex-shrink-0" />
            <span>
              {currentRisk.label === 'HIGH' 
                ? 'CRITICAL: High soil saturation. Evacuation recommended immediately.' 
                : 'Terrain stable under current conditions.'}
            </span>
          </p>
        </div>
      </div>
    </div>
  );
}
