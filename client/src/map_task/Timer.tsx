import React, { useEffect } from 'react';
import { useTimer } from 'react-timer-hook';
import { useApp } from './useApp';
import { useContext } from 'react';
import { AppContext } from '../AppContext';
import './Timer.css';

function Timer(): JSX.Element {
    const { state, setState } = useContext(AppContext);
    const { open_ending_modal } = useApp();

    const init_time = state.game_state.end ? 0 : state.game_state.init_time;
    const expiryTimestamp = new Date();
    expiryTimestamp.setSeconds(expiryTimestamp.getSeconds() + init_time);

    const { seconds, minutes } = useTimer({
        expiryTimestamp,
        onExpire: () => {
            if (state.game_state.end) return;
            open_ending_modal('Time is up');
        },
    });

    useEffect(() => {
        if (!state.game_state.end) return;

        const total_seconds = minutes * 60 + seconds;
        const game_state = state.game_state;
        game_state.game_time = game_state.init_time - total_seconds;
        setState({ ...state, game_state });
    }, [state.game_state.end]);

    const right = seconds % 10;
    const left = Math.floor(seconds / 10);
    return (
        <div className="timer_wrapper">
            <span className="timer_digit">0</span>
            <span className="timer_digit">{minutes}</span>
            <span className="timer_space">:</span>
            <span className="timer_digit">{left}</span>
            <span className="timer_digit">{right}</span>
        </div>
    );
}

export default Timer;
