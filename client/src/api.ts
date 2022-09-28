import axios, { AxiosResponse } from 'axios';
import { ChatMsg, gameMode, gameRole, MapCellIdx } from './Wrapper';

export const baseUrl = 'http://localhost:8080/api/v1/';

export const huamn_to_human_event = async (guid: string, update: Function) => {
    const evtSource = new EventSource(baseUrl + `event?guid=${guid}`);
    evtSource.onopen = function () {
        console.log('Connection to event server opened.');
    };
    evtSource.onmessage = function (e) {
        const splited = e.data.split('__');
        const guid = splited[0];
        const id = Number(splited[1]);
        const msg = splited[2];
        update(guid, { id, msg }, splited[3] === 'end');
    };
    evtSource.onerror = function (e) {
        console.log('EventSource failed.', e);
    };
};

export const callBot = async (msg: string, cell: MapCellIdx, update: Function) => {
    try {
        const response = (await axios.request({
            url: baseUrl + 'call_bot',
            method: 'POST',
            data: { msg, state: cell },
        })) as AxiosResponse;
        update(response.data.res);
    } catch (error: any) {
        update('Bot not connected');
    }
};

export const callHuman = async (guid: string, msg: ChatMsg) => {
    try {
        (await axios.request({
            url: baseUrl + 'call_human',
            method: 'POST',
            data: { guid, ...msg },
        })) as AxiosResponse;
    } catch (error: any) {
        console.log('Server not connected');
    }
};

export const notifyHumanEnd = async (guid: string, id: gameRole) => {
    try {
        (await axios.request({
            url: baseUrl + 'notify_end_human',
            method: 'POST',
            data: { id, guid },
        })) as AxiosResponse;
    } catch (error: any) {
        console.log('Server not connected');
    }
};

export const register = async (mode: gameMode, update: Function) => {
    try {
        const response = (await axios.request({
            url: baseUrl + 'register',
            method: 'POST',
            data: { mode },
        })) as AxiosResponse;
        update(response.data);
    } catch (error: any) {
        update(null);
    }
};
