import React, { useState, useMemo } from 'react';
import './InteractiveDemo.css'; // Import the new CSS

const DEFAULT_STATE = {
  themeColor: '#8a3ffc',
  fontSize: 16,
  isDarkMode: true,
  textAreaText: 'Use the controls below to change my appearance. The title color, font size, and font family will change.',
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
  const [isUnderlined, setIsUnderlined] = useState(false);
  const [isCopied, setIsCopied] = useState(false);

  const themeStyles = {
    '--dynamic-theme-color': themeColor,
    fontSize: `${fontSize}px`,
    fontFamily: fontFamily,
  };

  // Text transformation functions
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
      case 'underline':
        setIsUnderlined(!isUnderlined);
        break;
      default: break;
    }
  }

  // Character and word count
  const wordCount = useMemo(() => {
    return textAreaText.trim().split(/\s+/).filter(Boolean).length;
  }, [textAreaText]);

  const charCount = textAreaText.length;

  // Reset function
  const handleReset = () => {
    setThemeColor(DEFAULT_STATE.themeColor);
    setFontSize(DEFAULT_STATE.fontSize);
    setIsDarkMode(DEFAULT_STATE.isDarkMode);
    setTextAreaText(DEFAULT_STATE.textAreaText);
    setFontFamily(DEFAULT_STATE.fontFamily);
    setTextAlign(DEFAULT_STATE.textAlign);
    setIsUnderlined(false);
  }
  
    const handleExportCss = () => {
    const cssOutput = `
.custom-card {
  background-color: ${isDarkMode ? '#2c2c2c' : '#ffffff'};
  color: ${isDarkMode ? '#ffffff' : '#333333'};
  border: 1px solid ${isDarkMode ? '#555' : '#ddd'};
  border-radius: 12px;
  padding: 1.5rem;
  font-family: ${fontFamily};
  font-size: ${fontSize}px;
}

.custom-card-title {
  color: ${themeColor};
  font-size: 1.5em; /* Example size */
  margin-bottom: 0.5em;
}

.custom-card-text {
  text-align: ${textAlign};
  text-decoration: ${isUnderlined ? 'underline' : 'none'};
}

.custom-card-button {
  background-color: ${themeColor};
  color: #ffffff;
  border: none;
  padding: 0.8rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.custom-card-button:hover {
  opacity: 0.9;
}
    `;

    navigator.clipboard.writeText(cssOutput.trim());
    setIsCopied(true);
    setTimeout(() => setIsCopied(false), 2000);
  };


  const pStyle = {
    textAlign: textAlign,
    textDecoration: isUnderlined ? 'underline' : 'none',
  };

  return (
    <section id="interactive-demo" className={`interactive-demo ${isDarkMode ? 'dark-mode' : 'light-mode'}`}>
      <h2 className="section-title">Real-Time Customization</h2>
      <div className="demo-container">

        {/* Preview Area */}
        <div className="demo-preview" style={themeStyles}>
          <div className="preview-card">
            <h4 className="preview-title" style={{ color: themeColor }}>Customizable Card</h4>
            <p className="preview-text" style={pStyle}>{textAreaText}</p>
            <button className="preview-button" style={{ backgroundColor: themeColor }}>Try it!</button>
          </div>
        </div>

        {/* Controls Area */}
        <div className="demo-controls">
          {/* Existing Controls */}
          <div className="control-group">
            <label htmlFor="color-picker">Theme Color</label>
            <input type="color" id="color-picker" value={themeColor} onChange={(e) => setThemeColor(e.target.value)} />
          </div>
          <div className="control-group">
            <label htmlFor="font-slider">Font Size ({fontSize}px)</label>
            <input type="range" id="font-slider" min="12" max="24" value={fontSize} onChange={(e) => setFontSize(e.target.value)} />
          </div>
          <div className="control-group">
            <label htmlFor="font-picker">Font Family</label>
            <select id="font-picker" value={fontFamily} onChange={(e) => setFontFamily(e.target.value)} className="font-picker-select">
              <option value="Roboto, sans-serif">Roboto</option>
              <option value="Arial, sans-serif">Arial</option>
              <option value="Georgia, serif">Georgia</option>
              <option value="'Courier New', monospace">Courier New</option>
              <option value="'Brush Script MT', cursive">Brush Script</option>
            </select>
          </div>
          <div className="control-group">
            <label>Mode</label>
            <label className="switch"><input type="checkbox" checked={isDarkMode} onChange={() => setIsDarkMode(!isDarkMode)} /><span className="slider round"></span></label>
          </div>

          {/* New Textarea Controls */}
          <div className="control-group">
            <label htmlFor="desc-editor">Edit Description</label>
            <textarea
              id="desc-editor"
              className="demo-text-area"
              value={textAreaText}
              onChange={(e) => setTextAreaText(e.target.value)}
            />
            <div className="char-counter">{charCount} characters | {wordCount} words</div>
            
            <div className="button-group">
                <button onClick={() => handleTextTransform('uppercase')}>AA</button>
                <button onClick={() => handleTextTransform('lowercase')}>aa</button>
                <button onClick={() => handleTextTransform('capitalize')}>Aa</button>
                <button onClick={() => handleTextTransform('underline')}>Underline</button>
            </div>

            <div className="button-group">
                <button onClick={() => setTextAlign('left')}>Left</button>
                <button onClick={() => setTextAlign('center')}>Center</button>
                <button onClick={() => setTextAlign('right')}>Right</button>
            </div>

          </div>
          
          {/* Action Buttons */}
          <div className="action-buttons">
            <button className="reset-button" onClick={handleReset}>Reset</button>
            <button className="export-button" onClick={handleExportCss}>
              {isCopied ? 'Copied!' : 'Export CSS'}
            </button>
          </div>

        </div>
      </div>
    </section>
  );
}

export default InteractiveDemo;
