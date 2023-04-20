import React, { useContext } from 'react';
import { Button, IconButton, Typography } from '@material-ui/core';
import { AppContext } from '../AppContext';
import { maps } from '../Wrapper';
import { bot_welcome_str } from '../common/strings';
import { useNavigate } from 'react-router-dom';
import { register } from '../api';
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
            map_metadata.im_src = `${map}_${data.role}.jpg`;
        } else {
            game_config.registerd = 'err';
        }
        let chat = [...state.chat];
        chat = chat.concat([{ id: 1 - state.game_config.game_role, msg: bot_welcome_str, timestamp: Date.now() }]);

        console.log(game_config);

        setState({
            ...state,
            game_config,
            chat,
            map_metadata,
            user_map_path: [maps[map_index].start_cell],
            server_version,
        });
        if (game_config.registerd != 'err') navigate('/general_survey');
    };

    return (
        <div className="Conset">
            {state.game_config.registerd === 'err' && <h6>err</h6>}
            {state.game_config.registerd === 'yes' && <h6>consent stuff</h6>}
            {state.game_config.registerd === 'load' && <h6>loading...</h6>}
        </div>
    );
}

export default Conset;
