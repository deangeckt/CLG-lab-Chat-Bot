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
        const path = `survey`;
        navigate(path);
    };

    return { open_ending_modal, navigate_to_end_page };
}
