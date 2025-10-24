export const getUsers = () => {
    return fetch('src/assets/json/users.json')
        .then(response => {
            if (!response.ok) {
                throw new Error('Errore nel caricamento del file users.json');
            }
            return response.json();
        });
};
