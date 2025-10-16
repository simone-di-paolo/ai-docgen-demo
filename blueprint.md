# Blueprint del Progetto: Landing Page Interattiva

## Panoramica

Questo documento descrive la struttura e le funzionalità di una landing page moderna e interattiva creata con React. L'applicazione è stata sviluppata da un'intelligenza artificiale per dimostrare le capacità di progettazione e sviluppo rapido di UI complesse e visivamente accattivanti.

## Struttura del Progetto

L'applicazione è composta da quattro sezioni principali, ognuna implementata come un componente React separato:

1.  **Hero Section (`Hero.jsx`):** La prima sezione che l'utente vede. Contiene un titolo d'impatto, un sottotitolo e un pulsante "call to action".
2.  **Features Section (`Features.jsx`):** Una sezione che mette in evidenza le funzionalità principali dell'applicazione attraverso un layout a griglia con schede informative.
3.  **Interactive Demo (`InteractiveDemo.jsx`):** Un'area interattiva dove gli utenti possono personalizzare in tempo reale alcuni elementi dell'interfaccia, come il colore del tema, la dimensione del carattere e la modalità (chiara/scura).
4.  **Showcase Section (`Showcase.jsx`):** Una galleria visiva per mostrare progetti o esempi di componenti, con immagini e informazioni che appaiono al passaggio del mouse.

### Stile e Design

Lo stile dell'applicazione è definito nel file `App.css` e segue un approccio moderno e "dark mode" per impostazione predefinita.

*   **Colori:** La palette di colori è basata su una tonalità di viola come colore primario, con un blu acceso come secondario, su uno sfondo scuro.
*   **Tipografia:** Il font scelto è 'Inter', un carattere sans-serif pulito e moderno, ampiamente utilizzato nel design di interfacce.
*   **Effetti Visivi:**
    *   **Sfondo a Puntini:** Un leggero pattern a puntini sullo sfondo aggiunge una texture sottile.
    *   **Effetto "Glow":** I pulsanti e gli elementi interattivi presentano un'ombra luminosa per creare un effetto "glow".
    *   **Animazioni al Passaggio del Mouse:** Le schede delle funzionalità e gli elementi della vetrina hanno animazioni al passaggio del mouse per migliorare l'interattività.
    *   **Overlay Sfumato:** Le immagini nella vetrina hanno un overlay sfumato con testo che appare al passaggio del mouse.

## Componenti e Funzionalità

### 1. Hero Section

*   **Titolo:** Grande e con un gradiente di colore per attirare l'attenzione.
*   **Sottotitolo:** Fornisce una breve descrizione dello scopo della pagina.
*   **Pulsante "Inizia Ora":** Un pulsante call-to-action con un effetto "glow" al passaggio del mouse.

### 2. Features Section

*   **Griglia Flessibile:** Utilizza CSS Grid per un layout responsive che si adatta a diverse dimensioni dello schermo.
*   **Schede Informative:** Ogni scheda contiene un'icona, un titolo e una descrizione. Le icone sono semplici SVG inclusi direttamente nel componente.
*   **Effetto Hover:** Le schede si sollevano leggermente al passaggio del mouse per dare un feedback visivo.

### 3. Interactive Demo

*   **Stato React:** Utilizza il hook `useState` di React per gestire lo stato dei controlli di personalizzazione (colore, dimensione del carattere, modalità).
*   **Controlli di Personalizzazione:**
    *   **Selettore di Colore:** Un input `type="color"` standard per cambiare il colore del tema.
    *   **Slider per Font:** Un input `type="range"` per regolare la dimensione del carattere.
    *   **Interruttore Modalità:** Un interruttore personalizzato in CSS per passare dalla modalità scura a quella chiara.
*   **Stili Dinamici:** Gli stili vengono applicati dinamicamente utilizzando le variabili CSS e gli stili in linea di React per riflettere le scelte dell'utente in tempo reale.

### 4. Showcase Section

*   **Griglia di Immagini:** Una griglia responsive che mostra immagini di esempio.
*   **Effetto Overlay:** Al passaggio del mouse, un overlay scuro appare sull'immagine, insieme a un titolo e dei "tag" descrittivi.
*   **Animazioni Sottili:** Il titolo e i tag appaiono con una leggera animazione di scorrimento dal basso, e l'immagine si ingrandisce leggermente per un effetto più dinamico.

