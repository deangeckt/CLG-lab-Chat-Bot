import { useContext } from 'react';
import { AppContext } from '../AppContext';
import { useNavigate } from 'react-router-dom';
import { notifyHumanEnd } from '../api';
import { maps } from '../Wrapper';

export function useApp() {
    const { state, setState } = useContext(AppContext);
    const navigate = useNavigate();

    const open_ending_modal = (text: string) => {
        const game_state = state.game_state;
        game_state.end = true;
        game_state.end_modal_text = text;
        setState({ ...state, game_state });
    };

    const finish_early = () => {
        if (state.game_config.game_mode == 'human') {
            notifyHumanEnd(state.game_config.guid, state.game_config.game_role);
            navigate_to_end_page();
        } else {
            open_ending_modal('Please add you final review new page');
        }
    };

    const navigate_to_end_page = () => {
        const path = '/survey';
        navigate(path);
    };

    const register_cb = (data: any, map_index: number) => {
        const map_metadata = maps[map_index];
        const game_config = state.game_config;
        game_config.registerd = 'yes';

        if (data) {
            game_config.game_role = data.role;
            game_config.guid = data.guid;
            const map = map_metadata.im_src.split('_')[0];
            map_metadata.im_src = `${map}_${data.role}.jpg`;
        } else {
            console.warn('Server not connected - using mock bot mode');
            game_config.game_mode = 'bot';
        }
        let chat = [...state.chat];
        if (game_config.game_mode == 'bot') {
            chat = chat.concat([{ id: 1, msg: 'Welcome!', timestamp: Date.now() }]);
        }
        console.log(game_config);

        setState({
            ...state,
            game_config,
            chat,
            map_metadata,
            user_map_path: [maps[map_index].start_cell],
        });
    };

    return { open_ending_modal, navigate_to_end_page, register_cb, finish_early };
}
