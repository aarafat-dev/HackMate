/**
 * HackMate v2.0 - Engagement Detail Page
 */

'use client';

import { useState } from 'react';
import { useParams } from 'next/navigation';
import { useQuery } from '@tanstack/react-query';
import { Card, StatusBadge, SeverityBadge, Button } from '@/components/ui';
import { engagementsApi, phasesApi, findingsApi, aiApi, type Engagement, type Phase, type Finding } from '@/lib/api';
import { formatRelativeTime, cn } from '@/lib/utils';
import Link from 'next/link';
import {
    Target,
    ArrowLeft,
    Terminal,
    Bug,
    Radar,
    FileText,
    MessageSquare,
    CheckCircle2,
    Clock,
    AlertTriangle,
    ChevronDown,
    ChevronUp,
    Sparkles,
} from 'lucide-react';

export default function EngagementDetailPage() {
    const params = useParams();
    const id = params.id as string;

    const [expandedPhaseId, setExpandedPhaseId] = useState<string | null>(null);
    const [guidanceMap, setGuidanceMap] = useState<Record<string, string>>({});
    const [loadingGuidance, setLoadingGuidance] = useState<Record<string, boolean>>({});
    const [completingPhaseId, setCompletingPhaseId] = useState<string | null>(null);

    const togglePhase = async (phase: Phase) => {
        if (expandedPhaseId === phase.id) {
            setExpandedPhaseId(null);
            return;
        }

        setExpandedPhaseId(phase.id);

        if (!guidanceMap[phase.id]) {
            setLoadingGuidance(prev => ({ ...prev, [phase.id]: true }));
            try {
                const res = await aiApi.getPhaseGuidance(id, phase.phase_number);
                setGuidanceMap(prev => ({ ...prev, [phase.id]: res.data.guidance }));
            } catch (error) {
                console.error("Failed to fetch guidance:", error);
            } finally {
                setLoadingGuidance(prev => ({ ...prev, [phase.id]: false }));
            }
        }
    };

    const handleCompletePhase = async (phaseId: string) => {
        setCompletingPhaseId(phaseId);
        try {
            await phasesApi.complete(phaseId);
            // Refresh engagement and phases
            refetchEngagement();
            refetchPhases();
        } catch (error) {
            console.error("Failed to complete phase:", error);
        } finally {
            setCompletingPhaseId(null);
        }
    };

    // Fetch engagement
    const { data: engagement, isLoading: engagementLoading, refetch: refetchEngagement } = useQuery<Engagement>({
        queryKey: ['engagement', id],
        queryFn: async () => {
            const res = await engagementsApi.get(id);
            return res.data;
        },
    });

    // Fetch phases
    const { data: phases, refetch: refetchPhases } = useQuery<Phase[]>({
        queryKey: ['phases', id],
        queryFn: async () => {
            const res = await phasesApi.list(id);
            return res.data;
        },
        enabled: !!id,
    });

    // Fetch findings
    const { data: findings } = useQuery<Finding[]>({
        queryKey: ['findings', id],
        queryFn: async () => {
            const res = await findingsApi.list(id);
            return res.data;
        },
        enabled: !!id,
    });

    if (engagementLoading) {
        return (
            <div className="flex items-center justify-center h-64">
                <div className="animate-spin w-8 h-8 border-2 border-primary border-t-transparent rounded-full" />
            </div>
        );
    }

    if (!engagement) {
        return (
            <div className="text-center py-12">
                <AlertTriangle className="mx-auto text-severity-critical" size={48} />
                <h2 className="mt-4 text-xl font-bold text-primary">Engagement Not Found</h2>
                <Link href="/engagements" className="btn-primary mt-4 inline-block">
                    Back to Engagements
                </Link>
            </div>
        );
    }

    const currentPhase = phases?.find((p) => p.status === 'in_progress');
    const completedPhases = phases?.filter((p) => p.status === 'completed').length || 0;
    const criticalFindings = findings?.filter((f) => f.severity === 'critical').length || 0;
    const highFindings = findings?.filter((f) => f.severity === 'high').length || 0;

    return (
        <div className="space-y-6">
            {/* Header */}
            <div>
                <Link
                    href="/engagements"
                    className="inline-flex items-center gap-2 text-sm text-muted-foreground hover:text-primary transition-colors"
                >
                    <ArrowLeft size={16} />
                    Back to Engagements
                </Link>
                <div className="flex items-start justify-between mt-4">
                    <div>
                        <h1 className="text-2xl font-bold text-primary flex items-center gap-3">
                            <Target size={28} />
                            {engagement.name}
                        </h1>
                        <p className="text-muted-foreground font-mono mt-1">
                            Target: {engagement.target}
                        </p>
                    </div>
                    <StatusBadge status={engagement.status} />
                </div>
            </div>

            {/* Stats Row */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <Card className="p-4">
                    <div className="flex items-center gap-3">
                        <Clock className="text-primary" size={20} />
                        <div>
                            <p className="text-xs text-muted-foreground">PHASE</p>
                            <p className="text-lg font-bold text-primary">
                                {currentPhase?.phase_number || 0}/8
                            </p>
                        </div>
                    </div>
                </Card>
                <Card className="p-4">
                    <div className="flex items-center gap-3">
                        <CheckCircle2 className="text-status-completed" size={20} />
                        <div>
                            <p className="text-xs text-muted-foreground">COMPLETED</p>
                            <p className="text-lg font-bold text-primary">{completedPhases} phases</p>
                        </div>
                    </div>
                </Card>
                <Card className="p-4">
                    <div className="flex items-center gap-3">
                        <Bug className="text-severity-high" size={20} />
                        <div>
                            <p className="text-xs text-muted-foreground">FINDINGS</p>
                            <p className="text-lg font-bold text-primary">{findings?.length || 0}</p>
                        </div>
                    </div>
                </Card>
                <Card className="p-4">
                    <div className="flex items-center gap-3">
                        <AlertTriangle className="text-severity-critical" size={20} />
                        <div>
                            <p className="text-xs text-muted-foreground">CRITICAL</p>
                            <p className="text-lg font-bold text-severity-critical">{criticalFindings}</p>
                        </div>
                    </div>
                </Card>
            </div>

            {/* Main Content */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* PTES Phases */}
                <div className="lg:col-span-2">
                    <Card title="PTES Methodology" icon={<CheckCircle2 size={16} />}>
                        <div className="space-y-2">
                            {phases?.map((phase) => (
                                <div key={phase.id} className="border border-primary/10 rounded overflow-hidden transition-all">
                                    <div
                                        onClick={() => togglePhase(phase)}
                                        className={cn(
                                            'flex items-center gap-4 p-3 cursor-pointer hover:bg-white/5 transition-colors',
                                            phase.status === 'completed'
                                                ? 'bg-status-completed/5'
                                                : phase.status === 'in_progress'
                                                    ? 'bg-primary/10'
                                                    : ''
                                        )}
                                    >
                                        <div
                                            className={cn(
                                                'w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold',
                                                phase.status === 'completed'
                                                    ? 'bg-status-completed text-black'
                                                    : phase.status === 'in_progress'
                                                        ? 'bg-primary text-black'
                                                        : 'bg-muted text-muted-foreground'
                                            )}
                                        >
                                            {phase.phase_number}
                                        </div>
                                        <div className="flex-1">
                                            <h4
                                                className={cn(
                                                    'font-medium',
                                                    phase.status === 'in_progress' ? 'text-primary' : 'text-foreground'
                                                )}
                                            >
                                                {phase.name}
                                            </h4>
                                            <p className="text-xs text-muted-foreground">
                                                {phase.description?.substring(0, 60)}...
                                            </p>
                                        </div>
                                        <StatusBadge status={phase.status} />
                                        {expandedPhaseId === phase.id ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                                    </div>

                                    {/* Expanded Content with Guidance */}
                                    {expandedPhaseId === phase.id && (
                                        <div className="p-4 bg-black/40 border-t border-primary/10 text-sm space-y-4">
                                            <div className="flex items-start gap-3">
                                                <Sparkles className="text-purple-400 mt-1 flex-shrink-0" size={16} />
                                                <div className="flex-1 space-y-2">
                                                    <h5 className="font-semibold text-purple-400">AI Guidance</h5>
                                                    {loadingGuidance[phase.id] ? (
                                                        <div className="flex items-center gap-2 text-muted-foreground">
                                                            <div className="animate-spin w-3 h-3 border border-current border-t-transparent rounded-full" />
                                                            Generating implementation steps...
                                                        </div>
                                                    ) : (
                                                        <div className="prose prose-invert prose-sm max-w-none text-muted-foreground">
                                                            {guidanceMap[phase.id] ? (
                                                                <div className="whitespace-pre-wrap">{guidanceMap[phase.id]}</div>
                                                            ) : (
                                                                <p>No guidance available.</p>
                                                            )}
                                                        </div>
                                                    )}
                                                </div>
                                            </div>

                                            <div className="flex items-center justify-between pt-2">
                                                <div className="flex items-center gap-4">
                                                    <Link
                                                        href={`/terminal?engagement=${id}`}
                                                        className="text-xs flex items-center gap-1 text-primary hover:underline hover:text-primary-bright"
                                                    >
                                                        <Terminal size={12} />
                                                        Open Terminal
                                                    </Link>

                                                    {phase.phase_number === 7 && (
                                                        <Link
                                                            href={`/reports/new?engagement=${id}`}
                                                            className="text-xs flex items-center gap-1 text-status-active hover:underline hover:text-primary"
                                                        >
                                                            <FileText size={12} />
                                                            Generate Report
                                                        </Link>
                                                    )}
                                                </div>

                                                {phase.status !== 'completed' && (
                                                    <Button
                                                        size="sm"
                                                        onClick={(e) => {
                                                            e.stopPropagation();
                                                            handleCompletePhase(phase.id);
                                                        }}
                                                        disabled={completingPhaseId === phase.id}
                                                        className="h-8 text-[11px] font-bold tracking-wider"
                                                    >
                                                        {completingPhaseId === phase.id ? (
                                                            <div className="flex items-center gap-2">
                                                                <div className="animate-spin w-3 h-3 border-2 border-primary-foreground border-t-transparent rounded-full" />
                                                                COMPLETING...
                                                            </div>
                                                        ) : (
                                                            <div className="flex items-center gap-1">
                                                                <CheckCircle2 size={14} />
                                                                MARK AS DONE
                                                            </div>
                                                        )}
                                                    </Button>
                                                )}

                                                {phase.status === 'completed' && (
                                                    <div className="text-[10px] text-status-completed flex items-center gap-1 font-mono">
                                                        <CheckCircle2 size={12} />
                                                        COMPLETED {phase.completed_at ? formatRelativeTime(phase.completed_at) : ''}
                                                    </div>
                                                )}
                                            </div>
                                        </div>
                                    )}
                                </div>
                            ))}
                        </div>
                    </Card>
                </div>

                {/* Side Panel */}
                <div className="space-y-6">
                    {/* Quick Actions */}
                    <Card title="Quick Actions" icon={<Terminal size={16} />}>
                        <div className="space-y-2">
                            <Link
                                href={`/terminal?engagement=${id}`}
                                className="flex items-center gap-3 p-3 bg-black/40 rounded border border-primary/20 hover:border-primary/40 transition-colors"
                            >
                                <Terminal className="text-primary" size={18} />
                                <span className="text-sm">Open Terminal</span>
                            </Link>
                            <Link
                                href={`/findings?engagement=${id}`}
                                className="flex items-center gap-3 p-3 bg-black/40 rounded border border-primary/20 hover:border-primary/40 transition-colors"
                            >
                                <Bug className="text-severity-high" size={18} />
                                <span className="text-sm">View Findings</span>
                            </Link>
                            <Link
                                href={`/scans?engagement=${id}`}
                                className="flex items-center gap-3 p-3 bg-black/40 rounded border border-primary/20 hover:border-primary/40 transition-colors"
                            >
                                <Radar className="text-primary" size={18} />
                                <span className="text-sm">Run Scans</span>
                            </Link>
                            <Link
                                href={`/ai?engagement=${id}`}
                                className="flex items-center gap-3 p-3 bg-black/40 rounded border border-primary/20 hover:border-primary/40 transition-colors"
                            >
                                <MessageSquare className="text-status-active" size={18} />
                                <span className="text-sm">AI Assistant</span>
                            </Link>
                            <Link
                                href={`/reports?engagement=${id}`}
                                className="flex items-center gap-3 p-3 bg-black/40 rounded border border-primary/20 hover:border-primary/40 transition-colors"
                            >
                                <FileText className="text-primary" size={18} />
                                <span className="text-sm">Generate Report</span>
                            </Link>
                        </div>
                    </Card>

                    {/* Recent Findings */}
                    <Card title="Recent Findings" icon={<Bug size={16} />}>
                        {findings && findings.length > 0 ? (
                            <div className="space-y-2">
                                {findings.slice(0, 5).map((finding) => (
                                    <div
                                        key={finding.id}
                                        className="p-3 bg-black/40 rounded border border-primary/10"
                                    >
                                        <div className="flex items-start justify-between gap-2">
                                            <h4 className="text-sm font-medium text-primary truncate">
                                                {finding.title}
                                            </h4>
                                            <SeverityBadge severity={finding.severity} />
                                        </div>
                                        <p className="text-xs text-muted-foreground mt-1">
                                            {formatRelativeTime(finding.created_at)}
                                        </p>
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <p className="text-sm text-muted-foreground py-4 text-center">
                                No findings yet
                            </p>
                        )}
                    </Card>
                </div>
            </div>
        </div>
    );
}
