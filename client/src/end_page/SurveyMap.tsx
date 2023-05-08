import React, { useState } from 'react';
import { Button, Box, CircularProgress } from '@material-ui/core';
import { Typography } from '@material-ui/core';
import { useContext } from 'react';
import { AppContext } from '../AppContext';
import Header from '../common/Header';
import {
    end_page_group_1_str,
    end_page_title1_str,
    end_page_group_2_str,
    end_page_group_3_str,
} from '../common/strings';
import RatingQuestion from './RatingQuestion';
import TextFieldQuestion from './TextFieldQuestion';
import SelectQuestion from './SelectQuestion';
import { useNavigate } from 'react-router-dom';
import './EndPage.css';
import { maps } from '../Wrapper';
import { useRegister } from '../useRegister';
import { main_blue } from '../common/colors';

function SurveyMap(): JSX.Element {
    const navigate = useNavigate();
    const { state } = useContext(AppContext);
    const { create_new_game } = useRegister();
    const [currGroup, SetCurrGroup] = useState(0);

    React.useEffect(() => {
        if (!state.consent) navigate('/');
    }, []);

    const survey_groups: string[][] = [];
    const survey_groups_titles: string[] = [end_page_group_1_str, end_page_group_2_str, end_page_group_3_str];

    const map_survey = state.games[state.curr_game].map_survey;

    survey_groups.push(Object.keys(map_survey).slice(0, 3));
    survey_groups.push(Object.keys(map_survey).slice(3, 12));
    survey_groups.push(Object.keys(map_survey).slice(12, 14));

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
            navigate('/general_survey');
        } else {
            SetCurrGroup(currGroup + 1);
        }
    };

    const render_new_map_btn = () => {
        if (state.curr_game == maps.length - 1) return null;
        if (currGroup !== survey_groups.length - 1) return null;
        return (
            <Button
                style={{
                    textTransform: 'none',
                    marginRight: '16px',
                    marginBottom: '16px',
                }}
                variant="outlined"
                color="primary"
                onClick={create_new_game}
            >
                Start a new map
            </Button>
        );
    };

    const back = () => {
        scroll_begin();
        if (currGroup == 0) return;
        SetCurrGroup(currGroup - 1);
    };

    return (
        <div className="End">
            <Header />
            {state.registerd === 'load' && (
                <Box sx={{ display: 'flex', margin: '32px' }}>
                    <CircularProgress style={{ color: main_blue, width: '30px', height: '30px' }} />
                </Box>
            )}
            {state.registerd === 'yes' && (
                <div className="End_Container" id="container">
                    <Typography style={{ marginTop: '16px' }} variant="h4">
                        {end_page_title1_str} - map {state.curr_game + 1}
                    </Typography>
                    <div className="Group">
                        <Typography variant="h5" style={{ marginBottom: '32px' }}>
                            {survey_groups_titles[currGroup]}
                        </Typography>
                        {survey_groups[currGroup].map(function (key) {
                            if (map_survey[key].ignore) return null;
                            const t = map_survey[key].type;
                            if (t == 'rating')
                                return <RatingQuestion meta={map_survey[key]} id={key} key={key} survey="map" />;
                            else if (t == 'textfield')
                                return <TextFieldQuestion meta={map_survey[key]} id={key} key={key} survey="map" />;
                            else if (t == 'select')
                                return <SelectQuestion meta={map_survey[key]} id={key} key={key} survey="map" />;
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
                        <div>
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
                            {render_new_map_btn()}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default SurveyMap;
