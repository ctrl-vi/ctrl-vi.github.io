// @ts-check
import { defineConfig } from 'astro/config';
import partytown from '@astrojs/partytown';
import { unified } from "@astrojs/markdown-remark";
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import remarkInline from '@plugins/inline-code';
import { fileURLToPath } from 'node:url';

import mdx from '@astrojs/mdx';

// https://astro.build/config
export default defineConfig({
  site: 'https://ctrl-vi.github.io',
  integrations: [
    partytown(),
    mdx({
      remarkPlugins: [remarkInline, remarkMath],
      rehypePlugins: [rehypeKatex],
    }),
  ],
  vite: {
    resolve: {
      alias: {
        '@components': fileURLToPath(new URL('./src/components', import.meta.url)),
        '@assets': fileURLToPath(new URL('./src/assets', import.meta.url)),
        '@cardIcons': fileURLToPath(new URL('./src/assets/cardIcons', import.meta.url)),
        '@public': fileURLToPath(new URL('./public', import.meta.url)),
        '@styles': fileURLToPath(new URL('./src/styles', import.meta.url)),
        '@plugins': fileURLToPath(new URL('./src/plugins', import.meta.url))
      }
    }
  },
  markdown: {
    processor: unified({
      remarkPlugins: [remarkInline, remarkMath],
      rehypePlugins: [rehypeKatex],
    }),
    syntaxHighlight: {
      type: 'shiki',
      excludeLangs: []
    },
    shikiConfig: {
      theme: 'github-light',
    }
  }
});