import React from 'react';
import { TextField } from '@material-ui/core';
import { Typography } from '@material-ui/core';
import { useContext } from 'react';
import { AppContext } from '../AppContext';
import { IQuestionInterface } from '../Wrapper';

function TextFieldQuestion(data: IQuestionInterface): JSX.Element {
    const { state, setState } = useContext(AppContext);

    const simple_set = (e: any) => {
        const user_survey = state.user_survey;
        user_survey[data.id].answer = e.target.value.toString();
        setState({ ...state, user_survey });
    };

    return (
        <div className="QuestionGroup">
            <div style={{ width: '50%', display: 'flex', flexDirection: 'column' }}>
                <Typography component="legend" align="left">
                    {data.meta.question}
                </Typography>
                {data.meta.questionCont ? (
                    <Typography variant="caption" align="left">
                        {data.meta.questionCont}
                    </Typography>
                ) : null}
            </div>

            <TextField
                style={{ width: '50%' }}
                id={data.id}
                label="type here"
                variant="outlined"
                onChange={(event) => simple_set(event)}
                type={data.meta.numberText ? 'number' : undefined}
                value={state.user_survey[data.id].answer}
            />
        </div>
    );
}

export default TextFieldQuestion;
