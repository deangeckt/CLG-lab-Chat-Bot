import React, { useContext, useState } from 'react';
import { AppContext } from '../AppContext';
import { Box, CircularProgress, IconButton, List, ListItem, TextField } from '@material-ui/core';
import SendIcon from '@material-ui/icons/Send';
import { callBot } from '../api';
import { ChatMsg } from '../Wrapper';
import './Chat.css';

// TODO: fix scroll auto down

function Chat(): JSX.Element {
    const { state, setState } = useContext(AppContext);
    const [currMsg, setCurrMsg] = useState('');
    const [botType, setBotType] = useState(false);

    const updateChatState = (newMsg: ChatMsg[]) => {
        const chat = [...state.chat].concat(newMsg);
        setState({ ...state, chat: chat });
    };

    const addUserMsg = () => {
        if (!currMsg) return;
        updateChatState([{ message: currMsg, id: 0 }]);
        setCurrMsg('');
        setBotType(true);
        const curr_cell = state.user_map_path[state.user_map_path.length - 1];
        callBot(currMsg, curr_cell, addBotMsg);
    };
    // very ugly workaround!
    const addBotMsg = (msg: string) => {
        updateChatState([
            { message: currMsg, id: 0 },
            { message: msg, id: 1 },
        ]);
        setBotType(false);
    };

    const onKeyPress = (e: any) => {
        if (e.keyCode == 13) {
            addUserMsg();
        }
    };

    return (
        <div className="chat_container">
            <List style={{ height: '90%', overflowY: 'auto' }}>
                {state.chat.map(function (c, idx) {
                    const direction = c.id == 1 ? 'row' : 'row-reverse';
                    const color = c.id == 1 ? '#484644' : '#3f51b5';

                    return (
                        <ListItem key={idx}>
                            <div style={{ display: 'flex', flexDirection: direction, width: '100%' }}>
                                <span
                                    style={{
                                        color: 'white',
                                        backgroundColor: color,
                                        borderRadius: '8px',
                                        padding: '8px',
                                        fontSize: '18px',
                                    }}
                                >
                                    {c.message}
                                </span>
                            </div>
                        </ListItem>
                    );
                })}
                {botType ? (
                    <Box sx={{ display: 'flex', marginLeft: '16px' }}>
                        <CircularProgress style={{ color: '#484644', width: '30px', height: '30px' }} />
                    </Box>
                ) : null}
            </List>

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
