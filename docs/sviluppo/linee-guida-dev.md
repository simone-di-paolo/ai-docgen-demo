# Developer Guidelines

This document outlines the conventions, tech stack, and data fetching strategies for this project. Adhering to these guidelines will ensure consistency, maintainability, and efficient development.

## Table of Contents

*   [Introduction](#introduction)
*   [Tech Stack](#tech-stack)
*   [Project Structure](#project-structure)
*   [Component Glossary](#component-glossary)
*   [Styling Conventions](#styling-conventions)
*   [State Management (Redux & Redux Saga)](#state-management-redux--redux-saga)
*   [Data Fetching Strategies](#data-fetching-strategies)
*   [Code Conventions](#code-conventions)
*   [Testing](#testing)

## Introduction

This project is a modern React application built with a focus on dynamic components, reactive state management, and AI-driven documentation. The codebase is structured to be modular and scalable.

## Tech Stack

The project utilizes the following core technologies:

*   **React:** A JavaScript library for building user interfaces.
*   **Vite:** A build tool that significantly improves the frontend development experience.
*   **Redux Toolkit:** A set of utilities for efficient Redux development.
*   **Redux Saga:** A middleware for Redux to handle side effects in a more declarative way.
*   **CSS Modules/Plain CSS:** For component-specific styling and global styles.
*   **Prop-Types:** For runtime type checking of props passed to React components.

## Project Structure

The project follows a standard React project structure with some specific additions for state management and components.

```
src/
├── api/             # API service definitions
├── assets/          # Static assets (images, JSON, etc.)
│   └── json/
│       └── users.json
├── components/      # Reusable UI components
│   ├── Features.jsx
│   ├── Hero.jsx
│   ├── InteractiveDemo.jsx
│   ├── Showcase.jsx
│   ├── UserInfo.jsx
│   ├── InteractiveDemo.css
│   ├── UserInfo.css
├── redux/           # Redux store configuration and logic
│   ├── action/      # Action creators
│   │   └── user.js
│   ├── helper/      # Utility functions for Redux
│   │   └── createAsyncActionType.js
│   ├── reducer/     # Reducers
│   │   └── user.reducer.js
│   ├── sagas/       # Redux Saga logic
│   │   ├── rootSaga.js
│   │   └── user.js
│   ├── selector/    # Selectors for accessing Redux state
│   │   └── user.js
│   ├── rootReducer.js
│   └── store.js
├── App.css          # Global styles for the App component
├── App.jsx          # Main App component
├── index.css        # Global CSS variables and base styles
├── main.jsx         # Entry point of the React application
└── provider.jsx     # Redux Provider setup (duplicate of main.jsx logic)
```

## Component Glossary

| Component Name      | Description                                                                                                | File Location             |
| :------------------ | :--------------------------------------------------------------------------------------------------------- | :------------------------ |
| `App`               | The root component of the application, orchestrating the rendering of other sections.                      | `src/App.jsx`             |
| `Hero`              | Displays the main welcome message and a call to action.                                                    | `src/components/Hero.jsx` |
| `Features`          | Showcases the key features of the application with descriptive cards.                                      | `src/components/Features.jsx` |
| `InteractiveDemo`   | A section allowing users to customize theme colors, font sizes, and text styles in real-time.            | `src/components/InteractiveDemo.jsx` |
| `UserInfo`          | Displays user information fetched from the Redux store, with a dropdown for selection.                     | `src/components/UserInfo.jsx` |
| `Showcase`          | Presents a gallery of project examples with images and tags.                                               | `src/components/Showcase.jsx` |
| `FeatureCard`       | A reusable card component for displaying individual features.                                              | `src/components/Features.jsx` |
| `ShowcaseItem`      | A reusable component for displaying individual items in the showcase gallery.                              | `src/components/Showcase.jsx` |

## Styling Conventions

*   **Global Styles:** `src/index.css` defines global CSS variables, font stacks, and basic element styling.
*   **Component-Specific Styles:** Each component can have its own CSS file (e.g., `UserInfo.css`) for scoped styles.
*   **Utility Classes:** Common styling patterns are applied directly in JSX using classes defined in `src/App.css`.
*   **CSS Variables:** Used extensively for theming and consistent styling (e.g., `--primary-color`, `--background-color`).
*   **Dark Mode:** Implemented via a `dark-mode` class on the `body` or relevant sections, toggled by a switch.
*   **Transitions and Animations:** Used judiciously to enhance user experience.

## State Management (Redux & Redux Saga)

*   **Redux:** Used for managing global application state, particularly user data.
    *   **Store:** Configured in `src/redux/store.js` using `configureStore` from Redux Toolkit.
    *   **Reducers:** Defined in `src/redux/reducer/user.reducer.js` and combined in `src/redux/rootReducer.js`.
    *   **Actions:** Defined in `src/redux/action/user.js`. Asynchronous actions use the `createAsyncActionType` helper for `_REQUEST`, `_SUCCESS`, and `_ERROR` suffixes.
    *   **Selectors:** Defined in `src/redux/selector/user.js` using `reselect` for efficient state access.
*   **Redux Saga:** Handles side effects, primarily for asynchronous API calls.
    *   **Sagas:** Defined in `src/redux/sagas/user.js` and orchestrated by `rootSaga.js`.
    *   **`takeLatest`:** Used to ensure only the latest dispatched action of a certain type is processed, preventing race conditions.

## Data Fetching Strategies

Data fetching is primarily handled by Redux Saga, which orchestrates API calls and dispatches actions to update the Redux store.

1.  **Triggering Fetch:** An action is dispatched (e.g., `GET_USERS._REQUEST`).
2.  **Saga Interception:** The corresponding saga watcher (`watchGetUsers`) intercepts this action.
3.  **API Call:** The saga calls the relevant API function (e.g., `getUsersApi` from `src/api/api.js`).
4.  **Dispatching Success/Error:**
    *   On successful data retrieval, a `_SUCCESS` action is dispatched with the fetched data as `payload`.
    *   On error, an `_ERROR` action is dispatched with the error message as `payload`.
5.  **Reducer Update:** The reducer listens for `_SUCCESS` or `_ERROR` actions and updates the Redux state accordingly.
6.  **Component Update:** Components subscribed to the Redux store (via `connect` or hooks) re-render with the updated data.

**Example:** Fetching users is initiated by dispatching `GET_USERS._REQUEST`. The `getUsers` saga calls `getUsersApi`, which fetches data from `src/assets/json/users.json`. The response is then put into the store via `GET_USERS._SUCCESS`.

## Code Conventions

*   **Component Naming:** PascalCase (e.g., `UserInfo`, `FeatureCard`).
*   **File Naming:** PascalCase for components (`ComponentName.jsx`), kebab-case for CSS (`component-name.css`).
*   **Imports:** Grouped by type: React, third-party libraries, local components, and styles.
*   **Props:** Use `PropTypes` for type checking and documentation.
*   **State:** Use `useState` for local component state and Redux for global state.
*   **Event Handlers:** Use camelCase (e.g., `handleClick`, `handleChange`).
*   **Constants:** Use `UPPER_SNAKE_CASE` for action types and constants.
*   **Comments:** Use JSDoc-style comments for functions and complex logic.
*   **Formatting:** Consistent indentation and spacing (e.g., 2 spaces).

## Testing

*   **Unit Tests:** (Not explicitly present in the provided code dump, but recommended) Components and utility functions should be tested using a framework like Jest and React Testing Library.
*   **Integration Tests:** Focus on how different parts of the application work together.
*   **End-to-End Tests:** (Not explicitly present) Tools like Cypress can be used for simulating user interactions.

---

This guideline serves as a starting point. As the project evolves, please contribute to its improvement by suggesting updates and additions.