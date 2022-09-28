import React from 'react';
import MapCanvas from './MapCanvas';
import Chat from './Chat';
import { IconButton, Typography } from '@material-ui/core';
import Timer from './Timer';
import { useContext } from 'react';
import { AppContext } from '../AppContext';
import Header from '../common/Header';
import { role_strings } from '../Wrapper';
import GameEndDialog from './GameEndDialog';
import InfoIcon from '@material-ui/icons/Info';
import { main_gray } from '../common/colors';
import GameInstructionsDialog from '../common/GameInstructionsDialog';
import { useGameInstructions } from '../common/useGameInstructions';
import './App.css';

function App(): JSX.Element {
    const { state } = useContext(AppContext);
    const { setGameInstructions } = useGameInstructions();

    const role_string = role_strings[state.game_config.game_role];

    return (
        <div className="App">
            <Header />
            <GameEndDialog />
            <GameInstructionsDialog />

            <div className="App_Header">
                <IconButton onClick={() => setGameInstructions(true)}>
                    <InfoIcon style={{ color: main_gray, fontSize: 40 }} />
                </IconButton>
                <Typography variant="h4" style={{ alignSelf: 'center' }}>
                    Your role: {role_string}
                </Typography>
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
