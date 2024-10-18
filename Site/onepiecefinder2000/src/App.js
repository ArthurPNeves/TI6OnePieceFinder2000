import './App.css';
import WantedPoster from './components/WantedPoster.tsx';
import Handler from './components/Handler.tsx';

function App() {
  return (
    <>
    <Handler />
    <div className='app-background'>
        <WantedPoster />
    </div>
    </>
  );
}

export default App;
