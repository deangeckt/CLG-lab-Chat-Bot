import { useContext, useState, useEffect, useRef } from 'react';
import { callBot } from '../api';
import { AppContext } from '../AppContext';
import { ChatMsg } from '../Wrapper';
import { hh_end_modal_str } from '../common/strings';

export function useChat() {
    const { state, setState } = useContext(AppContext);
    const [inputTxt, setInputTxt] = useState('');
    const [botType, setBotType] = useState(false);
    const stateRef = useRef(state);

    useEffect(() => {
        stateRef.current = state;
    }, [state]);

    const updateChatState = (newMsg: ChatMsg[]) => {
        const chat = [...stateRef.current.chat].concat(newMsg);
        setState({ ...stateRef.current, chat });
    };

    const updateChatAndFinish = (newMsg: ChatMsg[], endModalText: string) => {
        const game_state = state.game_state;
        game_state.end = true;
        game_state.end_modal_text = endModalText;
        const chat = [...stateRef.current.chat].concat(newMsg);
        setState({ ...stateRef.current, chat, game_state });
    };

    const sendUserMsg = () => {
        if (!inputTxt) return;
        const curr_cell = state.user_map_path[state.user_map_path.length - 1];

        const selfChatMsg: ChatMsg = {
            msg: inputTxt,
            id: state.game_config.game_role,
            timestamp: Date.now(),
            curr_nav_cell: curr_cell,
        };

        updateChatState([selfChatMsg]);
        setInputTxt('');

        setBotType(true);
        callBot(
            state.game_config.guid,
            inputTxt,
            curr_cell,
            state.map_metadata.map_idx,
            state.game_config.game_role,
            addBotMsg,
        );
    };

    const addBotMsg = (data: any) => {
        const msgs: string[] = data.res;
        const is_finish = data.is_finish;
        const chatMsgs = msgs.map((msg) => ({ msg: msg, id: 1 - state.game_config.game_role, timestamp: Date.now() }));
        setBotType(false);
        if (is_finish) updateChatAndFinish(chatMsgs, hh_end_modal_str);
        else updateChatState(chatMsgs);
    };

    const onKeyPress = (e: any) => {
        if (e.keyCode == 13) {
            sendUserMsg();
        }
    };

    return { updateChatState, onKeyPress, botType, sendUserMsg, inputTxt, setInputTxt };
}
