import React, { useContext, useEffect, useRef, useState } from 'react';
import { AppContext } from '../AppContext';
import CanvasDraw from 'react-canvas-draw';
import { Button, Typography } from '@material-ui/core';

import './MapCanvas.css';

const get_canvas_size = (im_width: number, im_height: number) => {
    // map canvas is 80% width, the app container is 90% width
    const container_width = 0.8 * 0.9 * window.innerWidth;
    const container_hegiht = 0.8 * 0.9 * window.innerHeight;

    // console.log(container_width,container_hegiht);

    const ratio_w = container_width / im_width;
    // const ratio_h = container_hegiht / im_height;

    let canvas_width = im_width;
    let canvas_height = im_height;

    if (ratio_w < 1) {
        canvas_width *= ratio_w;
        canvas_height *= ratio_w;
    }

    return { canvas_width, canvas_height };
};

export interface IMapCanvas {
    im_width: number;
    im_height: number;
    im_name: string;
}

function MapCanvas({ im_width, im_height, im_name }: IMapCanvas) {
    const { state, setState } = useContext(AppContext);
    let canvasRef: CanvasDraw | null = null;

    const { canvas_width, canvas_height } = get_canvas_size(im_width, im_height);

    return (
        <>
            <div className="map_container">
                <Typography variant="h5">CLG lab - Chat Bot 1.0</Typography>
                <CanvasDraw
                    onChange={(e) => console.log((e as any).lines)}
                    ref={(canvasDraw) => (canvasRef = canvasDraw)}
                    canvasWidth={canvas_width}
                    canvasHeight={canvas_height}
                    brushColor="rgba(63,81,181,0.75)"
                    hideGrid={true}
                    clampLinesToDocument={false}
                    imgSrc={im_name}
                />
                <div className="control">
                    <Button
                        style={{ textTransform: 'none' }}
                        variant="contained"
                        color="primary"
                        onClick={() => canvasRef!.undo()}
                    >
                        Undo
                    </Button>
                    <Button
                        style={{ textTransform: 'none' }}
                        variant="outlined"
                        color="primary"
                        onClick={() => canvasRef!.clear()}
                    >
                        Erase
                    </Button>
                </div>
            </div>
        </>
    );
}

export default MapCanvas;
