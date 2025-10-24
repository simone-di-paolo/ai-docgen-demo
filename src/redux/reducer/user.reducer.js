import { GET_USERS, GET_USER_INFO } from '../action/user';

const initialState = {
    users: [],
    error: null,
    loading: false,
};
  
export const user = (state = initialState, action) => {
    switch (action.type) {
        
        case GET_USERS._REQUEST: {
            return {
                ...state,
                loading: true,
                error: null,
            }
        }

        case GET_USERS._SUCCESS: {
            const {
                payload
            } = action;

            return {
                ...state,
                loading: false,
                users: payload
            }
        }

        // Gestione dell'errore
        case GET_USERS._ERROR: {
            return {
                ...state,
                loading: false,
                error: action.payload
            }
        }

        case GET_USER_INFO: {
            const {
                id
            } = action;

            return {
                ...state,
                currentUser: state.users.find((user) => user?.id === id)
            }
        }
        
        default: 
            return state;

    }
};