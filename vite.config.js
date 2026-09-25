import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const rootDir = fileURLToPath(new URL('.', import.meta.url))

export default defineConfig({
  plugins: [react()],
  // LamarIS uses a custom subdomain, so assets must resolve from the domain root.
  base: '/',
  build: {
    rollupOptions: {
      input: {
        main: resolve(rootDir, 'index.html'),
        admin: resolve(rootDir, 'admin.html'),
      },
    },
  },
})
