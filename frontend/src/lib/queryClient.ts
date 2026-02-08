/**
 * HackMate v2.0 - TanStack Query Client
 * React Query configuration for data fetching.
 */

'use client';

import { QueryClient } from '@tanstack/react-query';

function makeQueryClient() {
    return new QueryClient({
        defaultOptions: {
            queries: {
                // Data is considered fresh for 1 minute
                staleTime: 60 * 1000,
                // Retry failed requests 2 times
                retry: 2,
                // Refetch on window focus
                refetchOnWindowFocus: true,
            },
            mutations: {
                retry: 1,
            },
        },
    });
}

let browserQueryClient: QueryClient | undefined = undefined;

export function getQueryClient() {
    if (typeof window === 'undefined') {
        // Server: always make a new query client
        return makeQueryClient();
    } else {
        // Browser: make a new query client if we don't already have one
        if (!browserQueryClient) browserQueryClient = makeQueryClient();
        return browserQueryClient;
    }
}
