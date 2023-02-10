import React, { useState } from 'react';
import { Button, Typography } from '@material-ui/core';
import { useContext } from 'react';
import { AppContext } from '../AppContext';
import { Rating } from '@material-ui/lab';
import { IQuestionInterface } from '../Wrapper';

const na_value = 'Not Applicable';

function RatingQuestion(data: IQuestionInterface): JSX.Element {
    const { state, setState } = useContext(AppContext);
    const [na, setNa] = useState(false);
    const left_caption = data.meta.sliderLeftText ? data.meta.sliderLeftText : 'not at all likely';
    const right_caption = data.meta.slideRightText ? data.meta.slideRightText : 'extremely likely';

    const simple_set = (val: number | null | string) => {
        if (val == null) return;
        const user_survey = state.user_survey;
        user_survey[data.id].answer = val;
        setState({ ...state, user_survey });
        if (val != na_value) setNa(false);
    };

    const set_not_applicable = () => {
        setNa(true);
        simple_set(na_value);
    };

    const curr_ans = na ? null : state.user_survey[data.id].answer;

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
                    value={curr_ans as number}
                    onChange={(event, newValue) => {
                        simple_set(newValue);
                    }}
                />
                <Typography variant="caption">{right_caption}</Typography>
            </div>
            {data.meta.not_applicable ? (
                <Button
                    style={{ textTransform: 'none', fontSize: '12px', marginTop: '8px' }}
                    variant={na ? 'contained' : 'outlined'}
                    color="primary"
                    onClick={() => set_not_applicable()}
                >
                    Not Applicable
                </Button>
            ) : null}
        </div>
    );
}

export default RatingQuestion;
