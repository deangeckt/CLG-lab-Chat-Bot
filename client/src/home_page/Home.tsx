import React from 'react';
import { Box, Button, CircularProgress, ImageList, ImageListItem } from '@material-ui/core';
import { Typography } from '@material-ui/core';
import { useContext } from 'react';
import { AppContext } from '../AppContext';
import Header from '../common/Header';
import Form from './Form';
import { main_blue } from '../common/colors';
import GameInstructionsDialog from '../common/GameInstructionsDialog';
import { useHome } from './useHome';
import { home_page_title1 } from '../common/strings';
import './Home.css';

function Home(): JSX.Element {
    const { state } = useContext(AppContext);
    const { set_register_state, map_chosen_click, filteredMaps } = useHome();

    return (
        <div className="Home">
            <Header />

            <div className="Home_Container">
                <Typography variant="h4" style={{ marginTop: '16px', marginBottom: '16px' }}>
                    {home_page_title1}
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
                            {filteredMaps.map((item, index) => (
                                <ImageListItem key={item.im_src} onClick={() => map_chosen_click(index)}>
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
                                onClick={() => set_register_state('bot')}
                            >
                                Chat with a bot
                            </Button>
                            <Button
                                className="register_btn"
                                style={{ textTransform: 'none' }}
                                variant="outlined"
                                color="primary"
                                onClick={() => set_register_state('human')}
                            >
                                Chat with a huamn
                            </Button>
                        </div>
                    </div>
                ) : null}
            </div>
        </div>
    );
}

export default Home;
