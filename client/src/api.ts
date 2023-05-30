import axios, { AxiosResponse } from 'axios';
import { IAppState, MapCellIdx, UserSurvey } from './Wrapper';

// export const baseUrl = 'http://localhost:8080/api/v1/';
export const baseUrl = 'https://map-task-server-juxn2vqqxa-nw.a.run.app/api/v1/';

export const register = async (map_index: number, game_role: number, update: Function) => {
    try {
        const response = (await axios.request({
            url: baseUrl + 'register',
            method: 'POST',
            data: { map_index, game_role },
        })) as AxiosResponse;
        update(response.data, map_index);
    } catch (error: any) {
        update(null, map_index);
    }
};

export const callBot = async (
    guid: string,
    msg: string,
    cell: MapCellIdx,
    map_index: number,
    game_role: number,
    update: Function,
) => {
    try {
        const response = (await axios.request({
            url: baseUrl + 'call_bot',
            method: 'POST',
            data: { guid, msg, map_index, state: cell, game_role },
        })) as AxiosResponse;
        update(response.data);
    } catch (error: any) {
        update('Bot not connected');
    }
};

const simplify_survey = (survey: UserSurvey) => {
    const survey_simpler = Object.keys(survey).map((key) => {
        const q_obj = survey[key];
        const q = q_obj.question_ref ? `${survey[q_obj.question_ref].hintAbove} ${q_obj.question}` : q_obj.question;
        return { answer: survey[key].answer, question: q };
    });
    return survey_simpler;
};

export const upload = async (state: IAppState, update: Function) => {
    try {
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        const { general_survey, games } = state;
        const general_survey_simpler = simplify_survey(general_survey);

        const games_data = games.map((game) => {
            return {
                survey: simplify_survey(game.map_survey),
                game_time: game.game_state.game_time,
                config: game.game_config,
                chat: game.chat,
                map_metadata: game.map_metadata,
                user_map_path: game.user_map_path,
            };
        });

        (await axios.request({
            url: baseUrl + 'upload',
            method: 'POST',
            data: {
                games_data,
                general_survey: general_survey_simpler,
                clinet_version: state.clinet_version,
                prolific: state.prolific,
            },
        })) as AxiosResponse;
        update();
        console.log('uploaded successfully');
    } catch (error: any) {
        console.log('Server not connected');
        update();
    }
};
