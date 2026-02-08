/**
 * HackMate v2.0 - API Client
 * Axios configuration for backend communication.
 */

import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios';

// API base URL from environment
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Create axios instance
export const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 600000,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor
api.interceptors.request.use(
    (config: InternalAxiosRequestConfig) => {
        // Add auth token if available (future implementation)
        // const token = localStorage.getItem('token');
        // if (token) {
        //   config.headers.Authorization = `Bearer ${token}`;
        // }
        return config;
    },
    (error: AxiosError) => {
        return Promise.reject(error);
    }
);

// Response interceptor
api.interceptors.response.use(
    (response) => response,
    (error: AxiosError) => {
        // Handle common errors
        if (error.response?.status === 401) {
            // Handle unauthorized
            console.error('[API] Unauthorized');
        } else if (error.response?.status === 404) {
            console.error('[API] Resource not found');
        } else if (error.response?.status === 500) {
            console.error('[API] Server error');
        }
        return Promise.reject(error);
    }
);

// ============================================================================
// API Types
// ============================================================================

export interface Engagement {
    id: string;
    name: string;
    target: string;
    scope: string | null;
    status: 'planning' | 'active' | 'completed' | 'on_hold';
    created_at: string;
    updated_at: string;
    phase_count?: number;
    completed_phases?: number;
    finding_count?: number;
    critical_findings?: number;
}

export interface EngagementStats {
    total_engagements: number;
    active_engagements: number;
    completed_engagements: number;
    total_findings: number;
    critical_findings: number;
    high_findings: number;
}

export interface Phase {
    id: string;
    engagement_id: string;
    phase_number: number;
    name: string;
    description: string | null;
    status: 'not_started' | 'in_progress' | 'completed';
    objectives: string[] | null;
    guidance: string | null;
    notes: string | null;
    completed_at: string | null;
    created_at: string;
}

export interface Finding {
    id: string;
    engagement_id: string;
    phase_id: string | null;
    title: string;
    description: string | null;
    severity: 'critical' | 'high' | 'medium' | 'low' | 'info';
    status: 'open' | 'confirmed' | 'false_positive' | 'remediated';
    affected_component: string | null;
    evidence: string | null;
    remediation: string | null;
    cvss_score: number | null;
    cve_id: string | null;
    created_at: string;
    updated_at: string;
}

export interface Scan {
    id: string;
    engagement_id: string;
    tool: string;
    target: string;
    command: string;
    options: string | null;
    status: 'pending' | 'running' | 'completed' | 'failed' | 'cancelled';
    output: string | null;
    parsed_results: Record<string, unknown> | null;
    started_at: string | null;
    completed_at: string | null;
    created_at: string;
}

export interface ChatMessage {
    id: string;
    role: 'user' | 'assistant';
    content: string;
    created_at: string;
}

export interface CommandResult {
    id: string;
    command: string;
    output: string;
    exit_code: number;
    execution_time: number;
    executed_at: string;
}

// ============================================================================
// API Functions - Engagements
// ============================================================================

export const engagementsApi = {
    list: (params?: { status?: string; search?: string; skip?: number; limit?: number }) =>
        api.get<Engagement[]>('/api/engagements', { params }),

    get: (id: string) => api.get<Engagement>(`/api/engagements/${id}`),

    create: (data: { name: string; target: string; scope?: string }) =>
        api.post<Engagement>('/api/engagements', data),

    update: (id: string, data: Partial<Engagement>) =>
        api.put<Engagement>(`/api/engagements/${id}`, data),

    delete: (id: string) => api.delete(`/api/engagements/${id}`),

    getStats: () => api.get<EngagementStats>('/api/engagements/stats'),
};

// ============================================================================
// API Functions - Phases/Methodology
// ============================================================================

export const phasesApi = {
    list: (engagementId: string) =>
        api.get<Phase[]>(`/api/methodology/phases/${engagementId}`),

    getCurrent: (engagementId: string) =>
        api.get<Phase>(`/api/methodology/phases/${engagementId}/current`),

    update: (phaseId: string, data: Partial<Phase>) =>
        api.put<Phase>(`/api/methodology/phases/${phaseId}`, data),

    complete: (phaseId: string, notes?: string) =>
        api.post<Phase>(`/api/methodology/phases/${phaseId}/complete`, { notes }),

    getGuidance: (phaseId: string) =>
        api.post<{ guidance: string }>(`/api/methodology/phases/${phaseId}/guidance`),
};

