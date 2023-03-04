import { useContext, useState, useEffect, useRef } from 'react';
import { callBot, callHuman, huamn_to_human_event } from '../api';
import { AppContext } from '../AppContext';
import { useApp } from './useApp';
import { ChatMsg } from '../Wrapper';
import { hh_end_modal_str } from '../common/strings';

export function useChat() {
    const { state, setState } = useContext(AppContext);
    const [inputTxt, setInputTxt] = useState('');
    const [botType, setBotType] = useState(false);
    const stateRef = useRef(state);
    const { open_ending_modal } = useApp();

    useEffect(() => {
        stateRef.current = state;
    }, [state]);

    useEffect(() => {
        if (state.game_config.game_mode != 'human') return;
        huamn_to_human_event(state.game_config.guid, addOtherHumanMsg);
    }, []);

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

        if (state.game_config.game_mode == 'bot') {
            setBotType(true);
            const curr_cell = state.user_map_path[state.user_map_path.length - 1];
            callBot(
                state.game_config.guid,
                inputTxt,
                curr_cell,
                state.map_metadata.map_idx,
                state.game_config.game_role,
                addBotMsg,
            );
        } else {
            callHuman(state.game_config.guid, selfChatMsg);
        }
    };

    const addBotMsg = (data: any) => {
        const msgs: string[] = data.res;
        const is_finish = data.is_finish;
        const chatMsgs = msgs.map((msg) => ({ msg: msg, id: 1 - state.game_config.game_role, timestamp: Date.now() }));
        setBotType(false);
        if (is_finish) updateChatAndFinish(chatMsgs, hh_end_modal_str);
        else updateChatState(chatMsgs);
    };

    const addOtherHumanMsg = (guid: string, msg: ChatMsg, other_finished: boolean) => {
        if (state.game_config.guid !== guid) return;
        if (msg.id === state.game_config.game_role) return;
        if (other_finished) {
            localStorage.setItem('state', JSON.stringify(stateRef.current));
            open_ending_modal(hh_end_modal_str);
        } else updateChatState([msg]);
    };

    const onKeyPress = (e: any) => {
        if (e.keyCode == 13) {
            sendUserMsg();
        }
    };

    return { updateChatState, onKeyPress, botType, sendUserMsg, inputTxt, setInputTxt };
}
