import { defineConfig } from 'vite'

export default defineConfig({
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
