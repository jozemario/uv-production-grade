import React from "react";
import ReactDOM from "react-dom/client";
import { Provider } from "react-redux";
import "./styles.scss";
import { store } from "./store";
import App from "./App";

const mount = (el: HTMLElement) => {
  const root = ReactDOM.createRoot(el);
  root.render(
    <React.StrictMode>
      <Provider store={store}>
        <App />
      </Provider>
    </React.StrictMode>
  );
};

// If we're in development and running in isolation,
// mount immediately
if (process.env.NODE_ENV === "development") {
  const devRoot = document.querySelector("#root");
  if (devRoot) {
    mount(devRoot as HTMLElement);
  }
}

// We're running through container
// and we should export the mount function
export { mount };