// ============================================================================
// API Functions - Terminal
// ============================================================================

export const terminalApi = {
    execute: (engagementId: string, command: string) =>
        api.post<CommandResult>(`/api/terminal/execute/${engagementId}`, { command }),

    getHistory: (engagementId: string, params?: { skip?: number; limit?: number }) =>
        api.get<CommandResult[]>(`/api/terminal/history/${engagementId}`, { params }),

    getSuggestions: (engagementId: string, phase?: number) =>
        api.get<Array<{ command: string; description: string; category: string }>>(
            `/api/terminal/suggestions/${engagementId}`,
            { params: { phase } }
        ),
};

// ============================================================================
// API Functions - Findings
// ============================================================================

export const findingsApi = {
    list: (engagementId: string, params?: { severity?: string; status?: string; search?: string }) =>
        api.get<Finding[]>(`/api/findings/engagement/${engagementId}`, { params }),

    listAll: (params?: { severity?: string; status?: string; search?: string }) =>
        api.get<Finding[]>('/api/findings/', { params }),

    get: (id: string) => api.get<Finding>(`/api/findings/${id}`),

    create: (engagementId: string, data: Partial<Finding>) =>
        api.post<Finding>(`/api/findings/${engagementId}`, data),

    update: (id: string, data: Partial<Finding>) =>
        api.put<Finding>(`/api/findings/${id}`, data),

    delete: (id: string) => api.delete(`/api/findings/${id}`),

    bulkUpdate: (findingIds: string[], status: string) =>
        api.post<{ updated: number }>('/api/findings/bulk-update', { finding_ids: findingIds, status }),
};

// ============================================================================
// API Functions - Scans
// ============================================================================

export const scansApi = {
    list: (engagementId: string, params?: { tool?: string; status?: string }) =>
        api.get<Scan[]>(`/api/scans/engagement/${engagementId}`, { params }),

    listAll: (params?: { tool?: string; status?: string }) =>
        api.get<Scan[]>('/api/scans/', { params }),

    get: (id: string) => api.get<Scan>(`/api/scans/${id}`),

    create: (engagementId: string, data: { tool: string; target: string; options?: string }) =>
        api.post<Scan>(`/api/scans/${engagementId}`, data),

    cancel: (id: string) => api.delete(`/api/scans/${id}`),
};

// ============================================================================
// API Functions - Reports
// ============================================================================

export const reportsApi = {
    list: (engagementId: string) =>
        api.get<Array<{ id: string; report_type: string; title: string; created_at: string; engagement_id: string }>>(
            `/api/reports/engagement/${engagementId}`
        ),

    listAll: () =>
        api.get<Array<{ id: string; report_type: string; title: string; created_at: string; engagement_id: string }>>(
            '/api/reports/'
        ),

    get: (id: string) => api.get<{ id: string; content: string; report_type: string }>(`/api/reports/${id}`),

    generate: (engagementId: string, data: { report_type: string; format?: string }) =>
        api.post<{ id: string; content: string }>(`/api/reports/${engagementId}`, data),

    delete: (id: string) => api.delete(`/api/reports/${id}`),
};

// ============================================================================
// API Functions - AI
// ============================================================================

export const aiApi = {
    chat: (engagementId: string, message: string, context?: string) =>
        api.post<{ message: string; suggestions: string[] }>(`/api/ai/chat/${engagementId}`, {
            message,
            context,
        }),

    getChatHistory: (engagementId: string) =>
        api.get<ChatMessage[]>(`/api/ai/chat/${engagementId}`),

    analyzeOutput: (engagementId: string, tool: string, output: string) =>
        api.post<{ summary: string; findings: unknown[]; next_steps: string[]; risk_level: string }>(
            `/api/ai/analyze-output/${engagementId}`,
            { tool, output }
        ),

    getPhaseGuidance: (engagementId: string, phaseNumber?: number) =>
        api.post<{ phase_number: number; phase_name: string; guidance: string }>(
            `/api/ai/phase-guidance/${engagementId}${phaseNumber ? `?phase_number=${phaseNumber}` : ''}`
        ),

    suggestNextScan: (engagementId: string) =>
        api.post<{ tool: string; command: string; reason: string }>(`/api/ai/suggest-next-scan/${engagementId}`),
};
