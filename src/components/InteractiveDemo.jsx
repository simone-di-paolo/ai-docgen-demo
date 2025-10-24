import React, { useState, useMemo } from 'react';
import './InteractiveDemo.css'; // Importiamo il nuovo CSS

const DEFAULT_STATE = {
  themeColor: '#8a3ffc',
  fontSize: 16,
  isDarkMode: true,
  textAreaText: 'Usa i controlli qui sotto per modificare il mio aspetto. Dimensione, font e colore del titolo cambieranno.',
  fontFamily: 'Roboto, sans-serif',
  textAlign: 'left',
};

function InteractiveDemo() {
  const [themeColor, setThemeColor] = useState(DEFAULT_STATE.themeColor);
  const [fontSize, setFontSize] = useState(DEFAULT_STATE.fontSize);
  const [isDarkMode, setIsDarkMode] = useState(DEFAULT_STATE.isDarkMode);
  const [textAreaText, setTextAreaText] = useState(DEFAULT_STATE.textAreaText);
  const [fontFamily, setFontFamily] = useState(DEFAULT_STATE.fontFamily);
  const [textAlign, setTextAlign] = useState(DEFAULT_STATE.textAlign);
  const [isItalic, setIsItalic] = useState(false);

  const themeStyles = {
    '--dynamic-theme-color': themeColor,
    fontSize: `${fontSize}px`,
    fontFamily: fontFamily,
  };

  // Funzioni di trasformazione del testo
  const handleTextTransform = (transform) => {
    switch(transform) {
      case 'uppercase':
        setTextAreaText(textAreaText.toUpperCase());
        break;
      case 'lowercase':
        setTextAreaText(textAreaText.toLowerCase());
        break;
      case 'capitalize':
        setTextAreaText(textAreaText.replace(/\b\w/g, char => char.toUpperCase()));
        break;
      default: break;
    }
  }

  // Conteggio caratteri e parole
  const wordCount = useMemo(() => {
    return textAreaText.trim().split(/\s+/).filter(Boolean).length;
  }, [textAreaText]);

  const charCount = textAreaText.length;

  // Funzione di Reset
  const handleReset = () => {
    setThemeColor(DEFAULT_STATE.themeColor);
    setFontSize(DEFAULT_STATE.fontSize);
    setIsDarkMode(DEFAULT_STATE.isDarkMode);
    setTextAreaText(DEFAULT_STATE.textAreaText);
    setFontFamily(DEFAULT_STATE.fontFamily);
    setTextAlign(DEFAULT_STATE.textAlign);
  }

  const pStyle = {
    textAlign: textAlign,
  };

  return (
    <section id="interactive-demo" className={`interactive-demo ${isDarkMode ? 'dark-mode' : 'light-mode'}`}>
      <h2 className="section-title">Personalizza in Tempo Reale</h2>
      <div className="demo-container">

        {/* Preview Area */}
        <div className="demo-preview" style={themeStyles}>
          <div className="preview-card">
            <h4 className="preview-title" style={{ color: themeColor }}>Card Personalizzabile</h4>
            <p className="preview-text" style={pStyle}>{textAreaText}</p>
            <button className="preview-button" style={{ backgroundColor: themeColor }}>Provalo!</button>
          </div>
        </div>

        {/* Controls Area */}
        <div className="demo-controls">
          {/* Controlli Esistenti */}
          <div className="control-group">
            <label htmlFor="color-picker">Colore del Tema</label>
            <input type="color" id="color-picker" value={themeColor} onChange={(e) => setThemeColor(e.target.value)} />
          </div>
          <div className="control-group">
            <label htmlFor="font-slider">Dimensione Font ({fontSize}px)</label>
            <input type="range" id="font-slider" min="12" max="24" value={fontSize} onChange={(e) => setFontSize(e.target.value)} />
          </div>
          <div className="control-group">
            <label htmlFor="font-picker">Tipo di Font</label>
            <select id="font-picker" value={fontFamily} onChange={(e) => setFontFamily(e.target.value)} className="font-picker-select">
              <option value="Roboto, sans-serif">Roboto</option>
              <option value="Arial, sans-serif">Arial</option>
              <option value="Georgia, serif">Georgia</option>
              <option value="'Courier New', monospace">Courier New</option>
              <option value="'Brush Script MT', cursive">Brush Script</option>
            </select>
          </div>
          <div className="control-group">
            <label>Modalità</label>
            <label className="switch"><input type="checkbox" checked={isDarkMode} onChange={() => setIsDarkMode(!isDarkMode)} /><span className="slider round"></span></label>
          </div>

          {/* Nuovi Controlli per la Textarea */}
          <div className="control-group">
            <label htmlFor="desc-editor">Modifica descrizione</label>
            <textarea
              id="desc-editor"
              className="demo-text-area"
              value={textAreaText}
              onChange={(e) => setTextAreaText(e.target.value)}
            />
            <div className="char-counter">{charCount} caratteri | {wordCount} parole</div>
            
            <div className="button-group">
                <button onClick={() => handleTextTransform('uppercase')}>AA</button>
                <button onClick={() => handleTextTransform('lowercase')}>aa</button>
                <button onClick={() => handleTextTransform('capitalize')}>Aa</button>
            </div>

            <div className="button-group">
                <button onClick={() => setTextAlign('left')}>Sinistra</button>
                <button onClick={() => setTextAlign('center')}>Centro</button>
                <button onClick={() => setTextAlign('right')}>Destra</button>
            </div>
          </div>
          
          {/* Pulsante di Reset */}
          <button className="reset-button" onClick={handleReset}>Reset</button>

        </div>
      </div>
    </section>
  );
}

export default InteractiveDemo;