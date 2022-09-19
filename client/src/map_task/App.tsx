/* eslint-disable react/react-in-jsx-scope */
import MapCanvas from './MapCanvas';
import Chat from './Chat';
import './App.css';
import { Typography } from '@material-ui/core';

function App(): JSX.Element {
    return (
        <div className="App">
            <Typography variant="h5">CLG lab - Chat Bot 1.0</Typography>
            <div className="App_Container">
                <MapCanvas im_width={1413} im_height={1052} im_name={'map1.png'} />
                <Chat />
            </div>
        </div>
    );
}

export default App;
