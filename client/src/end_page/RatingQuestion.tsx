import React, { useState } from 'react';
import { Button, Slider, Typography } from '@material-ui/core';
import { useContext } from 'react';
import { AppContext } from '../AppContext';
import { IQuestionInterface } from '../Wrapper';

function RatingQuestion(data: IQuestionInterface): JSX.Element {
    const { state, setState } = useContext(AppContext);
    const [na, setNa] = useState(false);
    const left_caption = data.meta.sliderLeftText ? data.meta.sliderLeftText : 'not at all likely';
    const right_caption = data.meta.slideRightText ? data.meta.slideRightText : 'extremely likely';

    const simple_set = (val: number | string) => {
        const user_survey = state.user_survey;
        user_survey[data.id].answer = val;
        setState({ ...state, user_survey });
    };

    const toggle_na = () => {
        if (!na) simple_set('na');
        else simple_set(50);
        setNa(!na);
    };

    const curr_ans = na ? null : state.user_survey[data.id].answer;

    return (
        <>
            {data.meta.hintAbove ? (
                <Typography style={{ marginTop: '32px' }} align="left" component="legend">
                    {data.meta.hintAbove}
                </Typography>
            ) : null}
            <div className="SliderQuestionGroup">
                <Typography align="left" component="legend" style={{ width: '50%' }}>
                    {data.meta.question}
                </Typography>
                <div className="SliderQuestionRate">
                    {!na ? (
                        <>
                            <Typography style={{ width: '25%' }} variant="caption">
                                {left_caption}
                            </Typography>
                            <Slider
                                style={{ width: '50%' }}
                                name={data.id}
                                value={curr_ans as number}
                                onChange={(event, newValue) => {
                                    simple_set(newValue as number);
                                }}
                                valueLabelDisplay="off"
                            />
                            <Typography style={{ width: '25%' }} variant="caption">
                                {right_caption}
                            </Typography>
                        </>
                    ) : null}
                </div>
                {data.meta.not_applicable ? (
                    <Button
                        style={{ textTransform: 'none', fontSize: '12px', marginTop: '8px' }}
                        variant={na ? 'contained' : 'outlined'}
                        color="primary"
                        onClick={() => toggle_na()}
                    >
                        Not Applicable
                    </Button>
                ) : null}
            </div>
        </>
    );
}

export default RatingQuestion;
