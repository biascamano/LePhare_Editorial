interface ImportMetaEnv {
  readonly PHARE_SOURCE?: 'mock' | 'wordpress';
  readonly PHARE_WP_URL?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
