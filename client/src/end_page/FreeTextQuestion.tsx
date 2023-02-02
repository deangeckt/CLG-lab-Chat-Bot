import React from 'react';
import { TextField } from '@material-ui/core';
import { Typography } from '@material-ui/core';
import { useContext } from 'react';
import { AppContext } from '../AppContext';
import { UserSurveyQuestion } from '../Wrapper';

export interface IQuestionInterface {
    meta: UserSurveyQuestion;
    id: string;
}

function FreeTextQuestion(data: IQuestionInterface): JSX.Element {
    const { state, setState } = useContext(AppContext);

    const simple_set = (e: any) => {
        const user_survey = state.user_survey;
        user_survey[data.id].answer = e.target.value.toString();
        setState({ ...state, user_survey });
    };

    return (
        <div className="FreeTextGroup">
            <Typography component="legend">{data.meta.question}</Typography>
            <TextField
                style={{ width: '25%', margin: '8px' }}
                id={data.id}
                label="type here"
                variant="outlined"
                onChange={(event) => simple_set(event)}
            />
        </div>
    );
}

export default FreeTextQuestion;
