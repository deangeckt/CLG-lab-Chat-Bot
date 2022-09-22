import React from 'react';
import { useTimer } from 'react-timer-hook';
import { useApp } from './useApp';
import { useContext } from 'react';
import { AppContext } from '../AppContext';
import './Timer.css';

function Timer(): JSX.Element {
    const { state } = useContext(AppContext);
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
