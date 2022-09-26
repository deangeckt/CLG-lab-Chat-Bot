import axios, { AxiosResponse } from 'axios';
import { ChatMsg, gameMode, MapCellIdx } from './Wrapper';

export const baseUrl = 'http://localhost:8080/api/v1/';

export const huamn_to_human_event = async (update: Function) => {
    const evtSource = new EventSource(baseUrl + 'event');
    evtSource.onopen = function () {
        console.log('Connection to event server opened.');
    };
    evtSource.onmessage = function (e) {
        const splited = e.data.split('__');

        update({ id: Number(splited[0]), msg: splited[1] });
    };
    evtSource.onerror = function (e) {
        console.log('EventSource failed.', e);
    };
};

export const callBot = async (msg: string, cell: MapCellIdx, update: Function) => {
    try {
        const data = { msg, state: cell };
        const response = (await axios.request({
            url: baseUrl + 'call_bot',
            method: 'POST',
            data: data,
        })) as AxiosResponse;
        update(response.data.res);
    } catch (error: any) {
        update('Bot not connected');
    }
};

export const callHuman = async (msg: ChatMsg) => {
    try {
        (await axios.request({
            url: baseUrl + 'call_human',
            method: 'POST',
            data: msg,
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
