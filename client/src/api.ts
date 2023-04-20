import axios, { AxiosResponse } from 'axios';
import { IAppState, MapCellIdx, UserSurvey } from './Wrapper';

// export const baseUrl = 'http://localhost:8080/api/v1/';
export const baseUrl = 'https://map-task-server-juxn2vqqxa-nw.a.run.app/api/v1/';

// export const huamn_to_human_event = async (guid: string, update: Function) => {
//     const evtSource = new EventSource(baseUrl + `event?guid=${guid}`);
//     evtSource.onopen = function () {
//         console.log('Connection to event server opened.');
//     };
//     evtSource.onmessage = function (e) {
//         const splited = e.data.split('__');
//         const guid = splited[0];
//         const id = Number(splited[1]);
//         const msg = splited[2];
//         update(guid, { id, msg, timestamp: Date.now() }, splited[3] === 'end');
//     };
//     evtSource.onerror = function (e) {
//         console.log('EventSource failed.', e);
//     };
// };

// export const callHuman = async (guid: string, msg: ChatMsg) => {
//     try {
//         (await axios.request({
//             url: baseUrl + 'call_human',
//             method: 'POST',
//             data: { guid, ...msg },
//         })) as AxiosResponse;
//     } catch (error: any) {
//         console.log('Server not connected');
//     }
// };

// export const notifyHumanEnd = async (guid: string, id: gameRole) => {
//     try {
//         (await axios.request({
//             url: baseUrl + 'notify_end_human',
//             method: 'POST',
//             data: { id, guid },
//         })) as AxiosResponse;
//     } catch (error: any) {
//         console.log('Server not connected');
//     }
// };

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
        const { game_state, general_survey, map_survey, ...all } = state;
        const map_survey_simpler = simplify_survey(map_survey);
        const general_survey_simpler = simplify_survey(general_survey);

        (await axios.request({
            url: baseUrl + 'upload',
            method: 'POST',
            data: {
                ...all,
                guid: all.game_config.guid,
                time: game_state.game_time,
                map_survey: map_survey_simpler,
                general_survey: general_survey_simpler,
            },
        })) as AxiosResponse;
        update();
        console.log('uploaded successfully');
    } catch (error: any) {
        console.log('Server not connected');
        update();
    }
};
