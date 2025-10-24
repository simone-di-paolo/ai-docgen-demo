import React, { useEffect } from 'react';
import PropTypes from "prop-types";
import { connect } from "react-redux";
import { getUsers as getUsersSelector, getCurrentUser } from "../redux/selector/user";

import {
    GET_USER_INFO,
    GET_USERS
} from '../redux/action/user';

import './UserInfo.css'; // Importa il foglio di stile dedicato

// Ho mantenuto la tua struttura e ho solo aggiunto la nuova UI
function UserInfo({
    users,
    currentUser, // L'utente selezionato arriva direttamente dallo store
    getUserInfoById,
    getUsers
}) {

    // La tua logica Redux gestisce lo stato, quindi lo stato locale non serve più

    // Quando l'utente seleziona dal dropdown, usiamo la tua azione
    const handleUserSelection = (event) => {
        const userId = event.target.value;
        if (userId) {
            getUserInfoById(parseInt(userId, 10)); // Usiamo l'azione che hai creato
        }
    }

    useEffect(() => {
        if (!users || users.length === 0) {
            getUsers();
        }
    }, [getUsers, users])

    return (
        <>
            <div className="user-info-wrapper">
                <div className="user-info-selection">
                    <label htmlFor="user-select">Seleziona un Profilo</label>
                    {/* Il valore del select non è più controllato da uno stato locale */}
                    <select id="user-select" onChange={handleUserSelection} defaultValue="">
                        <option value="" disabled>-- Visualizza i dettagli di un utente --</option>
                        {users.map(user => (
                            <option key={user.id} value={user.id}>
                                {user.name} {user.surname}
                            </option>
                        ))}
                    </select>
                </div>

                {/* La UI ora dipende solo da 'currentUser' che arriva dalle props */}
                {currentUser ? (
                    <div className="user-card fade-in">
                        <div className="user-card-header">
                            <div className="user-avatar">{currentUser.name.charAt(0)}{currentUser.surname.charAt(0)}</div>
                            <h2>{currentUser.name} {currentUser.surname}</h2>
                            <p>{currentUser.job}</p>
                        </div>
                        <div className="user-card-body">
                            <div className="user-info-row">
                                <span>🎂</span>
                                <p><strong>Nato il:</strong> {new Date(currentUser.date_of_birth).toLocaleDateString('it-IT')}</p>
                            </div>
                            <div className="user-info-row">
                                <span>🎓</span>
                                <p><strong>Studi:</strong> {currentUser.studies}</p>
                            </div>
                            <div className="user-info-row">
                                <span>📍</span>
                                <p><strong>Indirizzi:</strong></p>
                            </div>
                            <ul className="address-list">
                                {currentUser.addresses.map((addr, index) => (
                                    <li key={index} className="address-item">
                                        <p><strong>{addr.type.charAt(0).toUpperCase() + addr.type.slice(1)}:</strong> {addr.street}, {addr.zip_code} {addr.city}</p>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </div>
                ) : (
                    <div className="user-info-placeholder">
                        <p>Seleziona un utente per vedere la magia!</p>
                    </div>
                )}
            </div>
        </>
    );
}

UserInfo.propTypes = {
    users: PropTypes.array.isRequired,
    currentUser: PropTypes.object, // Può essere null all'inizio
    getUserInfoById: PropTypes.func.isRequired,
    getUsers: PropTypes.func.isRequired,
}

const mapStateToProps = (state) => ({
    users: getUsersSelector(state),
    currentUser: getCurrentUser(state), // Mappiamo l'utente selezionato alle props
});

const mapDispatchToProps = (dispatch) => ({
    getUserInfoById: (id) => dispatch({type: GET_USER_INFO, id}), // la tua azione
    getUsers: () => dispatch({type: GET_USERS._REQUEST}),
});

export default connect(mapStateToProps, mapDispatchToProps)(UserInfo);