import React, { useEffect, useState } from 'react';
import { Box, Button, CircularProgress } from '@material-ui/core';
import { Typography } from '@material-ui/core';
import { useContext } from 'react';
import { AppContext } from '../AppContext';
import Header from '../common/Header';
import { IAppState } from '../Wrapper';
import { upload } from '../api';
import { main_blue } from '../common/colors';
import {
    end_page_group_1_str,
    end_page_title1_str,
    end_page_group_2_str,
    end_page_group_3_str,
    end_page_group_4_str,
    end_page_group_5_str,
    end_page_group_6_str,
} from '../common/strings';
import RatingQuestion from './RatingQuestion';
import TextFieldQuestion from './TextFieldQuestion';
import SelectQuestion from './SelectQuestion';
import './EndPage.css';

function EndPage(): JSX.Element {
    const { state, setState } = useContext(AppContext);
    const [reg, SetReg] = useState('not_sent');
    const [finish, setFinish] = useState(true);

    const survey_groups: string[][] = [];
    const survey_groups_titles: string[] = [
        end_page_group_1_str,
        end_page_group_2_str,
        end_page_group_3_str,
        end_page_group_4_str,
        end_page_group_5_str,
        end_page_group_6_str,
    ];
    survey_groups.push(Object.keys(state.user_survey).slice(0, 4));
    survey_groups.push(Object.keys(state.user_survey).slice(4, 12));
    survey_groups.push(Object.keys(state.user_survey).slice(12, 14));
    survey_groups.push(Object.keys(state.user_survey).slice(14, 23));
    survey_groups.push(Object.keys(state.user_survey).slice(23, 30));
    // survey_groups.push(Object.keys(state.user_survey).slice(30, 35));

    useEffect(() => {
        if (state.game_config.game_mode != 'human') return;
        const state_str = localStorage.getItem('state');
        if (!state_str) return;
        const state_obj = JSON.parse(state_str) as IAppState;
        if (state.game_config.game_role != state_obj.game_config.game_role) return;
        if (state.game_config.guid != state_obj.game_config.guid) return;
        console.log('using local strg');
        setState(state_obj);
        localStorage.removeItem('state');
    }, []);

    useEffect(() => {
        const answers = Object.keys(state.user_survey).map((key) => state.user_survey[key].answer);
        const notFinished = answers.some((ans) => ans == '' || ans == null);
        // setFinish(!notFinished);
    }, [state]);

    const send = () => {
        // upload(state, () => {
        //     SetReg('done');
        // });
        // SetReg('loading');
        console.log(state.user_survey);
    };

    return (
        <div className="End">
            <Header />
            <div className="End_Container">
                {reg == 'not_sent' ? (
                    <>
                        <Typography style={{ marginTop: '16px' }} variant="h4">
                            {end_page_title1_str}
                        </Typography>
                        {survey_groups.map((group, index) => (
                            <div className="Group" key={index}>
                                <>
                                    <Typography variant="h5">{survey_groups_titles[index]}</Typography>
                                    {group.map(function (key) {
                                        const t = state.user_survey[key].type;
                                        if (t == 'rating')
                                            return <RatingQuestion meta={state.user_survey[key]} id={key} key={key} />;
                                        else if (t == 'textfield')
                                            return (
                                                <TextFieldQuestion meta={state.user_survey[key]} id={key} key={key} />
                                            );
                                        else if (t == 'select')
                                            return <SelectQuestion meta={state.user_survey[key]} id={key} key={key} />;
                                    })}
                                </>
                            </div>
                        ))}

                        <Button
                            disabled={!finish}
                            style={{ textTransform: 'none', marginBottom: '16px' }}
                            variant="outlined"
                            color="primary"
                            onClick={send}
                        >
                            Send
                        </Button>
                    </>
                ) : null}
                {reg == 'loading' ? (
                    <Box sx={{ display: 'flex', marginTop: '25%' }}>
                        <CircularProgress style={{ color: main_blue, width: '30px', height: '30px' }} />
                    </Box>
                ) : null}
                {reg == 'done' ? (
                    <Typography style={{ marginTop: '25%' }} variant="h4">
                        Thank you
                    </Typography>
                ) : null}
            </div>
        </div>
    );
}

export default EndPage;
