import React from 'react';
import { Typography } from '@material-ui/core';
import { useContext } from 'react';
import { AppContext } from '../AppContext';
import { Rating } from '@material-ui/lab';
import { IQuestionInterface } from '../Wrapper';

function RatingQuestion(data: IQuestionInterface): JSX.Element {
    const { state, setState } = useContext(AppContext);
    const left_caption = data.meta.sliderLeftText ? data.meta.sliderLeftText : 'not at all likely';
    const right_caption = data.meta.slideRightText ? data.meta.slideRightText : 'extremely likely';

    const simple_set = (val: number | null) => {
        if (val == null) return;
        const user_survey = state.user_survey;
        user_survey[data.id].answer = val as number;
        setState({ ...state, user_survey });
    };

    return (
        <div className="SliderQuestionGroup">
            {data.meta.hintAbove ? (
                <Typography style={{ margin: '8px' }} component="legend">
                    {data.meta.hintAbove}
                </Typography>
            ) : null}

            <Typography component="legend">{data.meta.question}</Typography>
            <div className="SliderQuestionRate">
                <Typography variant="caption">{left_caption}</Typography>
                <Rating
                    style={{ marginLeft: '8px', marginRight: '8px' }}
                    name={data.id}
                    value={state.user_survey[data.id].answer as number}
                    onChange={(event, newValue) => {
                        simple_set(newValue);
                    }}
                />
                <Typography variant="caption">{right_caption}</Typography>
            </div>
        </div>
    );
}

export default RatingQuestion;
