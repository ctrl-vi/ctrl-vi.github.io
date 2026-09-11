// @ts-check
import { defineConfig } from 'astro/config';
import partytown from '@astrojs/partytown';
import { unified } from "@astrojs/markdown-remark";
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import { fileURLToPath } from 'node:url';

import mdx from '@astrojs/mdx';
import rehypeShiki from '@shikijs/rehype';

// https://astro.build/config
export default defineConfig({
  site: 'https://ctrl-vi.github.io',
  integrations: [
    partytown(),
    mdx({
      remarkPlugins: [remarkMath],
      rehypePlugins: [
        rehypeKatex,
        [rehypeShiki,
        {
          theme: 'github-light',
          inline: 'tailing-curly-colon'
        }]
      ],
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
    syntaxHighlight: false,
    processor: unified({
      remarkPlugins: [remarkMath],
      rehypePlugins: [ 
        [rehypeShiki,
        {
          theme: 'github-light',
          inline: 'tailing-curly-colon'
        }],
        rehypeKatex,
      ],
    }),
  }
});