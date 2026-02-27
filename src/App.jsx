import React from 'react';
import Hero from './components/Hero';
import Features from './components/Features';
import InteractiveDemo from './components/InteractiveDemo';
import Showcase from './components/Showcase';
import UserInfo from './components/UserInfo';
import './App.css';

function App() {
  return (
    <div className="App">
      <Hero />
      <Features />
      <InteractiveDemo />
      <UserInfo />
      <Showcase />
      <footer className="app-footer" style={{ padding: '2rem', textAlign: 'center', opacity: 0.7 }}>
        <p>AI DocGen Demo v1 - Powered by Google Gemini 1.5 Pro</p>
      </footer>
    </div>
  );
}

export default App;
