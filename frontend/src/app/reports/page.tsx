/**
 * HackMate v2.0 - Reports Page
 */

'use client';

import { Suspense, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { useQuery } from '@tanstack/react-query';
import { Card, Button } from '@/components/ui';
import { reportsApi, engagementsApi, type Engagement } from '@/lib/api';
import { formatRelativeTime } from '@/lib/utils';
import { FileText, Download, Eye, FileSearch, Target, X, Terminal } from 'lucide-react';

function ReportsContent() {
    const searchParams = useSearchParams();
    const engagementId = searchParams.get('engagement') || '';
    const [selectedReport, setSelectedReport] = useState<any>(null);

    const { data: reports, isLoading } = useQuery({
        queryKey: ['reports', engagementId],
        queryFn: async () => {
            if (engagementId) {
                const res = await reportsApi.list(engagementId);
                return res.data;
            } else {
                const res = await reportsApi.listAll();
                return res.data;
            }
        },
    });

    const { data: engagements } = useQuery<Engagement[]>({
        queryKey: ['engagements'],
        queryFn: async () => {
            const res = await engagementsApi.list();
            return res.data;
        },
    });

    const getEngagementName = (id: string) => {
        return engagements?.find(e => e.id === id)?.name || id.substring(0, 8);
    };

    const handleExportJSON = (report: any) => {
        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(report, null, 2));
        const downloadAnchorNode = document.createElement('a');
        downloadAnchorNode.setAttribute("href", dataStr);
        downloadAnchorNode.setAttribute("download", `${report.title.replace(/\s+/g, '_')}.json`);
        document.body.appendChild(downloadAnchorNode);
        downloadAnchorNode.click();
        downloadAnchorNode.remove();
    };

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between print:hidden">
                <div>
                    <h1 className="text-2xl font-bold text-primary flex items-center gap-3">
                        <FileText size={28} />
                        Reports
                    </h1>
                    <p className="text-muted-foreground mt-1">$ ls -l /opt/hackmate/reports/json/</p>
                </div>
            </div>

            <Card className="print:border-none print:shadow-none">
                <div className="p-4 border-b border-primary/10 bg-primary/5 flex items-center justify-between print:hidden">
                    <h3 className="text-sm font-semibold text-primary uppercase tracking-wider">
                        {engagementId ? 'Engagement Reports' : 'All Global Reports'}
                    </h3>
                    <div className="text-xs text-muted-foreground">{reports?.length || 0} reports archived</div>
                </div>

                {isLoading ? (
                    <div className="p-12 text-center">
                        <div className="animate-spin w-8 h-8 border-2 border-primary border-t-transparent rounded-full mx-auto" />
                        <p className="mt-4 text-muted-foreground font-mono text-sm">ARCHIVING SYSTEM RECORDS...</p>
                    </div>
                ) : reports && reports.length > 0 ? (
                    <div className="divide-y divide-primary/10">
                        {reports.map((report) => (
                            <div key={report.id} className="p-4 hover:bg-primary/5 transition-colors group print:break-inside-avoid">
                                <div className="flex items-center justify-between">
                                    <div className="flex items-center gap-4">
                                        <div className="w-12 h-12 bg-primary/10 rounded flex items-center justify-center border border-primary/20 group-hover:border-primary/40 print:hidden">
                                            <FileText size={24} className="text-primary" />
                                        </div>
                                        <div>
                                            <div className="flex items-center gap-2">
                                                <h4 className="font-bold text-primary">{report.title}</h4>
                                                {!engagementId && (
                                                    <span className="flex items-center gap-1 text-[10px] text-primary/40 uppercase bg-primary/5 px-1.5 py-0.5 rounded border border-primary/10">
                                                        <Target size={10} />
                                                        {getEngagementName(report.engagement_id)}
                                                    </span>
                                                )}
                                            </div>
                                            <p className="text-sm text-muted-foreground">
                                                Type: <span className="text-primary/70 uppercase text-xs font-mono">{report.report_type}</span>
                                            </p>
                                        </div>
                                    </div>
                                    <div className="flex items-center gap-4">
                                        <div className="text-right mr-4 hidden sm:block">
                                            <p className="text-xs text-muted-foreground uppercase tracking-widest">Generated</p>
                                            <p className="text-sm font-mono text-primary">{formatRelativeTime(report.created_at)}</p>
                                        </div>
                                        <div className="flex gap-2 print:hidden">
                                            <Button
                                                size="sm"
                                                variant="ghost"
                                                className="p-2 text-primary/60 hover:text-primary hover:bg-primary/10"
                                                onClick={() => setSelectedReport(report)}
                                                title="View Report"
                                            >
                                                <Eye size={18} />
                                            </Button>
                                            <Button
                                                size="sm"
                                                variant="ghost"
                                                className="p-2 text-primary/60 hover:text-primary hover:bg-primary/10"
                                                onClick={() => handleExportJSON(report)}
                                                title="Export JSON"
                                            >
                                                <Download size={18} />
                                            </Button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                ) : (
                    <div className="p-16 text-center">
                        <FileSearch className="mx-auto text-primary/20" size={64} />
                        <h4 className="mt-4 text-primary font-medium">No reports yet</h4>
                        <p className="text-sm text-muted-foreground mt-2 max-w-md mx-auto">
                            No reports have been generated for your engagements yet.
                        </p>
                    </div>
                )}
            </Card>

            {/* Report Viewer Modal */}
            {selectedReport && (
                <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in duration-200">
                    <div className="bg-[#050505] border border-primary/20 rounded-lg shadow-glow-lg w-full max-w-5xl max-h-[90vh] flex flex-col overflow-hidden border-t-primary/50">
                        {/* Modal Header */}
                        <div className="p-4 border-b border-primary/10 flex items-center justify-between bg-primary/5">
                            <div className="flex items-center gap-3">
                                <FileText size={20} className="text-primary" />
                                <div>
                                    <h2 className="font-bold text-primary leading-none">{selectedReport.title}</h2>
                                    <p className="text-[10px] text-muted-foreground mt-1 font-mono uppercase tracking-widest">
                                        ID: {selectedReport.id} • TYPE: {selectedReport.report_type}
                                    </p>
                                </div>
                            </div>
                            <div className="flex items-center gap-2">
                                <Button
                                    size="sm"
                                    variant="ghost"
                                    className="h-8 px-2 text-primary/60 hover:text-primary"
                                    onClick={() => handleExportJSON(selectedReport)}
                                >
                                    <Download size={16} className="mr-2" />
                                    JSON
                                </Button>
                                <Button
                                    size="sm"
                                    variant="ghost"
                                    className="h-8 w-8 p-0 text-primary/60 hover:text-severity-critical"
                                    onClick={() => setSelectedReport(null)}
                                >
                                    <X size={20} />
                                </Button>
                            </div>
                        </div>

                        {/* Modal Content */}
                        <div className="flex-1 overflow-y-auto p-6 scrollbar-thin scrollbar-thumb-primary/20 scrollbar-track-transparent">
                            <div className="prose prose-invert prose-primary max-w-none">
                                {/* Report Metadata Section */}
                                {selectedReport.metadata && (
                                    <div className="mb-8 grid grid-cols-2 md:grid-cols-4 gap-4 p-4 bg-primary/5 border border-primary/10 rounded font-mono">
                                        <div>
                                            <p className="text-[10px] text-muted-foreground uppercase">Findings</p>
                                            <p className="text-lg text-primary">{selectedReport.metadata.findings_count || 0}</p>
                                        </div>
                                        {selectedReport.metadata.severity_counts && Object.entries(selectedReport.metadata.severity_counts).map(([sev, count]: [string, any]) => (
                                            <div key={sev}>
                                                <p className="text-[10px] text-muted-foreground uppercase">{sev}</p>
                                                <p className={`text-lg ${sev === 'critical' ? 'text-severity-critical' :
                                                    sev === 'high' ? 'text-severity-high' :
                                                        sev === 'medium' ? 'text-severity-medium' :
                                                            'text-primary'
                                                    }`}>{count}</p>
                                            </div>
                                        ))}
                                    </div>
                                )}

                                {/* Markdown Content */}
                                <div className="whitespace-pre-wrap font-sans leading-relaxed text-primary/90">
                                    {selectedReport.content}
                                </div>
                            </div>
                        </div>

                        {/* Modal Footer */}
                        <div className="p-3 border-t border-primary/10 bg-black/40 flex justify-end">
                            <Button size="sm" onClick={() => setSelectedReport(null)}>
                                Close Terminal View
                            </Button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default function ReportsPage() {
    return (
        <Suspense fallback={<div className="text-primary/50">Loading reports...</div>}>
            <ReportsContent />
        </Suspense>
    );
}
