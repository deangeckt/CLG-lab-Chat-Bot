import React, { useContext } from 'react';
import { Box, Button, CircularProgress, Typography } from '@material-ui/core';
import { AppContext } from '../AppContext';
import { maps } from '../Wrapper';
import { bot_welcome_str } from '../common/strings';
import { useNavigate } from 'react-router-dom';
import { register } from '../api';
import Header from '../common/Header';
import { main_blue } from '../common/colors';
import './Consent.css';

function Conset(): JSX.Element {
    const { state, setState } = useContext(AppContext);
    const navigate = useNavigate();

    React.useEffect(() => {
        const game_config = state.game_config;
        if (game_config.registerd === 'yes') return;
        register(game_config.map_index, game_config.game_role, register_cb);

        game_config.registerd = 'load';
        setState({ ...state, game_config });
    }, []);

    const register_cb = (data: any) => {
        const game_config = state.game_config;
        const map_index = game_config.map_index;
        const map_metadata = maps[map_index];

        let server_version = '';
        game_config.registerd = 'yes';

        if (data) {
            server_version = data.version;
            game_config.guid = data.guid;
            const map = map_metadata.im_src.split('_')[0];
            map_metadata.im_src = `${map}_${game_config.game_role}.jpg`;
        } else {
            game_config.registerd = 'err';
        }
        let chat = [...state.chat];
        chat = chat.concat([{ id: 1 - state.game_config.game_role, msg: bot_welcome_str, timestamp: Date.now() }]);

        setState({
            ...state,
            game_config,
            chat,
            map_metadata,
            user_map_path: [maps[map_index].start_cell],
            server_version,
        });
    };

    const onClick = () => {
        setState({ ...state, consent: true });
        navigate('/general_survey');
    };

    const redner_conset = () => {
        return (
            <>
                <h6>text here</h6>
                <Button
                    className="register_btn"
                    style={{ textTransform: 'none' }}
                    variant="outlined"
                    color="primary"
                    onClick={() => onClick()}
                >
                    Accept
                </Button>
            </>
        );
    };

    return (
        <div className="conset">
            <Header />
            <div className="conset_container">
                {state.game_config.registerd === 'err' && (
                    <Typography variant="h5" style={{ margin: '16px' }}>
                        An errur occured, please try again later
                    </Typography>
                )}
                {state.game_config.registerd === 'yes' && redner_conset()}
                {state.game_config.registerd === 'load' && (
                    <Box sx={{ display: 'flex', margin: '32px' }}>
                        <CircularProgress style={{ color: main_blue, width: '30px', height: '30px' }} />
                    </Box>
                )}
            </div>
        </div>
    );
}

export default Conset;
