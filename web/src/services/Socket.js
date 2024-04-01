import io from "socket.io-client";

class Socket {
  static socket = null;

  static init(username) {
    Socket.socket = io("http://localhost:5000")
    // console.log("Socket initialized", Socket.socket);
  }

  static getSocket() {
    return Socket.socket;
  }
}

export default Socket;
