/* eslint-disable react/react-in-jsx-scope */
import { useTimer } from 'react-timer-hook';
import './Timer.css';

function Timer(): JSX.Element {
    const expiryTimestamp = new Date();
    expiryTimestamp.setSeconds(expiryTimestamp.getSeconds() + 300);

    const { seconds, minutes } = useTimer({
        expiryTimestamp,
        onExpire: () => console.warn('onExpire called'),
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
