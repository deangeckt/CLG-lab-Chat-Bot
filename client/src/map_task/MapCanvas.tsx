import React, { useContext, useEffect, useRef, useState } from 'react';
import { AppContext } from '../AppContext';
import { MapCellIdx } from '../Wrapper';

import './MapCanvas.css';

const get_canvas_size = (im_width: number, im_height: number) => {
    // map canvas is 75% width, the app container is 90% width
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

const path_cell_color = 'rgba(63, 81, 181, 0.8)';
const next_cells_color = 'rgba(22, 196, 59, 0.4)';

function MapCanvas() {
    const { state, setState } = useContext(AppContext);
    const [matrix, setMatrix] = useState(Array<Array<Path2D>>);
    const [neighbors, setNeighbors] = useState<Set<string>>(new Set());
    const canvasRef = useRef(null);
    const { canvas_width, canvas_height } = get_canvas_size(state.map_metadata.im_width, state.map_metadata.im_height);
    const radius = 15;

    useEffect(() => {
        const image = document.getElementById('source');
        const canvas = canvasRef.current as any;
        if (!canvas) {
            return;
        }
        const context = canvas.getContext('2d');
        context.drawImage(image, 0, 0, canvas_width, canvas_height);
        init_matrix();
    }, []);

    const color_change = (cells: MapCellIdx[], color: string) => {
        const canvas = canvasRef.current;
        const context = (canvas as any).getContext('2d');

        for (const cell of cells) {
            const path_obj = matrix[cell.r][cell.c];
            context.fillStyle = color;
            context.fill(path_obj);
        }
    };

    const init_matrix = () => {
        const canvas = canvasRef.current;
        const context = (canvas as any).getContext('2d');
        context.beginPath();

        const rows = state.map_metadata.rows;
        const columns = state.map_metadata.cols;

        const col_step = canvas_width / columns;
        const row_step = canvas_height / rows;

        const new_mat: Array<Array<Path2D>> = [];
        const new_neighbors = get_neighbors(state.curr_map_cell);

        for (let row = 0; row < rows; row++) {
            const new_col: Array<Path2D> = [];
            for (let col = 0; col < columns; col++) {
                const curr: MapCellIdx = { r: row, c: col };
                if (curr.c == state.curr_map_cell.c && curr.r == state.curr_map_cell.r)
                    context.fillStyle = path_cell_color;
                else if (new_neighbors.has(`${curr.r}_${curr.c}`)) context.fillStyle = next_cells_color;
                else context.fillStyle = 'transparent';

                const circle = new Path2D();
                circle.arc(col_step * col + radius * 1.5, row_step * row + radius * 1.5, radius, 0, 2 * Math.PI);
                context.fill(circle);
                new_col.push(circle);
            }
            new_mat.push(new_col);
        }
        setMatrix(new_mat);
        setNeighbors(new_neighbors);
    };

    const neighbor_str_to_cell = (neighbor: string): MapCellIdx => {
        const splited = neighbor.split('_');
        return { r: Number(splited[0]), c: Number(splited[1]) };
    };

    const get_neighbors = (curr: MapCellIdx): Set<string> => {
        const row = curr.r;
        const col = curr.c;

        const new_neighbors = new Set<string>();
        if (row - 1 > 0) new_neighbors.add(`${row - 1}_${col}`);
        if (row + 1 < state.map_metadata.rows - 1) new_neighbors.add(`${row + 1}_${col}`);
        if (col - 1 > 0) new_neighbors.add(`${row}_${col - 1}`);
        if (col + 1 < state.map_metadata.cols - 1) new_neighbors.add(`${row}_${col + 1}`);
        return new_neighbors;
    };

    const next_move = (new_cell: MapCellIdx) => {
        const new_neighbors = get_neighbors(new_cell);
        setNeighbors(new_neighbors);

        const ui_new_neighbors = new Set(new_neighbors);
        ui_new_neighbors.delete(`${state.curr_map_cell.r}_${state.curr_map_cell.c}`);
        const ui_new_neighbors_list = Array.from(new_neighbors).map((n) => neighbor_str_to_cell(n));

        const canvas = canvasRef.current;
        const context = (canvas as any).getContext('2d');
        context.clearRect(0, 0, canvas_width, canvas_height);
        const image = document.getElementById('source');
        context.drawImage(image, 0, 0, canvas_width, canvas_height);

        const user_map_path = [...state.user_map_path].concat(new_cell);
        color_change(ui_new_neighbors_list, next_cells_color);
        color_change(user_map_path, path_cell_color);

        setState({ ...state, curr_map_cell: new_cell, user_map_path: user_map_path });
    };

    const onKeyClick = (e: any) => {
        let row = state.curr_map_cell.r;
        let col = state.curr_map_cell.c;
        const cols = state.map_metadata.cols;
        const rows = state.map_metadata.rows;

        if (e.keyCode == 37) {
            // console.log('left');
            col = col > 0 ? col - 1 : 0;
        } else if (e.keyCode == 39) {
            // console.log('right');
            col = col < cols - 1 ? col + 1 : cols - 1;
        } else if (e.keyCode == 40) {
            // console.log('down');
            row = row < rows - 1 ? row + 1 : rows - 1;
        } else if (e.keyCode == 38) {
            // console.log('up');
            row = row > 0 ? row - 1 : 0;
        } else {
            return;
        }
        const new_cell: MapCellIdx = { r: row, c: col };
        next_move(new_cell);
    };

    const onMouseClick = (e: any) => {
        const canvas = canvasRef.current;
        const context = (canvas as any).getContext('2d');
        for (const neighbor_str of neighbors) {
            const neighbor = neighbor_str_to_cell(neighbor_str);
            const cell = matrix[neighbor.r][neighbor.c];
            if (context.isPointInPath(cell, e.nativeEvent.offsetX, e.nativeEvent.offsetY)) {
                next_move(neighbor);
                break;
            }
        }
    };

    return (
        <div className="map_container">
            <canvas
                tabIndex={0}
                ref={canvasRef}
                width={canvas_width}
                height={canvas_height}
                className={'map_canvas'}
                onKeyDown={onKeyClick}
                onMouseDown={onMouseClick}
            />
            <div className="map_img">
                <img id="source" src={state.map_metadata.im_src} />
            </div>
        </div>
    );
}

export default MapCanvas;
