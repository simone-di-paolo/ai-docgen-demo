import { combineReducers } from 'redux';
import { user } from './reducer/user.reducer';

const rootReducer = combineReducers({
  user,
});

export default rootReducer;
