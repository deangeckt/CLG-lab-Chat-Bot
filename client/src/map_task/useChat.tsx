import { useContext, useState, useEffect, useRef } from 'react';
import { callBot, callHuman, huamn_to_human_event } from '../api';
import { AppContext } from '../AppContext';
import { useApp } from './useApp';
import { ChatMsg } from '../Wrapper';

export function useChat() {
    const { state, setState } = useContext(AppContext);
    const [inputTxt, setInputTxt] = useState('');
    const [botType, setBotType] = useState(false);
    const [otherMsg, setOtherMsg] = useState(false);
    const stateRef = useRef(state);
    const { open_ending_modal } = useApp();

    useEffect(() => {
        stateRef.current = state;
    }, [state]);

    useEffect(() => {
        if (state.game_config.game_mode != 'human') return;
        huamn_to_human_event(state.game_config.guid, addOtherHumanMsg);
    }, []);

    const updateChatState = (newMsg: ChatMsg) => {
        // const chat = [...stateRef.current.chat].concat([newMsg]);
        stateRef.current.chat.push(newMsg);
        console.log(stateRef.current.chat);
        console.log(stateRef.current.user_map_path);
        setState(stateRef.current);
    };

    const sendUserMsg = () => {
        if (!inputTxt) return;
        const selfChatMsg = { msg: inputTxt, id: state.game_config.game_role, timestamp: Date.now() };
        updateChatState(selfChatMsg);
        setInputTxt('');

        if (state.game_config.game_mode == 'bot') {
            setBotType(true);
            const curr_cell = state.user_map_path[state.user_map_path.length - 1];
            callBot(inputTxt, curr_cell, addBotMsg);
        } else {
            callHuman(state.game_config.guid, selfChatMsg);
        }
    };

    const addBotMsg = (msg: string) => {
        updateChatState({ msg: msg, id: 1 - state.game_config.game_role, timestamp: Date.now() });
        setBotType(false);
    };

    const addOtherHumanMsg = (guid: string, msg: ChatMsg, other_finished: boolean) => {
        if (state.game_config.guid !== guid) return;
        if (msg.id === state.game_config.game_role) return;
        if (other_finished) open_ending_modal('The other participant has finished the game');
        else {
            setOtherMsg(!otherMsg);
            updateChatState(msg);
        }
    };

    const onKeyPress = (e: any) => {
        if (e.keyCode == 13) {
            sendUserMsg();
        }
    };

    return { onKeyPress, botType, sendUserMsg, inputTxt, setInputTxt };
}
