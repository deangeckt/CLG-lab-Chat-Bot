import React from 'react';
import MapCanvas from './MapCanvas';
import Chat from './Chat';
import { Typography } from '@material-ui/core';
import Timer from './Timer';
import { useContext } from 'react';
import { AppContext } from '../AppContext';
import Header from '../common/Header';
import { role_strings } from '../Wrapper';
import GameEndDialog from './GameEndDialog';
import './App.css';

function App(): JSX.Element {
    const { state } = useContext(AppContext);
    const role_string = role_strings[state.game_config.game_role];

    return (
        <div className="App">
            <Header />
            <GameEndDialog />

            <div className="App_Header">
                <Typography variant="h4">Your role: {role_string}</Typography>
                {state.game_config.game_mode == 'bot' ? <Timer /> : null}
            </div>
            <div className="App_Container">
                <MapCanvas />
                <Chat />
            </div>
        </div>
    );
}

export default App;
