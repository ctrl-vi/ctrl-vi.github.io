// Declarations to allow importing image files and the @cardIcons alias in TypeScript

// Alias pattern for @cardIcons/* (maps to src/assets/cardIcons/* in tsconfig)
declare module '@cardIcons/*' {
  const src: string;
  export default src;
}

// Generic image module declarations
declare module '*.png' {
  const src: string;
  export default src;
}

declare module '*.jpg' {
  const src: string;
  export default src;
}

declare module '*.jpeg' {
  const src: string;
  export default src;
}

declare module '*.webp' {
  const src: string;
  export default src;
}

declare module '*.svg' {
  const src: string;
  export default src;
}
