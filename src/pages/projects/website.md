---
article: 
    publishedTime: "2025-06-19T02:07:41-08:00"
    modifiedTime: "2025-07-15T05:49:10-08:00"
    authors: ["Violet Monserate"]
    section: Personal Projects
    tags: ["astro", "html", "jsx", "vite", "css" ]
layout: '@components/MarkdownProjectLayout.astro'
title: Personal Website
description: Crafting a fast, reactive Multi-Page Application to host personal information and publish projects
seoDescription: Using Astro (HTML, JSX, Vite, CSS) for rich, fast, and efficient Multi-Page Application (MPA), crafting Astro components from scratch to streamline publishing.
image:
    src: "@assets/website/website-thumbnail.png"
    alt: "Thumbnail for Violet Monestrate's personal website, featuring the letters 'VM' and blue, white and purple swirls."
startDate: 2025-03
icons: ["astro", "html", "css", "vite", "github" ]
---
![Thumbnail for Violet Monestrate's personal website, featuring the letters 'VM' and blue, white and purple swirls.](@assets/website/website-thumbnail.png)

---

One of piece of advise I—along with every other student in STEM—consistently recieve is to build a personal website and park all my projects onto there. With this in mind, I have made this website, but it's not any ordinary website; I set myself some additional objectives:

1. **Make it snappy**: I am so sick of slow, ram-consuming websites that run thounds of lines of JavaScript, and wanted to return a more traditional form of web-development, focused more on quickly delivering information to users.

2. **Make it accessible**: I wanted to make sure that all elements of the website would be as universally usable as possible, by including good alt text in images, minimizing how much JavaScript is used, and following other aspects laid out by [the Web Content Accessibility Guidelines (WCAG)](https://www.w3.org/TR/WCAG21/). In this point, I also wanted to be easily usable on a computer, tablet, phone, or otherwise.

3. **Make it pretty**: this was probably at the bottom of my list in terms of priority, but having a pretty website would give me more practice in doing proper web-development, and also feel better at showing it off to peers, recruiters, and whomever else. 

## Why Astro?

While doing research on the different frameworks that were possible, one stuck out to me: Astro. I have experience with a couple different frameworks, including React, but was not really satisfied with how slow Single Page Applications (SPA) can feel. In addition, the website HAS to be static, as I did not want to worry about setting up a whole server to dynamically serve content. As such, I sought out a simple, lightweight Multi Page Application (MPA) framework, and stumbled across Astro.

In short, Astro does a lot of pre-processing as it creates the many different HTML files that are hosted on the static server, condensing all of the JavaScript to really reduce the load that users have to endure. It also simplifies the SEO process and ensures that different pages of my website are easily searchable in *any* given Search Engine.  

It also is just another web dev framework for me to learn, and pratice, and to generally improve as picking up new languages/frameworks. 

## GitHub Pages? Why not _____?

Another choice I made was to stick with GitHub Pages, as opposed to anything else, was because I already would be storing it on GitHub, and static website hosting is free on GitHub Pages, so might as well use it! It also has a lot of built in integration with GitHub repositories, allowing for automatic deployment when anything is pushed to the remote repository. 


## Cool Features

As I learned to make more and more components, I created a couple that I'm particularly happy with! There aren't the only components, and you can see all of those in my [GitHub repository](https://github.com/ctrl-vi/ctrl-vi.github.io). 

### Cards and Card Grid

To easily share the different projects I wanted brief overviews with thumbnails and icons that quickly share the information on all my projects. Following some principles I learned in CSE 440, I made sure to utilize whitespace to group each of the different projects together, and to give users continual feedback about what they're clicking or hoving over by using shadows, for example. Even better, the card grid itself is responsive to the size of the viewport, increasing and the decreasing the number of cards appropriately. 

If you are curious about how the code turned out, you can view the [grid component here](https://github.com/ctrl-vi/ctrl-vi.github.io/blob/main/src/components/CardGrid.astro) and the [card component here](https://github.com/ctrl-vi/ctrl-vi.github.io/blob/main/src/components/Card.astro). One of the additions that I hope to make in the near future is the ability to *filter* through the different projects, and look at ones with only specific tags. 

### Markdown Layout

To REALLY simplify the process of presenting all of the different projects I have my hands in, I created a .md layout file that not only maintains the general design and style of the entire website (with the same navigation, footer, and header), but also easily interfaces with SEO utilities, OpenGraph protocol, and more. The important information that would be used by cards or SEO utilities is included in the frontmatter in a very straightforward format that I can fill out without worrying about properly formatting HTML. 

More recently, I was trying to utilize $\LaTeX$ to show some equations, and that led to `KaTeX`, which renders math. By using another library, `remark-math`, I am simply able to write beautiful equations like 

$$
\int_{0}^{\infty} \left( \sum_{n=1}^{\infty} \frac{\alpha_n}{n^2 + \beta^2} \right) \cdot \sqrt{\frac{\pi}{2}} \, dx = \lim_{x \to \infty} \left[ e^{-\gamma x^2} + \frac{\delta}{x^2} \right] + \text{constant}
$$

with some simple code, like so:

```
$$
\int_{0}^{\infty} \left( \sum_{n=1}^{\infty} \frac{\alpha_n}{n^2 + \beta^2} \right) \cdot \sqrt{\frac{\pi}{2}} \, dx = \lim_{x \to \infty} \left[ e^{-\gamma x^2} + \frac{\delta}{x^2} \right] + \text{constant}
$$
```

Or for inline things like $\Tau$, $\Beta$, or $\Kappa$, we do `$\Tau$, $\Beta$, or $\Kappa$`.

You can look at the [markdown layout component itself here](https://github.com/ctrl-vi/ctrl-vi.github.io/blob/main/src/components/MarkdownProjectLayout.astro).