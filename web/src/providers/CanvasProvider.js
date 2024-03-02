import React, { useEffect, useState } from "react";
import Socket from "../services/Socket";
import { delay } from "../utils";
// import { GameContextProps, GameContext } from './GameProvider';

export const CanvasContext = React.createContext();

const CanvasProvider = ({children}) => {
  const socket = Socket.getSocket();
  const [isDrawing, setIsDrawing] = useState(false);
  const [ctx, setCtx] = useState(null);
  const [color, setColor] = useState("#000000");
  const [width, setWidth] = useState(10);

  useEffect(() => {
    if (ctx) {
      socket.on("lineDraw", (line) => {
        console.log("lineDraw", line);
        drawLine(line.line);
      });
      socket.on("drawingState", async (lines) => {
        for (let line of lines) {
          drawLine(line);
          await delay(100);
        }
      });
      socket.on("clearCanvas", () => {
        clearCanvas();
      });
    }
  }, [ctx]);

  const drawLine = (line) => {
    if (!ctx) return;

    ctx.strokeStyle = line.color;
    ctx.lineWidth = line.width;
    ctx.lineTo(line.x, line.y);
    ctx.stroke();

    if (line.isEnding) {
      ctx.beginPath();
    }
  };

  const draw = (ev, isEnding) => {
    if (!ctx || !isDrawing || !ev) return;

    // console.log("drawing", ev.clientX, ev.clientY, ctx.canvas.offsetLeft, ctx.canvas.offsetTop);

    const newLine = {
      x: ev.clientX - ctx.canvas.offsetLeft,
      y: ev.clientY - ctx.canvas.offsetTop,
      color,
      width,
      isEnding,
    };
    drawLine(newLine);
    // socket.emit("join_room", { username: props.name, room: props.room });
    socket.emit("lineDraw", { line: newLine, room: "367757" });
    
  };

  const clearCanvas = () => {
    if (!ctx) return;

    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
  };

  return (
    <CanvasContext.Provider
      value={{
        isDrawing,
        setIsDrawing,
        ctx,
        setCtx,
        color,
        setColor,
        width,
        setWidth,
        draw,
        clearCanvas,
      }}
    >
      {children}
    </CanvasContext.Provider>
  );
};

export default CanvasProvider;