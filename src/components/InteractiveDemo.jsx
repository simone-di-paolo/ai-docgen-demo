import React, { useState } from 'react';

function InteractiveDemo() {
  const [themeColor, setThemeColor] = useState('#8a3ffc');
  const [fontSize, setFontSize] = useState(16);
  const [isDarkMode, setIsDarkMode] = useState(true);
  const [fontFamily, setFontFamily] = useState('Roboto, sans-serif');

  const themeStyles = {
    '--dynamic-theme-color': themeColor,
    fontSize: `${fontSize}px`,
    fontFamily: fontFamily,
  };

  return (
    <section id="interactive-demo" className={`interactive-demo ${isDarkMode ? 'dark-mode' : 'light-mode'}`}>
      <h2 className="section-title">Personalizza in Tempo Reale</h2>
      <div className="demo-container">

        {/* Preview Area */}
        <div className="demo-preview" style={themeStyles}>
          <div className="preview-card">
            <h4 className="preview-title" style={{ color: themeColor }}>Card Personalizzabile</h4>
            <p className="preview-text">Usa i controlli qui sotto per modificare il mio aspetto. Dimensione, font e colore del titolo cambieranno.</p>
            <button className="preview-button" style={{ backgroundColor: themeColor }}>Provalo!</button>
          </div>
        </div>

        {/* Controls Area */}
        <div className="demo-controls">
          <div className="control-group">
            <label htmlFor="color-picker">Colore del Tema</label>
            <input 
              type="color" 
              id="color-picker" 
              value={themeColor} 
              onChange={(e) => setThemeColor(e.target.value)} 
            />
          </div>
          <div className="control-group">
            <label htmlFor="font-slider">Dimensione Font ({fontSize}px)</label>
            <input 
              type="range" 
              id="font-slider" 
              min="12" 
              max="24" 
              value={fontSize} 
              onChange={(e) => setFontSize(e.target.value)} 
            />
          </div>
          <div className="control-group">
            <label htmlFor="font-picker">Tipo di Font</label>
            <select
              id="font-picker"
              value={fontFamily}
              onChange={(e) => setFontFamily(e.target.value)}
              className="font-picker-select"
            >
              <option value="Roboto, sans-serif">Roboto</option>
              <option value="Arial, sans-serif">Arial</option>
              <option value="Georgia, serif">Georgia</option>
              <option value="'Courier New', monospace">Courier New</option>
              <option value="'Brush Script MT', cursive">Brush Script</option>
            </select>
          </div>
          <div className="control-group">
            <label>Modalità</label>
            <label className="switch">
              <input 
                type="checkbox" 
                checked={isDarkMode}
                onChange={() => setIsDarkMode(!isDarkMode)}
              />
              <span className="slider round"></span>
            </label>
          </div>
        </div>
      </div>
    </section>
  );
}

export default InteractiveDemo;
