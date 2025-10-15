import { useSelector, useDispatch } from 'react-redux';
import { increment, decrement } from './redux/action/counterActions';
import { selectCount } from './redux/selector/counterSelector';
import './App.css';

function App() {
  const count = useSelector(selectCount);
  const dispatch = useDispatch();

  return (
    <div className='App'>
      <header className='App-header'>
        <h1>Redux Counter</h1>
        <p>Count: {count}</p>
        <button onClick={() => dispatch(increment())}>Increment</button>
        <button onClick={() => dispatch(decrement())}>Decrement</button>
      </header>
    </div>
  );
}

export default App;
