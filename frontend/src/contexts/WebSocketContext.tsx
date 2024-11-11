import React, { createContext, useContext, useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { RootState } from "../store";

interface WebSocketContextType {
  lastMessage: any;
  sendMessage: (message: any) => void;
  connected: boolean;
}

const WebSocketContext = createContext<WebSocketContextType>({
  lastMessage: null,
  sendMessage: () => {},
  connected: false,
});

export const WebSocketProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [ws, setWs] = useState<WebSocket | null>(null);
  const [connected, setConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState<any>(null);
  const auth = useSelector((state: RootState) => state.auth);

  useEffect(() => {
    if (auth.token) {
      const wsProtocol = window.location.protocol === "https:" ? "wss:" : "ws:";
      // check development or production
      console.log("NODE_ENV:", process.env.NODE_ENV);
      const wsUrl = `${wsProtocol}//${
        process.env.NODE_ENV === "development"
          ? "localhost:8000"
          : window.location.host
      }/api/v1/ws/${auth.token}`;
      //const wsUrl = `${wsProtocol}//${window.location.host}/api/v1/ws/${auth.token}`;
      // const wsUrl = `ws://localhost:8000/api/v1/ws/${auth.token}`;

      console.log("WebSocket URL:", wsUrl);
      const websocket = new WebSocket(wsUrl);

      websocket.onopen = () => {
        console.log("WebSocket Connected");
        setConnected(true);
      };

      websocket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        setLastMessage(data);
      };

      websocket.onclose = () => {
        console.log("WebSocket Disconnected");
        setConnected(false);
      };

      websocket.onerror = (error) => {
        console.error("WebSocket Error:", error);
      };

      setWs(websocket);

      return () => {
        websocket.close();
      };
    }
  }, [auth.token]);

  const sendMessage = (message: any) => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify(message));
    }
  };

  return (
    <WebSocketContext.Provider value={{ lastMessage, sendMessage, connected }}>
      {children}
    </WebSocketContext.Provider>
  );
};

export const useWebSocket = () => useContext(WebSocketContext);
