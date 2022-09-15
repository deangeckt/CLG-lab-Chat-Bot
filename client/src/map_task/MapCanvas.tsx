import React, { useContext, useEffect } from 'react';
import { AppContext } from '../AppContext';
import CanvasDraw from 'react-canvas-draw';
import { Button, Typography } from '@material-ui/core';

import './MapCanvas.css';
const start_data =
    '{"lines":[{"points":[{"x":937.5472857842693,"y":52.92399213028491},{"x":937.5472857842693,"y":52.92399213028491}],"brushColor":"rgba(63,81,181,0.75)","brushRadius":10}],"width":969.0063878326996,"height":721.44}';

const get_canvas_size = (im_width: number, im_height: number) => {
    // map canvas is 80% width, the app container is 90% width
    const container_width = 0.75 * 0.9 * window.innerWidth;
    const container_height = 0.75 * 0.9 * window.innerHeight;

    const ratio_w = container_width / im_width;
    const ratio_h = container_height / im_height;

    const ratio = ratio_w < ratio_h ? ratio_w : ratio_h;

    let canvas_width = im_width;
    let canvas_height = im_height;

    if (ratio < 1) {
        canvas_width *= ratio;
        canvas_height *= ratio;
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

    const curr_coord = (e: any) => {
        const lines = e.lines;
        const last_line = lines[lines.length - 1];

        const points = last_line.points;
        const last_point = points[points.length - 1];

        const curr_coord = state.curr_corrd;
        curr_coord.x = last_point.x / canvas_width;
        curr_coord.y = last_point.y / canvas_height;
        setState({ ...state, curr_coord });

        console.log((canvasRef as any).lines);
    };

    const un_do = () => {
        if ((canvasRef as any).lines.length == 1) return;
        canvasRef!.undo();
    };

    useEffect(() => {
        if (canvasRef) {
            canvasRef.loadSaveData(start_data, true);
            console.log('load');
        }
    }, []);

    return (
        <>
            <div className="map_container">
                <Typography variant="h5">CLG lab - Chat Bot 1.0</Typography>
                <CanvasDraw
                    onChange={(e) => curr_coord(e)}
                    ref={(canvasDraw) => (canvasRef = canvasDraw)}
                    canvasWidth={canvas_width}
                    canvasHeight={canvas_height}
                    brushColor="rgba(63,81,181,0.75)"
                    hideGrid={true}
                    clampLinesToDocument={false}
                    imgSrc={im_name}
                    enablePanAndZoom={false}
                    disabled={false}
                />
                <div className="control">
                    <Button
                        style={{ textTransform: 'none' }}
                        variant="contained"
                        color="primary"
                        onClick={() => un_do()}
                    >
                        Undo
                    </Button>
                    <Button
                        style={{ textTransform: 'none' }}
                        variant="outlined"
                        color="primary"
                        onClick={() => canvasRef!.loadSaveData(start_data)}
                    >
                        Erase
                    </Button>
                </div>
            </div>
        </>
    );
}

export default MapCanvas;
