// Menu.js

import React from "react";
import "./Canvas.css";
import "./Menu.css";
import { CanvasContext } from "../../providers/CanvasProvider";

const Menu = (props) => {
  const context = React.useContext(CanvasContext);

  return (
    <div className="Menu">
      {props.word ? (
        <h2 className="menu-word-header">
          Draw: <span className="word">{props.word}</span>
        </h2>
      ) : null}
      {props.roles ? (
        <h2 className="menu-roles">
          Roles: <span className="roles">{props.roles.join(" ")}</span>
        </h2>
      ) : null}
      {props.artist ? (
        <h2 className="menu-artist">
          <span className="artist">{props.artist} is drawing</span>
        </h2>
      ) : null}
      {props.artist == props.name ? (
        <form id="stylepicker-container">
          <label htmlFor="color-picker">Brush color</label>
          <input
            id="color-picker"
            type="color"
            value={context.color}
            onChange={context.handleColorChange}
          />
          <label htmlFor="brush-size"> Brush size</label>
          <input
            id="brush-size"
            type="range"
            min={5}
            max={30}
            value={context.width}
            onChange={context.handleBrushSizeChange}
          />
        </form>
      ) : null}

      {/* <label>Color </label> 
            <input 
                type="color"
                onChange={(e) => { 
                    setLineColor(e.target.value); 
                }} 
            /> 
            <label>Size </label> 
            <input 
                type="range"
                min="3"
                max="40"
                onChange={(e) => { 
                    setLineWidth(e.target.value); 
                }} 
            /> 
            <label>Opacity</label> 
            <input 
                type="range"
                min="1"
                max="100"
                onChange={(e) => { 
                    setLineOpacity(e.target.value / 100); 
                }} 
            /> 
            <button onClick={() => { 
                clearCanvas();
            }}> 
                Clear
            </button> */}
    </div>
  );
};

export default Menu;
