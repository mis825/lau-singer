import React, { useEffect } from 'react';
import Socket from '../services/Socket';

const GameProvider = ({ children }) => {
    const socket = Socket.getSocket();

    return (
        <GameContext.Provider value={{ socket }}>
            {children}
        </GameContext.Provider>
    );
}

export default GameProvider;