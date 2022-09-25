import { useContext, useState, useEffect, useRef } from 'react';
import { ChatMsg } from '../Wrapper';
import { callBot, callHuman, huamn_to_human_event } from '../api';
import { AppContext } from '../AppContext';

export function useChat() {
    const { state, setState } = useContext(AppContext);
    const [inputTxt, setInputTxt] = useState('');
    const [botType, setBotType] = useState(false);
    const chatRef = useRef(state.chat);

    useEffect(() => {
        chatRef.current = state.chat;
    }, [state.chat]);

    useEffect(() => {
        if (state.game_config.game_mode != 'human') return;
        huamn_to_human_event(addOtherHumanMsg);
    }, []);

    const updateChatState = (newMsg: ChatMsg) => {
        const chat = [...chatRef.current].concat([newMsg]);
        setState({ ...state, chat: chat });
    };

    const sendUserMsg = () => {
        if (!inputTxt) return;
        const selfChatMsg = { msg: inputTxt, id: state.game_config.game_role };
        updateChatState({ msg: inputTxt, id: state.game_config.game_role });
        setInputTxt('');

        if (state.game_config.game_mode == 'bot') {
            setBotType(true);
            const curr_cell = state.user_map_path[state.user_map_path.length - 1];
            callBot(inputTxt, curr_cell, addBotMsg);
        } else {
            callHuman(selfChatMsg);
        }
    };

    const addBotMsg = (msg: string) => {
        updateChatState({ msg: msg, id: 1 - state.game_config.game_role });
        setBotType(false);
    };

    const addOtherHumanMsg = (msg: string) => {
        const splited = msg.split('__');
        const id_ = Number(splited[0]);
        const otherMsg = splited[1];
        if (id_ != state.game_config.game_role) {
            updateChatState({ msg: otherMsg, id: id_ });
        }
    };

    const onKeyPress = (e: any) => {
        if (e.keyCode == 13) {
            sendUserMsg();
        }
    };

    return { onKeyPress, botType, sendUserMsg, inputTxt, setInputTxt };
}
