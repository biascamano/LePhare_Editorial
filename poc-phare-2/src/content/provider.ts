import { mockProvider } from './mock-provider';
import { wordpressProvider } from './wordpress-provider';
import type { ContentProvider } from './types';

const source = (import.meta.env.PHARE_SOURCE ?? 'mock') as string;

if (source !== 'mock' && source !== 'wordpress') throw new Error(`PHARE_SOURCE inconnu : ${source} (attendu : mock | wordpress)`);

export const content: ContentProvider = source === 'wordpress' ? wordpressProvider : mockProvider;
export type * from './types';
