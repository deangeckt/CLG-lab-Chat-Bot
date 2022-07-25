import React, { useContext, useState } from 'react';
import { AppContext } from '../AppContext';
import { ChatFeed, Message } from 'react-chat-ui';
import { IconButton, TextField } from '@material-ui/core';
import SendIcon from '@material-ui/icons/Send';
import './Chat.css';

const messages_mock = [
    new Message({
        id: 1,
        message: "I'm the recipient! (The person you're talking to fsf sf sf sf sf sf sfsf sf sf )",
    }),
    new Message({ id: 0, message: "I'm you -- the blue bubble!" }),
];

function Chat(): JSX.Element {
    const { state, setState } = useContext(AppContext);
    const [currMsg, setCurrMsg] = useState('');
    const [messages, setMessages] = useState(messages_mock);

    const submitMsg = () => {
        if (!currMsg) return;
        console.log('msg:', currMsg);
        setCurrMsg('');
        const newMsg = new Message({ id: 0, message: currMsg });
        setMessages([...messages, newMsg]);
    };

    const onKeyPress = (e: any) => {
        if (e.keyCode == 13) {
            submitMsg();
        }
    };

    return (
        <div className="chat_container">
            <ChatFeed
                messages={messages}
                isTyping={false} // set this to true when bot is typing
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
                <IconButton color="primary" size="medium" onClick={submitMsg}>
                    <SendIcon />
                </IconButton>
            </div>
        </div>
    );
}

export default Chat;
