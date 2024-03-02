import React, { useLayoutEffect } from "react";
import {
  CanvasContext,
} from "../../providers/CanvasProvider";
import "./Canvas.css";

const Canvas = (props) => {
  const context = React.useContext(CanvasContext);

  const ref = React.useRef(null);

  useLayoutEffect(() => {
    const canvas = ref.current;
    const ctx = canvas.getContext("2d");
    canvas.width = props.width;
    canvas.height = props.height;
    ctx.lineCap = "round";
    ctx.lineJoin = "round";
    ctx.strokeStyle = context.color;
    ctx.lineWidth = context.width;
    context.setCtx(ctx);
  }, []);

  return (
    <canvas
      ref={ref}
      onMouseDown={(ev) => {
        context.setIsDrawing(true);
        context.draw(ev, false);
      }}
      onMouseUp={() => {
        context.setIsDrawing(false);
        context.draw(null, true);
      }}
      onMouseMove={(ev) => {
        context.draw(ev, false);
      }}
    />
  );
};

export default Canvas;
