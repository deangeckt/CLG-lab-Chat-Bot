import { useContext } from 'react';
import { AppContext } from '../AppContext';
import { gameMode, gameRegister } from '../Wrapper';
import { register } from '../api';
import { useApp } from '../map_task/useApp';

export function useHome() {
    const { state, setState } = useContext(AppContext);
    const { register_cb } = useApp();

    const map_chosen_click = (map_index: number) => {
        set_register_state(state.game_config.game_mode!, 'load');
        register(state.game_config.game_mode!, register_cb, map_index);
    };

    const set_register_state = (m: gameMode, r: gameRegister = 'fill_details') => {
        const game_config = state.game_config;
        game_config.registerd = r;
        game_config.game_mode = m;
        setState({ ...state, game_config });
    };

    return { map_chosen_click, set_register_state };
}
