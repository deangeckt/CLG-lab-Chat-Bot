/* eslint-disable react/react-in-jsx-scope */
import MapCanvas from './MapCanvas';
import Chat from './Chat';
import { Typography } from '@material-ui/core';
import Timer from './Timer';
import './App.css';

function App(): JSX.Element {
    return (
        <div className="App">
            <div className="App_Header">
                <Typography variant="h5" style={{ alignSelf: 'center', width: '50%' }}>
                    CLG lab - Chat Bot 1.0
                </Typography>
                <Timer />
            </div>
            <div className="App_Container">
                <MapCanvas />
                <Chat />
            </div>
        </div>
    );
}

export default App;
