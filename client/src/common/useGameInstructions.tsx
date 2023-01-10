import { useContext } from 'react';
import { AppContext } from '../AppContext';

export function useGameInstructions() {
    const { state, setState } = useContext(AppContext);

    const setGameInstructions = (val: boolean) => {
        const game_state = state.game_state;
        game_state.open_instructions = val;
        game_state.started = true;
        setState({ ...state, game_state });
    };

    return { setGameInstructions };
}
