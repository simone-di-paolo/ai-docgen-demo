const initialState = {
  value: 0,
};

const counterReducer = (state = initialState, action) => {
  switch (action.type) {
    case 'counter/increment':
      return { ...state, value: state.value + 1 };
    case 'counter/decrement':
      return { ...state, value: state.value - 1 };
    case 'counter/incrementByAmount':
      return { ...state, value: state.value + action.payload };
    default:
      return state;
  }
};

export default counterReducer;
