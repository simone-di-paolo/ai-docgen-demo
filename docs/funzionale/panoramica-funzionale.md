# AI DocGen Demo v2 - Functional Overview

This document provides a functional overview of the AI DocGen Demo v2 application, detailing its user-facing features, underlying mechanics, and typical user flows.

## Product Description

AI DocGen Demo v2 is a modern web application showcasing interactive components, dynamic styling, and AI-driven documentation capabilities. It leverages React for its frontend architecture and Redux for state management, with Redux Saga handling asynchronous operations. The application aims to provide a visually appealing and interactive experience, demonstrating how AI can assist in generating and updating documentation.

## User Features

The application offers the following user-facing features:

1.  **Interactive Hero Section:**
    *   A prominent hero section with a captivating title and subtitle.
    *   A call-to-action button that smoothly scrolls the user to the interactive demo section.

2.  **Feature Showcase:**
    *   Highlights the core functionalities of the application through visually distinct feature cards.
    *   Each card displays an icon, title, and a brief description of a feature.

3.  **Interactive Demo & Customization:**
    *   A central section allowing users to customize various aspects of a demo card in real-time.
    *   **Theme Color Picker:** Users can select a primary color that dynamically updates the theme of the demo card and its elements.
    *   **Font Size Slider:** Adjusts the font size of the demo card's text content.
    *   **Font Family Selector:** Allows users to choose from a predefined list of font families for the demo card.
    *   **Dark/Light Mode Toggle:** Switches the application's theme between a dark and light mode, affecting the overall appearance.
    *   **Text Area Editor:**
        *   Users can input or modify text that will be displayed in the demo card's description.
        *   **Character and Word Count:** Displays the current character and word count of the text area.
        *   **Text Transformation Buttons:**
            *   **Uppercase:** Converts all text to uppercase.
            *   **Lowercase:** Converts all text to lowercase.
            *   **Capitalize:** Capitalizes the first letter of each word.
            *   **Underline:** Toggles an underline effect on the text.
        *   **Text Alignment Buttons:** Aligns the text within the demo card to the left, center, or right.
    *   **Reset Button:** Resets all customization options to their default values.

4.  **User Profile Viewer:**
    *   A section to select and view detailed profiles of predefined users.
    *   **User Selection Dropdown:** A dropdown menu populated with available user names.
    *   **User Profile Card:** Displays the selected user's avatar, name, job title, date of birth, studies, and addresses.

5.  **Project Showcase:**
    *   A visually rich grid displaying examples of past projects.
    *   Each project item features an image, title, and associated tags.
    *   Hovering over a project reveals an overlay with the title and tags.

6.  **Footer:**
    *   Displays the application version and the AI model used for generation.

## How the Product Works

The application is built using a component-based architecture in React.

*   **State Management:** Redux is used to manage the global state of the application, particularly for user data and asynchronous operations. Redux Saga handles side effects like fetching user data.
*   **Dynamic Styling:** CSS variables and inline styles are extensively used to apply dynamic changes to the UI based on user interactions (e.g., theme color, font size).
*   **Component Reusability:** Features like `FeatureCard`, `ShowcaseItem`, and `PreviewCard` are designed as reusable components.
*   **Data Fetching:** User data is fetched from a local JSON file (`users.json`) using an API service and processed through Redux Sagas.
*   **Interactive Elements:** User interactions (button clicks, input changes) trigger state updates, which in turn re-render components with the new visual configurations.

## User Flows

### 1. Initial Landing and Exploration

This flow describes a user's first interaction with the application.

```mermaid
graph TD
    A[User lands on the homepage] --> B{Views Hero Section};
    B --> C[Reads Hero Title and Subtitle];
    C --> D{Sees "Inizia Ora" button};
    D -- Clicks "Inizia Ora" --> E[Scrolls to Interactive Demo Section];
    E --> F{Explores Interactive Demo Controls};
    F -- Adjusts Theme Color --> G[Sees Demo Card update instantly];
    F -- Changes Font Size --> G;
    F -- Toggles Dark/Light Mode --> H[App theme changes];
    F -- Edits Text Area --> I[Sees Text Area and Demo Card update];
    F -- Clicks Reset --> J[All demo customizations revert to default];
    E --> K{Navigates to User Profile Viewer};
    K --> L[Sees User Selection Dropdown];
    L -- Selects a User --> M[User Profile Card displays details];
    M --> N{Explores Project Showcase};
    N --> O[Hovers over project items to see details];
    O --> P[Scrolls to Footer];
```

### 2. User Profile Selection

This flow details how a user selects and views different user profiles.

```mermaid
graph TD
    A[User is on the page] --> B{Locates User Profile Viewer Section};
    B --> C[Sees "Seleziona un Profilo" label and dropdown];
    C --> D[Clicks on the dropdown];
    D --> E[Dropdown expands showing list of names];
    E -- Selects a User (e.g., "Mario Rossi") --> F[Dropdown closes, selected name shown];
    F --> G[User Profile Card appears/updates];
    G --> H[Displays details for "Mario Rossi"];
    H --> I{User wants to see another profile};
    I --> D;
    D -- Selects another User (e.g., "Giulia Bianchi") --> F;
    F --> G;
    G --> J[Displays details for "Giulia Bianchi"];
    J --> K[User can also see placeholder if no user is selected];
```

### 3. Interactive Demo Customization

This flow focuses on a user interacting with the customization controls in the "Interactive Demo" section.

```mermaid
graph TD
    A[User is viewing the Interactive Demo section] --> B{Sees the Demo Card and Controls};
    B --> C[Interacts with Color Picker];
    C --> D[Theme Color updates on Demo Card];
    B --> E[Interacts with Font Size Slider];
    E --> F[Font Size updates on Demo Card];
    B --> G[Interacts with Font Family Selector];
    G --> H[Font Family updates on Demo Card];
    B --> I[Toggles Dark/Light Mode Switch];
    I --> J[Overall app theme and Demo Card appearance change];
    B --> K[Interacts with Text Area];
    K --> L[Text Area content updates];
    L --> M[Character and Word Count update];
    K --> N[Edits text];
    N --> O[Demo Card's Preview Text updates];
    B --> P[Clicks Text Transformation Button (e.g., Uppercase)];
    P --> Q[Text in Text Area and Demo Card changes to Uppercase];
    B --> R[Clicks Text Alignment Button (e.g., Center)];
    R --> S[Text in Demo Card is centered];
    B --> T[Clicks Reset Button];
    T --> U[All Demo customizations revert to default state];
```