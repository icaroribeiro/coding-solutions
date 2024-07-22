/// <reference types="vitest" />
/// <reference types="vite/client" />
import { defineConfig } from 'vite'
import { resolve } from 'path'

// https://vitejs.dev/config/
export default defineConfig({
	build: {
		outDir: "dist",
		lib: {
      entry: resolve(__dirname, 'src/index.ts'),
      name: 'MyLib',
      fileName: 'index',
    },
    rollupOptions: {
      external: ['vue'],
      output: {
        globals: {
          vue: 'Vue',
        },
      },
    }
	},
	test: {		
    coverage: {
      reporter: ["lcov"],
    },
		typecheck: {
			tsconfig: "tsconfig.test.json"
		}
  }
})