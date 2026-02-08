/**
 * HackMate v2.0 - Terminal Page
 */

'use client';

import { useState, useRef, useEffect, Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import { useMutation, useQuery } from '@tanstack/react-query';
import { Card } from '@/components/ui';
import { terminalApi, aiApi } from '@/lib/api';
import { Terminal as TerminalIcon, Send, Clock, Sparkles } from 'lucide-react';

function TerminalContent() {
    const searchParams = useSearchParams();
    const engagementId = searchParams.get('engagement') || 'default';
    const [command, setCommand] = useState('');
    const [history, setHistory] = useState<Array<{ type: 'input' | 'output'; content: string; exitCode?: number }>>([]);
    const outputRef = useRef<HTMLDivElement>(null);
    const inputRef = useRef<HTMLInputElement>(null);

    // Fetch command history
    const { data: commandHistory } = useQuery({
        queryKey: ['commandHistory', engagementId],
        queryFn: async () => {
            const res = await terminalApi.getHistory(engagementId);
            return res.data;
        },
        enabled: !!engagementId && engagementId !== 'default',
    });

    // Sync history from API
    useEffect(() => {
        if (commandHistory) {
            // Backend returns newest first, so we reverse it
            const formatted = commandHistory.slice().reverse().flatMap((entry: any) => [
                { type: 'input' as const, content: entry.command },
                { type: 'output' as const, content: entry.output, exitCode: entry.exit_code },
            ]);
            setHistory(formatted);
        }
    }, [commandHistory]);

    // Execute command mutation
    const executeMutation = useMutation({
        mutationFn: async (cmd: string) => {
            const res = await terminalApi.execute(engagementId, cmd);
            return res.data;
        },
        onSuccess: (result) => {
            setHistory((prev) => [
                ...prev,
                {
                    type: 'output',
                    content: result.output || '[No output]',
                    exitCode: result.exit_code,
                },
            ]);
        },
        onError: (error: Error) => {
            setHistory((prev) => [
                ...prev,
                {
                    type: 'output',
                    content: `[ERROR] ${error.message}`,
                    exitCode: 1,
                },
            ]);
        },
    });

    // AI Analyze mutation
    const analyzeMutation = useMutation({
        mutationFn: async (data: { output: string; tool: string }) => {
            const res = await aiApi.analyzeOutput(engagementId, data.tool, data.output);
            return res.data;
        },
        onSuccess: (result: any) => {
            const formattedOutput = `[AI ANALYSIS]

SUMMARY: ${result.summary}

RISK LEVEL: ${result.risk_level.toUpperCase()}

FINDINGS:
${result.findings.map((f: any) => `- ${f.title} (${f.severity})`).join('\n') || 'None'}

NEXT STEPS:
${result.next_steps.map((s: string) => `- ${s}`).join('\n')}`;

            setHistory((prev) => [
                ...prev,
                {
                    type: 'output',
                    content: formattedOutput,
                    exitCode: 0,
                },
            ]);
        },
        onError: (error: Error) => {
            setHistory((prev) => [
                ...prev,
                {
                    type: 'output',
                    content: `[ERROR] AI Analysis failed: ${error.message}`,
                    exitCode: 1,
                },
            ]);
        },
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!command.trim()) return;

        if (command.trim().toLowerCase() === 'clear') {
            setHistory([]);
            setCommand('');
            return;
        }

        if (command.trim().toLowerCase() === 'ai analyze') {
            // Find last output
            const lastOutput = [...history].reverse().find((h) => h.type === 'output');

            if (!lastOutput) {
                setHistory((prev) => [
                    ...prev,
                    { type: 'input', content: command },
                    { type: 'output', content: '[!] No output to analyze.', exitCode: 1 }
                ]);
                setCommand('');
                return;
            }

            // Attempt to find the tool command
            const outputIndex = history.indexOf(lastOutput);
            const inputEntry = history[outputIndex - 1];
            const tool = inputEntry?.type === 'input' ? inputEntry.content.split(' ')[0] : 'terminal';

            setHistory((prev) => [...prev, { type: 'input', content: command }]);
            analyzeMutation.mutate({ output: lastOutput.content, tool });
            setCommand('');
            return;
        }

        setHistory((prev) => [...prev, { type: 'input', content: command }]);
        executeMutation.mutate(command);
        setCommand('');
    };

    useEffect(() => {
        if (outputRef.current) {
            outputRef.current.scrollTop = outputRef.current.scrollHeight;
        }
    }, [history]);

    useEffect(() => {
        inputRef.current?.focus();
    }, []);

    return (
        <div className="h-[calc(100vh-5rem)] flex flex-col space-y-4">
            <div>
                <h1 className="text-2xl font-bold text-primary flex items-center gap-3">
                    <TerminalIcon size={28} />
                    Terminal
                </h1>
                <p className="text-muted-foreground mt-1">
                    $ secure-shell --engagement {engagementId}
                </p>
            </div>

            <Card className="flex-1 flex flex-col overflow-hidden" noPadding>
                <div className="flex items-center gap-2 px-4 py-2 bg-black/60 border-b border-primary/20">
                    <div className="flex gap-1.5">
                        <div className="w-3 h-3 rounded-full bg-severity-critical" />
                        <div className="w-3 h-3 rounded-full bg-severity-medium" />
                        <div className="w-3 h-3 rounded-full bg-status-active" />
                    </div>
                    <span className="text-xs text-muted-foreground ml-2">
                        hackmate-terminal — {engagementId}
                    </span>
                </div>

                <div
                    ref={outputRef}
                    className="flex-1 p-4 overflow-y-auto font-mono text-sm space-y-2"
                    onClick={() => inputRef.current?.focus()}
                >
                    <div className="text-primary/50">{`╔══════════════════════════════════════════════════════════════╗`}</div>
                    <div className="text-primary/50">{`║  HACKMATE TERMINAL v2.0                                       ║`}</div>
                    <div className="text-primary/50">{`║  Type 'help' for available commands                           ║`}</div>
                    <div className="text-primary/50">{`╚══════════════════════════════════════════════════════════════╝`}</div>
                    <div className="text-primary/30 text-xs mt-2">[!] Only authorized testing is permitted.</div>
                    <div className="h-4" />

                    {history.map((entry, i) => (
                        <div key={i} className={entry.type === 'input' ? 'text-primary' : 'text-foreground/80'}>
                            {entry.type === 'input' ? (
                                <div className="flex items-center gap-2">
                                    <span className="text-status-active">$</span>
                                    <span>{entry.content}</span>
                                </div>
                            ) : (
                                <div className="pl-4 whitespace-pre-wrap">
                                    {entry.content}
                                    {entry.exitCode !== undefined && entry.exitCode !== 0 && (
                                        <span className="text-severity-critical text-xs ml-2">[exit: {entry.exitCode}]</span>
                                    )}
                                </div>
                            )}
                        </div>
                    ))}

                    {(executeMutation.isPending || analyzeMutation.isPending) && (
                        <div className="flex items-center gap-2 text-primary/50">
                            {analyzeMutation.isPending ? (
                                <Sparkles className="animate-pulse text-purple-400" size={14} />
                            ) : (
                                <div className="animate-spin w-3 h-3 border border-primary border-t-transparent rounded-full" />
                            )}
                            <span>{analyzeMutation.isPending ? 'Analyzing output...' : 'Executing...'}</span>
                        </div>
                    )}
                </div>

                <form onSubmit={handleSubmit} className="flex items-center gap-2 px-4 py-3 bg-black/60 border-t border-primary/20">
                    <span className="text-status-active font-bold">$</span>
                    <input
                        ref={inputRef}
                        type="text"
                        value={command}
                        onChange={(e) => setCommand(e.target.value)}
                        disabled={executeMutation.isPending}
                        placeholder="Enter command..."
                        className="flex-1 bg-transparent border-none outline-none text-primary placeholder-primary/30 font-mono"
                        autoComplete="off"
                        spellCheck={false}
                    />
                    <button
                        type="submit"
                        disabled={executeMutation.isPending || !command.trim()}
                        className="p-2 text-primary hover:bg-primary/10 rounded transition-colors disabled:opacity-50"
                    >
                        <Send size={16} />
                    </button>
                </form>
            </Card>

            <Card className="p-3">
                <div className="flex items-center gap-4 text-xs text-muted-foreground">
                    <span className="flex items-center gap-1">
                        <TerminalIcon size={12} />
                        Available: nmap, nikto, gobuster, nuclei, curl, dig, whois
                    </span>
                    <span className="flex items-center gap-1">
                        <Clock size={12} />
                        Timeout: 10 min
                    </span>
                </div>
            </Card>
        </div>
    );
}

export default function TerminalPage() {
    return (
        <Suspense fallback={<div className="text-primary/50">Loading terminal...</div>}>
            <TerminalContent />
        </Suspense>
    );
}
