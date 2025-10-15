export const increment = () => ({ type: 'counter/increment' });
export const decrement = () => ({ type: 'counter/decrement' });
export const incrementByAmount = (amount) => ({ type: 'counter/incrementByAmount', payload: amount });
