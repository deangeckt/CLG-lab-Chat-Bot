import { useContext } from 'react';
import { AppContext } from '../AppContext';
import { useNavigate } from 'react-router-dom';
import { maps } from '../Wrapper';
import { bot_welcome_str, finish_btn_modal_str } from '../common/strings';

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
        open_ending_modal(finish_btn_modal_str);
    };

    const navigate_to_end_page = () => {
        const path = '/map_survey';
        navigate(path);
    };

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
        navigate('/map_task');
        //TODO: TMP
        // if (game_config.registerd != 'err') navigate('/map_task');
    };

    return { open_ending_modal, navigate_to_end_page, register_cb, finish_early };
}
