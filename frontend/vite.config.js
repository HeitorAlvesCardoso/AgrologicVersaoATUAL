import { defineConfig } from 'vite'

export default defineConfig({
  server: {
    allowedHosts: ['.trycloudflare.com'],
    proxy: {
      '/bois': 'http://127.0.0.1:5000',
    },
  },
  build: {
    rollupOptions: {
      input: {
        home: 'index.html',
        conta: 'conta.html',
        negociar: 'negociar.html',
      },
    },
  },
})
