import React from "react";
import { BrowserRouter } from "react-router-dom";
import { Provider } from "react-redux";
import { store } from "./store";
import AuthRoutes from "./routes/AuthRoutes";
import ErrorBoundary from "./components/ErrorBoundary";
import { WebSocketProvider } from "./contexts/WebSocketContext";
// import AuthDebug from "./components/AuthDebug";

const App: React.FC = () => {
  return (
    <Provider store={store}>
      <WebSocketProvider>
        <BrowserRouter>
          <ErrorBoundary>
            <AuthRoutes sx={"h-screen max-h-[40vh]"} />
          </ErrorBoundary>
        </BrowserRouter>
      </WebSocketProvider>
    </Provider>
  );
};

export default App;
