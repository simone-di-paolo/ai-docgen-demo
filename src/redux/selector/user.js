import { createSelector } from 'reselect';

const userState = (state) => state.user;

export const getUsers = createSelector(
    userState,
    (state) => state?.users
);

// Aggiungo questo selettore per ottenere l'utente specifico che hai selezionato
export const getCurrentUser = createSelector(
    userState,
    (state) => state?.currentUser
);