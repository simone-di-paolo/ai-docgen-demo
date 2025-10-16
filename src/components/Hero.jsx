import React from 'react';
import '../App.css'; // Make sure to import the CSS

function Hero() {
  return (
    <section className="hero">
      <div className="hero-content">
        <h1 className="hero-title">Benvenuto nel Futuro del Web</h1>
        <p className="hero-subtitle">
          Scopri componenti interattivi e un design accattivante, tutto documentato da AI.
        </p>
        <a href="#interactive-demo" className="hero-button">Inizia Ora</a>
      </div>
    </section>
  );
}

export default Hero;
