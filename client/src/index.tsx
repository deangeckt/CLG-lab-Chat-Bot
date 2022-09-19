import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './map_task/App';
import Wrapper from './Wrapper';
import { Route, Routes, BrowserRouter } from 'react-router-dom';
import './index.css';
import Home from './home_page/Home';

const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement);

root.render(
    <Wrapper>
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="map_task" element={<App />} />
            </Routes>
        </BrowserRouter>
    </Wrapper>,
);
