import { configureStore } from '@reduxjs/toolkit';
import createSagaMiddleware from 'redux-saga';
import rootReducer from './rootReducer';
import rootSaga from './sagas/rootSaga';

const sagaMiddleware = createSagaMiddleware();

export const store = configureStore({
  reducer: rootReducer,
  // Disabilitiamo i check di immutabilità e serializzabilità che sono
  // incompatibili con alcuni effetti di Redux Saga.
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({ 
      immutableCheck: false, 
      serializableCheck: false 
    }).concat(sagaMiddleware),
});

sagaMiddleware.run(rootSaga);
