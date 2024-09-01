import {defineConfig} from 'vite';
import vue from '@vitejs/plugin-vue';
import {resolve} from "path";

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": resolve(__dirname, "src"),
    },
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          // Выделяем Vue в отдельный бандл
          'vue-vendor': ['vue'],
          // Выделяем другие зависимости в отдельный бандл
          'vendor': ['vue-router', 'axios'],
        },
      },
    },
    // Увеличиваем лимит предупреждения для размера чанков, если необходимо
    chunkSizeWarningLimit: 600,
  },
});
