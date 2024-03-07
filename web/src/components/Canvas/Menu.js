// Menu.js 
  
import React from "react"; 
import "./Canvas.css"; 
  
const Menu = ({ setLineColor, setLineWidth, 
    setLineOpacity, clearCanvas }) => {
    return ( 
        <div className="Menu"> 
            <label>Color </label> 
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
            </button>
        </div> 
    ); 
}; 
  
export default Menu;