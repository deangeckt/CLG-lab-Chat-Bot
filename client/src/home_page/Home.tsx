import React from 'react';
import { Box, Button, CircularProgress } from '@material-ui/core';
import { Typography } from '@material-ui/core';
import { useContext } from 'react';
import { AppContext } from '../AppContext';
import { gameMode } from '../Wrapper';
import Header from '../common/Header';
import { useApp } from '../map_task/useApp';
import { register } from '../api';
import Form from './Form';
import { main_blue } from '../common/colors';
import './Home.css';
import GameInstructionsDialog from '../common/GameInstructionsDialog';

function Home(): JSX.Element {
    const { state, setState } = useContext(AppContext);
    const { register_cb } = useApp();

    const register_click = (mode: gameMode) => {
        const game_config = state.game_config;
        game_config.registerd = 'load';
        game_config.game_mode = mode;
        setState({ ...state, game_config });
        register(mode, register_cb);
    };

    return (
        <div className="Home">
            <Header />

            <div className="Home_Container">
                <Typography variant="h4" style={{ marginTop: '16px' }}>
                    Welcome to CLG map task
                </Typography>
                {state.game_config.registerd == 'yes' ? <Form /> : null}
                {state.game_config.registerd == 'yes' ? <GameInstructionsDialog /> : null}

                {state.game_config.registerd == 'load' ? (
                    <Box sx={{ display: 'flex', margin: '16px' }}>
                        <CircularProgress style={{ color: main_blue, width: '30px', height: '30px' }} />
                    </Box>
                ) : null}
                {state.game_config.registerd == 'no' ? (
                    <div style={{ width: '50%', marginTop: '16px' }}>
                        <Typography variant="h5" style={{ margin: '16px' }}>
                            Choose game mode
                        </Typography>
                        <div className="home_Register">
                            <Button
                                className="register_btn"
                                style={{ textTransform: 'none' }}
                                variant="outlined"
                                color="primary"
                                onClick={() => register_click('bot')}
                            >
                                Bot
                            </Button>
                            <Button
                                className="register_btn"
                                style={{ textTransform: 'none' }}
                                variant="outlined"
                                color="primary"
                                onClick={() => register_click('human')}
                            >
                                Human
                            </Button>
                        </div>
                    </div>
                ) : null}
            </div>
        </div>
    );
}

export default Home;
