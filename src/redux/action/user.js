import { createAsyncActionType } from '../helper/createAsyncActionType';

export const GET_USER_INFO = '@@v01/user/GET_USER_INFO';
export const GET_USERS = createAsyncActionType('v01/user','GET_USERS');