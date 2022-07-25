/* eslint-disable react/react-in-jsx-scope */
import MapCanvas from './map_task/MapCanvas';
import Chat from './map_task/Chat';
import './App.css';

function App(): JSX.Element {
    return (
        <div className="App">
            <div className="Container">
                <MapCanvas im_width={1413} im_height={1052} im_name={'map1.png'} />
                <Chat />
            </div>
        </div>
    );
}

export default App;
