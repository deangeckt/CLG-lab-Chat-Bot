import { useContext } from 'react';
import { AppContext } from '../AppContext';
import { useNavigate } from 'react-router-dom';

export function useApp() {
    const { state, setState } = useContext(AppContext);
    const navigate = useNavigate();

    const open_ending_modal = (text: string) => {
        const game_state = state.game_state;
        game_state.end = true;
        game_state.end_modal_text = text;
        setState({ ...state, game_state });
    };

    const navigate_to_end_page = () => {
        const path = '/survey';
        navigate(path);
    };

    const register_cb = (data: any) => {
        const game_config = state.game_config;
        const map_metadata = state.map_metadata;
        game_config.registerd = 'yes';

        if (data) {
            game_config.game_role = data.role;
            game_config.guid = data.guid;
            map_metadata.im_src = `${data.map_src}_${data.role}.jpg`;
        } else {
            console.warn('Server not connected - using mock bot mode');
            game_config.game_mode = 'bot';
        }
        let chat = [...state.chat];
        if (game_config.game_mode == 'bot') {
            chat = chat.concat([{ id: 1, msg: 'Welcome!', timestamp: Date.now() }]);
        }
        console.log(game_config);
        console.log(map_metadata);

        setState({ ...state, game_config, chat, map_metadata });
    };

    return { open_ending_modal, navigate_to_end_page, register_cb };
}
