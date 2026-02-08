/**
 * HackMate v2.0 - AI Assistant Page
 */

'use client';

import { useState, useRef, useEffect, Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import { useMutation, useQuery } from '@tanstack/react-query';
import { Card } from '@/components/ui';
import { aiApi, type ChatMessage } from '@/lib/api';
import { MessageSquare, Send, Sparkles, User, Bot } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

function AIContent() {
    const searchParams = useSearchParams();
    const engagementId = searchParams.get('engagement') || 'default';
    const [message, setMessage] = useState('');
    const [messages, setMessages] = useState<Array<{ role: 'user' | 'assistant'; content: string }>>([]);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const { data: chatHistory } = useQuery({
        queryKey: ['chatHistory', engagementId],
        queryFn: async () => {
            if (engagementId === 'default') return [];
            const res = await aiApi.getChatHistory(engagementId);
            return res.data;
        },
        enabled: engagementId !== 'default',
    });

    useEffect(() => {
        if (chatHistory) {
            setMessages(chatHistory.map((m: ChatMessage) => ({ role: m.role, content: m.content })));
        }
    }, [chatHistory]);

    const sendMutation = useMutation({
        mutationFn: async (msg: string) => {
            const res = await aiApi.chat(engagementId, msg);
            return res.data;
        },
        onSuccess: (response) => {
            setMessages((prev) => [...prev, { role: 'assistant', content: response.message }]);
        },
        onError: (error: Error) => {
            setMessages((prev) => [...prev, { role: 'assistant', content: `[ERROR] ${error.message}` }]);
        },
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!message.trim() || sendMutation.isPending) return;
        setMessages((prev) => [...prev, { role: 'user', content: message }]);
        sendMutation.mutate(message);
        setMessage('');
    };

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const quickPrompts = [
        'What tools should I run for reconnaissance?',
        'Analyze my last scan results',
        'Suggest next steps for this phase',
        'Help me write a finding report',
    ];

    return (
        <div className="h-[calc(100vh-8rem)] flex flex-col space-y-4">
            <div>
                <h1 className="text-2xl font-bold text-primary flex items-center gap-3">
                    <MessageSquare size={28} />
                    AI Assistant
                </h1>
                <p className="text-muted-foreground mt-1">$ hackmate-ai --mode mentor</p>
            </div>

            <Card className="flex-1 flex flex-col overflow-hidden" noPadding>
                <div className="flex-1 overflow-y-auto p-4 space-y-4">
                    {messages.length === 0 && (
                        <div className="text-center py-8">
                            <div className="w-16 h-16 bg-primary/20 rounded-full flex items-center justify-center mx-auto mb-4 border border-primary/50">
                                <Sparkles className="text-primary" size={32} />
                            </div>
                            <h3 className="text-lg font-semibold text-primary">HACKMATE AI</h3>
                            <p className="text-sm text-muted-foreground mt-2 max-w-md mx-auto">
                                Your elite penetration testing mentor. Ask me about reconnaissance, exploitation, report writing, or any security topic.
                            </p>
                            <div className="mt-6 grid grid-cols-2 gap-2 max-w-lg mx-auto">
                                {quickPrompts.map((prompt, i) => (
                                    <button key={i} onClick={() => setMessage(prompt)} className="p-3 text-left text-xs bg-black/40 border border-primary/20 rounded hover:border-primary/40 transition-colors">
                                        {prompt}
                                    </button>
                                ))}
                            </div>
                        </div>
                    )}

                    {messages.map((msg, i) => (
                        <div key={i} className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                            {msg.role === 'assistant' && (
                                <div className="w-8 h-8 bg-primary/20 rounded-full flex items-center justify-center flex-shrink-0 border border-primary/50">
                                    <Bot className="text-primary" size={16} />
                                </div>
                            )}
                            <div className={`max-w-[80%] p-3 rounded-lg ${msg.role === 'user' ? 'bg-primary/20 border border-primary/50' : 'bg-black/40 border border-primary/20'}`}>
                                {msg.role === 'assistant' ? (
                                    <div className="prose prose-invert prose-sm max-w-none"><ReactMarkdown>{msg.content}</ReactMarkdown></div>
                                ) : (
                                    <p className="text-sm">{msg.content}</p>
                                )}
                            </div>
                            {msg.role === 'user' && (
                                <div className="w-8 h-8 bg-muted rounded-full flex items-center justify-center flex-shrink-0">
                                    <User className="text-muted-foreground" size={16} />
                                </div>
                            )}
                        </div>
                    ))}

                    {sendMutation.isPending && (
                        <div className="flex gap-3">
                            <div className="w-8 h-8 bg-primary/20 rounded-full flex items-center justify-center flex-shrink-0 border border-primary/50">
                                <Bot className="text-primary" size={16} />
                            </div>
                            <div className="bg-black/40 border border-primary/20 p-3 rounded-lg">
                                <div className="flex gap-1">
                                    <span className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                                    <span className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                                    <span className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                                </div>
                            </div>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>

                <form onSubmit={handleSubmit} className="flex items-center gap-2 p-4 border-t border-primary/20 bg-black/40">
                    <input
                        type="text"
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                        disabled={sendMutation.isPending}
                        placeholder="Ask the AI mentor..."
                        className="flex-1 bg-transparent border border-primary/30 rounded px-4 py-2.5 text-sm outline-none focus:border-primary/60 transition-colors"
                    />
                    <button type="submit" disabled={sendMutation.isPending || !message.trim()} className="btn-primary px-4 py-2.5">
                        <Send size={16} />
                    </button>
                </form>
            </Card>
        </div>
    );
}

export default function AIPage() {
    return (
        <Suspense fallback={<div className="text-primary/50">Loading AI assistant...</div>}>
            <AIContent />
        </Suspense>
    );
}
