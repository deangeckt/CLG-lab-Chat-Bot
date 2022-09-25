import React, { useContext, useEffect } from 'react';
import { AppContext } from '../AppContext';
import { Box, CircularProgress, IconButton, List, ListItem, TextField } from '@material-ui/core';
import SendIcon from '@material-ui/icons/Send';
import { useChat } from './useChat';
import './Chat.css';

function Chat(): JSX.Element {
    const { state } = useContext(AppContext);
    const { botType, onKeyPress, sendUserMsg, inputTxt, setInputTxt } = useChat();

    useEffect(() => {
        const cc = document.getElementById('chat_list');
        if (!cc) return;
        cc.scrollTo({
            top: cc.scrollHeight,
            behavior: 'smooth',
        });
    }, [state.chat]);

    return (
        <div className="chat_container">
            <List id="chat_list" style={{ height: '90%', overflowY: 'auto' }}>
                {state.chat.map(function (c, idx) {
                    const direction = c.id != state.game_config.game_role ? 'row' : 'row-reverse';
                    const color = c.id != state.game_config.game_role ? '#484644' : '#3f51b5';

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
                    value={inputTxt}
                    placeholder={'Type here'}
                    onChange={(e) => setInputTxt(e.target.value)}
                    onKeyDown={(e) => onKeyPress(e)}
                />
                <IconButton color="primary" size="medium" onClick={sendUserMsg}>
                    <SendIcon />
                </IconButton>
            </div>
        </div>
    );
}

export default Chat;
