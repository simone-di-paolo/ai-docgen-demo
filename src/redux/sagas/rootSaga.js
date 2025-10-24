import { all, fork } from 'redux-saga/effects';
import user from './user';

const sagas = [
  ...user,
];

export default function* rootSaga() {
  yield all(sagas.map(saga => fork(saga)));
}
