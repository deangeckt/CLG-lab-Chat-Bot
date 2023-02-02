import React from 'react';
import { Typography } from '@material-ui/core';
import { useContext } from 'react';
import { AppContext } from '../AppContext';
import { Rating } from '@material-ui/lab';
import { UserSurveyQuestion } from '../Wrapper';

export interface IQuestionInterface {
    meta: UserSurveyQuestion;
    id: string;
}

function DiSliderQuestion(data: IQuestionInterface): JSX.Element {
    const { state, setState } = useContext(AppContext);

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
                <Typography variant="caption">not at all likely</Typography>
                <Rating
                    style={{ marginLeft: '8px', marginRight: '8px' }}
                    name={data.meta.question}
                    value={state.user_survey[data.id].answer as number}
                    onChange={(event, newValue) => {
                        simple_set(newValue);
                    }}
                />
                <Typography variant="caption">extremely likely</Typography>
            </div>
        </div>
    );
}

export default DiSliderQuestion;
