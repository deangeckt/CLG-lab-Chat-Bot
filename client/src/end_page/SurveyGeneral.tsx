import React, { useState } from 'react';
import { Box, Button, CircularProgress } from '@material-ui/core';
import { Typography } from '@material-ui/core';
import { useContext } from 'react';
import { AppContext } from '../AppContext';
import Header from '../common/Header';
import {
    end_page_title1_str,
    end_page_group_4_str,
    end_page_group_5_str,
    end_page_group_6_str,
    end_page_group_7_str,
} from '../common/strings';
import RatingQuestion from './RatingQuestion';
import TextFieldQuestion from './TextFieldQuestion';
import SelectQuestion from './SelectQuestion';
import { useNavigate } from 'react-router-dom';
import { upload } from '../api';
import { main_blue } from '../common/colors';

import './EndPage.css';

function SurveyGeneral(): JSX.Element {
    const { state, setState } = useContext(AppContext);
    const navigate = useNavigate();
    const [currGroup, SetCurrGroup] = useState(0);
    const [reg, SetReg] = useState('not_sent');

    React.useEffect(() => {
        if (!state.consent) navigate('/');
        if (state.uploaded) {
            SetReg('done');
        }
    }, []);

    const survey_groups: string[][] = [];
    const survey_groups_titles: string[] = [
        end_page_group_4_str,
        end_page_group_5_str,
        end_page_group_6_str,
        end_page_group_7_str,
    ];

    survey_groups.push(Object.keys(state.general_survey).slice(0, 9));
    survey_groups.push(Object.keys(state.general_survey).slice(9, 19));
    survey_groups.push(Object.keys(state.general_survey).slice(19, 31));
    survey_groups.push(Object.keys(state.general_survey).slice(31, 47));

    const scroll_begin = () => {
        const tr = document.getElementById('container');
        if (!tr) return;
        tr.scrollTo({
            top: 0,
            behavior: 'smooth',
        });
    };

    const next = () => {
        scroll_begin();
        if (currGroup == survey_groups.length - 1) {
            upload(state, () => {
                SetReg('done');
                setState({ ...state, uploaded: true });
                window.open('https://app.prolific.co/submissions/complete?cc=C15G3HZJ');
            });
            SetReg('loading');
        } else {
            SetCurrGroup(currGroup + 1);
        }
    };

    const back = () => {
        scroll_begin();
        if (currGroup == 0) return;
        SetCurrGroup(currGroup - 1);
    };

    return (
        <div className="End">
            <Header />
            <div className="End_Container" id="container">
                {reg == 'not_sent' ? (
                    <>
                        <Typography style={{ marginTop: '16px' }} variant="h4">
                            {end_page_title1_str}
                        </Typography>
                        <div className="Group">
                            <Typography variant="h5" style={{ marginBottom: '32px' }}>
                                {survey_groups_titles[currGroup]}
                            </Typography>
                            {survey_groups[currGroup].map(function (key) {
                                const t = state.general_survey[key].type;
                                if (t == 'rating')
                                    return (
                                        <RatingQuestion
                                            meta={state.general_survey[key]}
                                            id={key}
                                            key={key}
                                            survey="general"
                                        />
                                    );
                                else if (t == 'textfield')
                                    return (
                                        <TextFieldQuestion
                                            meta={state.general_survey[key]}
                                            id={key}
                                            key={key}
                                            survey="general"
                                        />
                                    );
                                else if (t == 'select')
                                    return (
                                        <SelectQuestion
                                            meta={state.general_survey[key]}
                                            id={key}
                                            key={key}
                                            survey="general"
                                        />
                                    );
                            })}
                        </div>
                        <div style={{ display: 'flex', width: '100%', justifyContent: 'space-between' }}>
                            <Button
                                disabled={currGroup == 0}
                                style={{
                                    textTransform: 'none',
                                    marginLeft: '16px',
                                    marginBottom: '16px',
                                }}
                                className="nav_btn"
                                variant="outlined"
                                color="primary"
                                onClick={back}
                            >
                                Back
                            </Button>
                            <Button
                                style={{
                                    textTransform: 'none',
                                    marginRight: '16px',
                                    marginBottom: '16px',
                                }}
                                variant="outlined"
                                color="primary"
                                onClick={next}
                            >
                                {currGroup == survey_groups.length - 1 ? 'Finish' : 'Next'}
                            </Button>
                        </div>
                    </>
                ) : null}
                {reg == 'loading' ? (
                    <Box sx={{ display: 'flex', marginTop: '25%' }}>
                        <CircularProgress style={{ color: main_blue, width: '30px', height: '30px' }} />
                    </Box>
                ) : null}
                {reg == 'done' ? (
                    <Typography style={{ marginTop: '25%' }} variant="h4">
                        Thank you! <br /> <br /> prolific completion code: C15G3HZJ
                    </Typography>
                ) : null}
            </div>
        </div>
    );
}

export default SurveyGeneral;
