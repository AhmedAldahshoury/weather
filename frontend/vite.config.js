import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    // If needed, you can configure proxy settings to your Flask backend:
    // proxy: {
    //   '/city': 'http://localhost:5000',
    //   '/forecast': 'http://localhost:5000',
    // },
  },
});
