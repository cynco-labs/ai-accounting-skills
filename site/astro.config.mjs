// @ts-check
import { defineConfig } from "astro/config"

/**
 * Static Astro site → Cloudflare Pages (Vite under the hood).
 * Build output: dist/  ·  Deploy: npm run deploy
 *
 * For SSR / Workers bindings later:
 *   npx astro add cloudflare
 */
export default defineConfig({
  output: "static",
  site: "https://ai-accounting-skills.pages.dev",
  build: {
    format: "directory",
    inlineStylesheets: "auto",
  },
  vite: {
    build: {
      cssMinify: true,
    },
  },
  server: {
    port: 4321,
    host: true,
  },
})
