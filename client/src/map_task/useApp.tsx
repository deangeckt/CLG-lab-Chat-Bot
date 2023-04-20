import React, { useContext, useEffect } from 'react';
import { AppContext } from '../AppContext';
import { useNavigate } from 'react-router-dom';
import { finish_btn_modal_str } from '../common/strings';

export function useApp() {
    const { state, setState } = useContext(AppContext);
    const navigate = useNavigate();

    useEffect(() => {
        if (!state.consent) navigate('/');
    }, []);

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
        navigate('/map_survey');
    };

    return { open_ending_modal, navigate_to_end_page, finish_early };
}
