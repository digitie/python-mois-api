import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react()],
  server: {
    host: "localhost",
    port: 8610,
    strictPort: true,
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8611",
        changeOrigin: true
      }
    }
  },
  preview: {
    host: "localhost",
    port: 8610,
    strictPort: true
  }
});
