import { useContext } from 'react';
import { AppContext } from './AppContext';
import { register } from './api';
import { maps } from './Wrapper';
import { bot_welcome_str } from './common/strings';

export function useRegister() {
    const { state, setState } = useContext(AppContext);

    const create_new_game = () => {
        return;
    };

    const register_game = (game_idx: number) => {
        const game_config = state.games[game_idx].game_config;
        register(game_config.map_index, game_config.game_role, register_cb);
        setState({ ...state, registerd: 'load' });
    };

    const register_cb = (data: any) => {
        const games = [...state.games];
        const game_config = games[0].game_config;
        const map_index = game_config.map_index;
        const map_metadata = maps[map_index];
        console.log(map_metadata);

        let server_version = '';
        let registerd = 'yes';

        if (data) {
            server_version = data.version;
            game_config.guid = data.guid;
            const map = map_metadata.im_src.split('_')[0];
            map_metadata.im_src = `${map}_${game_config.game_role}.jpg`;
        } else {
            registerd = 'err';
        }
        const chat = games[0].chat;
        chat.push({ id: 1 - game_config.game_role, msg: bot_welcome_str, timestamp: Date.now() });
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
