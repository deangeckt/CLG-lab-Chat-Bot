import axios, { AxiosResponse } from 'axios';

const baseUrl = 'http://localhost:8080/api/v1/';

export const getHealth = async () => {
    try {
        const response = (await axios.request({
            url: baseUrl + 'health',
            method: 'GET',
        })) as AxiosResponse;

        console.log(response.data);
    } catch (error: any) {
        console.log(error);
    }
};

export const callBot = async (msg: string, update: Function) => {
    try {
        const data = { msg };
        const response = (await axios.request({
            url: baseUrl + 'call',
            method: 'POST',
            data: data,
        })) as AxiosResponse;
        update(response.data.res);
    } catch (error: any) {
        update('Bot not connected');
    }
};
