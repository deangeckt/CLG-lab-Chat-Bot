import React, { useState } from 'react';
import { Box, Button, CircularProgress, TextField } from '@material-ui/core';
import { Typography } from '@material-ui/core';
import { useContext } from 'react';
import { AppContext } from '../AppContext';
import Header from '../common/Header';
import { init_app_state, UserSurvey } from '../Wrapper';
import { upload } from '../api';
import { main_blue } from '../common/colors';
import { useNavigate } from 'react-router-dom';
import './EndPage.css';

function EndPage(): JSX.Element {
    const { state, setState } = useContext(AppContext);
    const [reg, SetReg] = useState('not_sent');

    const navigate = useNavigate();
    const startOver = () => {
        setState(init_app_state);
        const path = '/';
        navigate(path);
    };

    const simple_set = (e: any, field: keyof UserSurvey) => {
        const user_survey = state.user_survey;
        user_survey[field] = e.target.value.toString();
        setState({ ...state, user_survey });
    };

    const onKeyClick = (e: any) => {
        if (e.keyCode == 13 && reg == 'not_sent') send();
    };

    const send = () => {
        upload(state, () => {
            SetReg('done');
        });
        SetReg('loading');
    };

    return (
        <div className="End">
            <Header />
            <div className="End_Container">
                {reg == 'not_sent' ? (
                    <>
                        <Typography variant="h4">Gracias for participating</Typography>
                        <TextField
                            id="outlined-basic"
                            label="What did you think?"
                            variant="outlined"
                            onChange={(event) => simple_set(event, 'free_text')}
                            onKeyDown={onKeyClick}
                        />
                        <Button style={{ textTransform: 'none' }} variant="outlined" color="primary" onClick={send}>
                            Send
                        </Button>
                    </>
                ) : null}
                {reg == 'loading' ? (
                    <Box sx={{ display: 'flex', margin: '16px' }}>
                        <CircularProgress style={{ color: main_blue, width: '30px', height: '30px' }} />
                    </Box>
                ) : null}
                {reg == 'done' ? (
                    <>
                        <Typography variant="h4">Thank you</Typography>
                        <Button
                            style={{ textTransform: 'none' }}
                            variant="outlined"
                            color="primary"
                            onClick={startOver}
                        >
                            Start Over
                        </Button>
                    </>
                ) : null}
            </div>
        </div>
    );
}

export default EndPage;
