import React, { useContext, useState } from 'react';
import { AppContext } from '../AppContext';
import { ChatFeed, Message } from 'react-chat-ui';
import { IconButton, TextField } from '@material-ui/core';
import SendIcon from '@material-ui/icons/Send';
import './Chat.css';
import { callBot } from '../api';

function Chat(): JSX.Element {
    const { state, setState } = useContext(AppContext);
    const [currMsg, setCurrMsg] = useState('');
    const [botType, setBotType] = useState(false);

    const updateChatState = (newMsg: Message[]) => {
        const chat = [...state.chat].concat(newMsg);
        setState({ ...state, chat: chat });
    };

    const addUserMsg = () => {
        if (!currMsg) return;
        updateChatState([new Message({ message: currMsg, id: 0 })]);
        setCurrMsg('');
        setBotType(true);
        callBot(currMsg, addBotMsg);
    };
    // very ugly workaround!
    const addBotMsg = (msg: string) => {
        updateChatState([new Message({ message: currMsg, id: 0 }), new Message({ message: msg, id: 1 })]);
        setBotType(false);
    };

    const onKeyPress = (e: any) => {
        if (e.keyCode == 13) {
            addUserMsg();
        }
    };

    return (
        <div className="chat_container">
            <ChatFeed
                messages={state.chat}
                isTyping={botType}
                bubbleStyles={{
                    text: {
                        fontSize: 18,
                    },
                    chatbubble: {
                        borderRadius: 50,
                        padding: 10,
                    },
                }}
            />
            <div className="input_panel">
                <TextField
                    style={{ width: '90%' }}
                    variant="outlined"
                    value={currMsg}
                    placeholder={'Type here'}
                    onChange={(e) => setCurrMsg(e.target.value)}
                    onKeyDown={(e) => onKeyPress(e)}
                />
                <IconButton color="primary" size="medium" onClick={addUserMsg}>
                    <SendIcon />
                </IconButton>
            </div>
        </div>
    );
}

export default Chat;
