import React from 'react';
import '../App.css';

const FeatureCard = ({ icon, title, description }) => (
  <div className="feature-card">
    <div className="feature-icon">{icon}</div>
    <h3 className="feature-title">{title}</h3>
    <p className="feature-description">{description}</p>
  </div>
);

// Simple SVG Icons for demonstration
const DynamicIcon = () => (
    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
);

const ReactiveIcon = () => (
    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M17 2.1l4 4-4 4"/><path d="M3 12.6V8.4a2.4 2.4 0 012.4-2.4H21"/><path d="M7 21.9l-4-4 4-4"/><path d="M21 11.4v4.2a2.4 2.4 0 01-2.4 2.4H3"/></svg>
);

const AIIcon = () => (
    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 8V4H8"/><rect x="4" y="4" width="16" height="16" rx="2"/><path d="M8 12h4"/><path d="M12 16h-4"/></svg>
);


function Features() {
  return (
    <section className="features">
      <h2 className="section-title">Funzionalità Potenti</h2>
      <div className="features-grid">
        <FeatureCard 
          icon={<DynamicIcon />} 
          title="Componenti Dinamici" 
          description="Componenti riutilizzabili e modulari costruiti con React per la massima flessibilità."
        />
        <FeatureCard 
          icon={<ReactiveIcon />} 
          title="Stato Reattivo" 
          description="Gestione dello stato efficiente che aggiorna l'UI istantaneamente al variare dei dati."
        />
        <FeatureCard 
          icon={<AIIcon />} 
          title="Documentazione AI" 
          description="La documentazione viene generata e aggiornata automaticamente dall'IA ad ogni modifica."
        />
      </div>
    </section>
  );
}

export default Features;
