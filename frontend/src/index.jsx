import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import { BaseProvider, LightTheme } from 'baseui';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BaseProvider theme={LightTheme}>
      <App />
    </BaseProvider>
  </React.StrictMode>
);
