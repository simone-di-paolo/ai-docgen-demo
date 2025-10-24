import {
    put, 
    call, 
    takeLatest
} from 'redux-saga/effects';

import { 
    GET_USER_INFO,
    GET_USERS
} from '../action/user';

import {
   getUsers as getUsersApi
} from '../../api/api'

// === GET USERS ===

function* getUsers() { // Non c'è bisogno di destrutturare un oggetto vuoto qui
    try {
        const response = yield call(getUsersApi);
        
        // CORREZIONE: 'put' accetta un solo argomento, l'oggetto azione completo.
        yield put({ type: GET_USERS._SUCCESS, payload: response });

    } catch (error) {
        // CORREZIONE: Passiamo anche il messaggio di errore nel payload.
        yield put({ type: GET_USERS._ERROR, payload: error.message });
    }
}

function* watchGetUsers() {
    yield takeLatest(GET_USERS._REQUEST, getUsers);
}

export default [
    watchGetUsers
];