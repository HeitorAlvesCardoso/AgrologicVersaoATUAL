import { defineConfig } from 'vite'

export default defineConfig({
  // GitHub Pages serve o site em /AgrologicVersaoATUAL/
  base: '/AgrologicVersaoATUAL/',
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
