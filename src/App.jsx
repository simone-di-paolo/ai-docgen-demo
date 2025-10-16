import React from 'react';
import Hero from './components/Hero';
import Features from './components/Features';
import InteractiveDemo from './components/InteractiveDemo';
import Showcase from './components/Showcase';
import './App.css';

function App() {
  return (
    <div className="App">
      <Hero />
      <Features />
      <InteractiveDemo />
      <Showcase />
    </div>
  );
}

export default App;
