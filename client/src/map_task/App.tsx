/* eslint-disable react/react-in-jsx-scope */
import MapCanvas from './MapCanvas';
import Chat from './Chat';
import { Typography } from '@material-ui/core';
import './App.css';

function App(): JSX.Element {
    return (
        <div className="App">
            <Typography variant="h5">CLG lab - Chat Bot 1.0</Typography>
            <div className="App_Container">
                <MapCanvas />
                <Chat />
            </div>
        </div>
    );
}

export default App;
