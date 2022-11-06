import React from 'react';
import { Box, Button, CircularProgress, ImageList, ImageListItem } from '@material-ui/core';
import { Typography } from '@material-ui/core';
import { useContext } from 'react';
import { AppContext } from '../AppContext';
import { gameMode, gameRegister, maps } from '../Wrapper';
import Header from '../common/Header';
import { useApp } from '../map_task/useApp';
import { register } from '../api';
import Form from './Form';
import { main_blue } from '../common/colors';
import GameInstructionsDialog from '../common/GameInstructionsDialog';
import './Home.css';

function Home(): JSX.Element {
    const { state, setState } = useContext(AppContext);
    const { register_cb } = useApp();

    const register_click = (mode: gameMode, map_index: number) => {
        set_register_state('load', mode);
        register(mode, register_cb, map_index);
    };

    const set_register_state = (r: gameRegister, m: gameMode) => {
        const game_config = state.game_config;
        game_config.registerd = r;
        game_config.game_mode = m;
        setState({ ...state, game_config });
    };

    return (
        <div className="Home">
            <Header />

            <div className="Home_Container">
                <Typography variant="h4" style={{ marginTop: '16px', marginBottom: '16px' }}>
                    Welcome to CLG map task
                </Typography>
                {state.game_config.registerd == 'yes' ? <Form /> : null}
                {state.game_config.registerd == 'err' ? (
                    <Typography variant="h5" style={{ margin: '16px' }}>
                        An errur occured, please try again later
                    </Typography>
                ) : null}

                {state.game_config.registerd == 'yes' ? <GameInstructionsDialog /> : null}
                {state.game_config.registerd == 'load' ? (
                    <Box sx={{ display: 'flex', margin: '32px' }}>
                        <CircularProgress style={{ color: main_blue, width: '30px', height: '30px' }} />
                    </Box>
                ) : null}
                {state.game_config.registerd == 'choose_map' ? (
                    <>
                        <Typography variant="h5" style={{ margin: '16px' }}>
                            Choose map
                        </Typography>
                        <ImageList cols={2} rowHeight={400}>
                            {maps.map((item, index) => (
                                <ImageListItem key={item.im_src} onClick={() => register_click('human', index)}>
                                    <img src={require(`../map_task/maps/${item.im_src}`)} loading="lazy" />
                                </ImageListItem>
                            ))}
                        </ImageList>
                    </>
                ) : null}
                {state.game_config.registerd == 'no' ? (
                    <div style={{ width: '50%' }}>
                        <Typography variant="h5" style={{ margin: '16px' }}>
                            Choose game mode
                        </Typography>
                        <div className="home_Register">
                            <Button
                                className="register_btn"
                                style={{ textTransform: 'none' }}
                                variant="outlined"
                                color="primary"
                                onClick={() => register_click('bot', 0)}
                            >
                                Bot
                            </Button>
                            <Button
                                className="register_btn"
                                style={{ textTransform: 'none' }}
                                variant="outlined"
                                color="primary"
                                onClick={() => set_register_state('choose_map', 'human')}
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
