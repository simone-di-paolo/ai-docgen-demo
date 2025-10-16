```markdown
## Componente App

Il componente `App` è il componente radice dell'applicazione. Funge da contenitore principale per tutti gli altri componenti e gestisce lo stile generale dell'applicazione.

### Stili

Il componente `App` utilizza un foglio di stile CSS (`App.css`) per definire il layout e l'aspetto dell'applicazione.

**Modifiche Recenti:**

*   È stato aggiunto un import per i font `Roboto` (pesi 400 e 700) e `Brush Script MT` da Google Fonts nel file `App.css`. Questi font sono ora disponibili per essere utilizzati in tutta l'applicazione. L'URL di importazione è: `https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&family=Brush+Script+MT&display=swap`

*   È definita una variabile CSS `--primary-color` per il colore primario dell'applicazione (#8a3ffc). Questo permette una gestione centralizzata del tema e facilita modifiche future.
```