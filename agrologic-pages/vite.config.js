import { defineConfig } from 'vite'

export default defineConfig({
  // GitHub Pages serve o site em /AgrologicVersaoATUAL/
  base: '/AgrologicVersaoATUAL/',
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
