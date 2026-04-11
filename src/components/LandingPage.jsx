import React from 'react';
import { Shield, Mountain, Activity, Globe, ChevronRight, Zap, Target, Lock } from 'lucide-react';

export default function LandingPage({ onLaunch }) {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 selection:bg-emerald-500/30 font-sans overflow-x-hidden">
      {/* Background Decorative Elements */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-emerald-500/10 blur-[120px] rounded-full animate-float" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-blue-500/10 blur-[120px] rounded-full animate-float" style={{ animationDelay: '-3s' }} />
      </div>

      <nav className="relative z-10 flex justify-between items-center p-6 lg:px-12 backdrop-blur-sm border-b border-white/5 animate-fade-in opacity-0">
        <div className="flex items-center gap-2 group cursor-pointer">
          <div className="w-8 h-8 bg-emerald-500 flex items-center justify-center rounded-lg shadow-[0_0_15px_rgba(16,185,129,0.5)] group-hover:rotate-12 transition-transform duration-300">
            <Shield className="text-slate-950" size={18} />
          </div>
          <span className="text-xl font-black tracking-tighter">GEO-SHIELD</span>
        </div>
        <div className="hidden md:flex gap-8 text-sm font-medium text-slate-400">
          <a href="#" className="hover:text-emerald-400 transition-colors relative group">
            Technology
            <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-emerald-400 transition-all group-hover:w-full" />
          </a>
          <a href="#" className="hover:text-emerald-400 transition-colors relative group">
            Safety Protocols
            <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-emerald-400 transition-all group-hover:w-full" />
          </a>
          <a href="#" className="hover:text-emerald-400 transition-colors relative group">
            Global Network
            <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-emerald-400 transition-all group-hover:w-full" />
          </a>
        </div>
        <button 
          onClick={onLaunch}
          className="bg-white text-slate-950 px-5 py-2 rounded-full text-sm font-bold hover:bg-emerald-400 hover:text-white transition-all active:scale-95 flex items-center gap-2 group"
        >
          GO LIVE <ChevronRight size={16} className="group-hover:translate-x-1 transition-transform" />
        </button>
      </nav>

      <main className="relative z-10">
        {/* Hero Section */}
        <section className="pt-20 pb-32 px-6 text-center lg:pt-32">
          <div className="inline-flex items-center gap-2 bg-emerald-500/10 text-emerald-500 px-4 py-1 rounded-full text-xs font-bold border border-emerald-500/20 mb-8 animate-fade-in opacity-0 stagger-1">
            <Zap size={12} fill="currentColor" /> NEW: GLOBAL TERRAIN SCAN v4.0
          </div>
          <h1 className="text-5xl lg:text-7xl font-black tracking-tighter mb-6 bg-gradient-to-b from-white to-slate-400 bg-clip-text text-transparent max-w-4xl mx-auto leading-[1.1] animate-fade-in opacity-0 stagger-2">
            Predict Rockfall Risks Before They Happen.
          </h1>
          <p className="text-slate-400 text-lg lg:text-xl max-w-2xl mx-auto mb-12 animate-fade-in opacity-0 stagger-3">
            AI-driven geological analysis for disaster prevention. Leveraging OpenTopography 30m DEM data and real-time precipitation monitoring.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center animate-fade-in opacity-0 stagger-4">
            <button 
              onClick={onLaunch}
              className="bg-emerald-600 hover:bg-emerald-500 text-white px-8 py-4 rounded-2xl font-black flex items-center justify-center gap-3 transition-all active:scale-95 group animate-pulse-glow"
            >
              LAUNCH COMMAND CENTER <Activity size={20} className="group-hover:animate-pulse" />
            </button>
            <button className="bg-slate-900 hover:bg-slate-800 text-slate-300 px-8 py-4 rounded-2xl font-bold flex items-center justify-center gap-3 transition-all border border-slate-800 group overflow-hidden relative">
              <span className="relative z-10">WATCH NETWORK OVERVIEW</span>
              <div className="absolute inset-0 bg-white/5 translate-x-[-100%] group-hover:translate-x-0 transition-transform duration-500" />
            </button>
          </div>
        </section>

        {/* Features Grid */}
        <section className="max-w-7xl mx-auto px-6 grid md:grid-cols-3 gap-6 mb-32">
          <div className="animate-fade-in opacity-0 stagger-1">
            <FeatureCard 
              icon={<Target className="text-emerald-400" />}
              title="Precision Targeting"
              desc="Analyze specific slope geometries with centimeter-level precision using global elevation models."
            />
          </div>
          <div className="animate-fade-in opacity-0 stagger-2">
            <FeatureCard 
              icon={<Globe className="text-blue-400" />}
              title="Global Coverage"
              desc="Monitoring across 190+ countries with active tectonic and geomorphic risk evaluation."
            />
          </div>
          <div className="animate-fade-in opacity-0 stagger-3">
            <FeatureCard 
              icon={<Lock className="text-amber-400" />}
              title="Safety Protocols"
              desc="Automated alert systems with direct integration to local evacuation and emergency APIs."
            />
          </div>
        </section>

        {/* Stats / Proof Section */}
        <section className="bg-slate-900/50 border-y border-white/5 py-20 px-6 backdrop-blur-md relative overflow-hidden">
          <div className="max-w-7xl mx-auto flex flex-wrap justify-around gap-12 text-center relative z-10">
            <Stat label="Global Nodes" value="1.2k+" />
            <Stat label="Prediction Accuracy" value="98.2%" />
            <Stat label="Data Refreshed" value="Every 15m" />
            <Stat label="Active Scans" value="247" />
          </div>
        </section>
      </main>

      <footer className="relative z-10 p-12 lg:px-24 border-t border-white/5 text-slate-500 text-sm flex flex-col items-center gap-8">
        <div className="flex items-center gap-2 opacity-50 grayscale hover:grayscale-0 transition-all duration-700">
          <span className="font-mono">PARTNERS //</span>
          <div className="h-4 w-px bg-slate-800 mx-2" />
          <span>OpenTopography</span>
          <div className="h-4 w-px bg-slate-800 mx-2" />
          <span>Google Earth</span>
          <div className="h-4 w-px bg-slate-800 mx-2" />
          <span>EarthEngine</span>
        </div>
        <div className="text-center italic opacity-40">
          © 2026 GEO-SHIELD ANALYTICS. ALL RIGHTS RESERVED. SECURED BY ENCRYPTION.
        </div>
      </footer>
    </div>
  );
}

function FeatureCard({ icon, title, desc }) {
  return (
    <div className="p-8 bg-slate-900/40 border border-white/5 rounded-3xl hover:border-emerald-500/30 transition-all hover:translate-y-[-4px] group cursor-pointer h-full">
      <div className="w-12 h-12 bg-white/5 rounded-2xl flex items-center justify-center mb-6 group-hover:bg-emerald-500/10 group-hover:scale-110 transition-all duration-300">
        {icon}
      </div>
      <h3 className="text-xl font-bold mb-3 group-hover:text-emerald-400 transition-colors">{title}</h3>
      <p className="text-slate-400 text-sm leading-relaxed">{desc}</p>
    </div>
  );
}

function Stat({ label, value }) {
  return (
    <div className="group cursor-default">
      <div className="text-4xl lg:text-5xl font-black text-white mb-2 group-hover:scale-110 transition-transform duration-300">{value}</div>
      <div className="text-xs font-bold text-slate-500 uppercase tracking-widest">{label}</div>
    </div>
  );
}
