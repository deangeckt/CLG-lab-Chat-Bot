import React, { useState } from 'react';
import { Box, Button, CircularProgress } from '@material-ui/core';
import { Typography } from '@material-ui/core';
import { useContext } from 'react';
import { AppContext } from '../AppContext';
import Header from '../common/Header';
import { upload } from '../api';
import { main_blue } from '../common/colors';
import {
    end_page_group_1_str,
    end_page_title1_str,
    end_page_group_2_str,
    end_page_group_3_str,
} from '../common/strings';
import RatingQuestion from './RatingQuestion';
import TextFieldQuestion from './TextFieldQuestion';
import SelectQuestion from './SelectQuestion';
import './EndPage.css';

function SurveyMap(): JSX.Element {
    const { state } = useContext(AppContext);
    const [reg, SetReg] = useState('not_sent');
    const [currGroup, SetCurrGroup] = useState(0);

    const survey_groups: string[][] = [];
    const survey_groups_titles: string[] = [end_page_group_1_str, end_page_group_2_str, end_page_group_3_str];

    survey_groups.push(Object.keys(state.map_survey).slice(0, 3));
    survey_groups.push(Object.keys(state.map_survey).slice(3, 12));
    survey_groups.push(Object.keys(state.map_survey).slice(12, 14));

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
                // TODO put prolific id then or ask to do a new map?
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
                                const t = state.map_survey[key].type;
                                if (t == 'rating')
                                    return (
                                        <RatingQuestion meta={state.map_survey[key]} id={key} key={key} survey="map" />
                                    );
                                else if (t == 'textfield')
                                    return (
                                        <TextFieldQuestion
                                            meta={state.map_survey[key]}
                                            id={key}
                                            key={key}
                                            survey="map"
                                        />
                                    );
                                else if (t == 'select')
                                    return (
                                        <SelectQuestion meta={state.map_survey[key]} id={key} key={key} survey="map" />
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
                        Thank you
                    </Typography>
                ) : null}
            </div>
        </div>
    );
}

export default SurveyMap;