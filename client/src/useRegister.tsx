import { useContext } from 'react';
import { AppContext } from './AppContext';
import { register } from './api';
import { maps, ISingleGameState, init_game_state, init_map_survey } from './Wrapper';
import { bot_welcome_str } from './common/strings';
import { useNavigate } from 'react-router-dom';
const game_role = 1;

export function useRegister() {
    const { state, setState } = useContext(AppContext);
    const navigate = useNavigate();

    const new_game_cb = (data: any) => {
        const games = [...state.games];
        const map_idx = state.curr_game + 1;

        const map_metadata = { ...maps[map_idx] };
        const map = map_metadata.im_src.split('_')[0];
        map_metadata.im_src = `${map}_${game_role}.jpg`;

        const new_game: ISingleGameState = {
            chat: [{ id: 1 - game_role, msg: bot_welcome_str, timestamp: Date.now() }],
            map_metadata: map_metadata,
            game_state: { ...init_game_state },
            map_survey: { ...init_map_survey },
            user_map_path: [maps[map_idx].start_cell],
            game_config: { game_role: game_role, map_index: map_idx, guid: data.guid },
        };
        games.push(new_game);

        setState({
            ...state,
            games: games,
            curr_game: state.curr_game + 1,
            registerd: 'yes',
        });
        navigate('/map_task');
    };

    const create_new_game = () => {
        setState({ ...state, registerd: 'load' });
        register(state.curr_game + 1, game_role, new_game_cb);
    };

    const register_game = (game_idx: number) => {
        const game_config = state.games[game_idx].game_config;
        setState({ ...state, registerd: 'load' });
        register(game_config.map_index, game_config.game_role, register_cb);
    };

    const register_cb = (data: any) => {
        const games = [...state.games];
        const game_config = games[0].game_config;
        const map_index = game_config.map_index;
        const map_metadata = maps[map_index];

        let server_version = '';
        let registerd = 'yes';

        if (data) {
            server_version = data.version;
            game_config.guid = data.guid;
            const map = map_metadata.im_src.split('_')[0];
            map_metadata.im_src = `${map}_${game_role}.jpg`;
        } else {
            registerd = 'err';
        }
        const chat = games[0].chat;
        chat.push({ id: 1 - game_role, msg: bot_welcome_str, timestamp: Date.now() });
        games[0].chat = chat;
        games[0].map_metadata = map_metadata;
        games[0].user_map_path = [maps[map_index].start_cell];

        setState({
            ...state,
            games: games,
            registerd,
            server_version,
        });
    };

    return { register_game, create_new_game };
}
