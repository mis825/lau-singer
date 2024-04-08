import io from "socket.io-client";

class Socket {
  static socket = null;

  static getServerURL() {
    return "http://localhost:5000";
  }

  static init(username) {
    Socket.socket = io(Socket.getServerURL());
  }

  static getSocket() {
    return Socket.socket;
  }
}

export default Socket;
