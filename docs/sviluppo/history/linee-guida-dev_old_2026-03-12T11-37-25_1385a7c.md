# Guida Rapida allo Sviluppo - AI DocGen Demo v2

Benvenuti nel team! Questa guida rapida vi aiuterà a familiarizzare con la codebase, le convenzioni e i componenti chiave del progetto AI DocGen Demo v2.

## Introduzione

Questo progetto è un'applicazione web frontend costruita con React, che utilizza Redux per la gestione dello stato e Redux Saga per le operazioni asincrone. L'obiettivo è presentare componenti interattivi e un design moderno, con un accenno alla documentazione generata da AI.

## Convenzioni di Sviluppo

### Linguaggio: TypeScript vs JavaScript

Attualmente, il progetto utilizza **JavaScript** con JSX per la definizione dei componenti React. Non ci sono file TypeScript (`.ts` o `.tsx`) presenti nella codebase fornita.

### Styling: SCSS vs CSS

Il progetto utilizza file **CSS** standard per lo styling. Non ci sono file SCSS (`.scss` o `.sass`) presenti nella codebase fornita. Gli stili sono organizzati in file `.css` separati, spesso importati direttamente nei componenti che li utilizzano (`./ComponentName.css`).

### Fetching dei Dati dalle API

Il fetching dei dati dalle API (o da fonti simulate come file JSON) avviene principalmente tramite:

1.  **Redux Saga:** Le operazioni asincrone, come il recupero di liste di utenti, sono gestite da Redux Saga.
    *   Le chiamate API sono definite nel file `src/api/api.js`.
    *   Le saghe in `src/redux/sagas/` orchestrano queste chiamate, gestendo le azioni `_REQUEST`, `_SUCCESS` e `_ERROR`.
    *   Ad esempio, `src/redux/sagas/user.js` gestisce il recupero degli utenti tramite `getUsersApi`.

2.  **`fetch` API:** La `fetch` API nativa del browser viene utilizzata per effettuare le richieste HTTP.
    *   Nel file `src/api/api.js`, la funzione `getUsers` utilizza `fetch` per recuperare dati dal file `src/assets/json/users.json`.

## Struttura del Progetto

La struttura generale segue le convenzioni di un'applicazione React:

```
src/
├── api/             # Moduli per le chiamate API
│   └── api.js
├── assets/          # Risorse statiche (immagini, JSON)
│   └── json/
│       └── users.json
├── components/      # Componenti React riutilizzabili
│   ├── Features.jsx
│   ├── Hero.jsx
│   ├── InteractiveDemo.jsx
│   ├── Showcase.jsx
│   ├── UserInfo.jsx
│   ├── UserInfo.css
│   └── InteractiveDemo.css
├── redux/           # Logica Redux
│   ├── action/      # Azioni Redux
│   │   └── user.js
│   ├── helper/      # Utilità per Redux
│   │   └── createAsyncActionType.js
│   ├── reducer/     # Reducer Redux
│   │   └── user.reducer.js
│   ├── sagas/       # Sagas Redux
│   │   ├── rootSaga.js
│   │   └── user.js
│   ├── selector/    # Selettori Redux (Reselect)
│   │   └── user.js
│   ├── store.js     # Configurazione dello store Redux
│   └── rootReducer.js # Combinazione dei reducer
├── App.css          # Stili globali dell'App
├── App.jsx          # Componente principale dell'applicazione
├── index.css        # Stili CSS globali di base
└── main.jsx         # Punto di ingresso dell'applicazione (rendering React DOM)
```

## Componenti React Principali

Ecco un glossario dei componenti React più importanti, la loro funzione e la loro locazione:

| Componente          | File di Origine             | Descrizione