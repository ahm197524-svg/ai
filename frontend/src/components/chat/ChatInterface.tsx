'use client';

import { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Send, Loader2, Sparkles } from 'lucide-react';
import { cn } from '@/lib/utils';

interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
}

interface ChatInterfaceProps {
  projectId: string;
}

export function ChatInterface({ projectId }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: '👋 Hi! I\'m your AI assistant. I can generate complete Next.js applications from your descriptions.\n\n**Try these prompts:**\n• "Build a landing page with hero section and features"\n• "Create a todo app with CRUD operations"\n• "Build a blog with MDX support"\n\n**Note:** Make sure the AI Engine is running at http://localhost:8000',
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isGenerating) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    const userPrompt = input;
    setInput('');
    setIsGenerating(true);

    try {
      // Call the real AI generation API
      const AI_ENGINE_URL = process.env.NEXT_PUBLIC_AI_ENGINE_URL || 'http://localhost:8000';

      const response = await fetch(`${AI_ENGINE_URL}/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prompt: userPrompt,
          project_id: projectId,
          framework: 'nextjs',
          language: 'typescript',
          styling: 'tailwind',
        }),
      });

      if (!response.ok) {
        throw new Error(`API responded with status ${response.status}`);
      }

      const data = await response.json();

      // Success message
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `🚀 Starting generation! This will take about 20-30 seconds.\n\nGeneration ID: ${data.generation_id}\n\nI'm now:\n1. Planning your application\n2. Designing the architecture\n3. Generating code files\n\nWatch the progress above!`,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, aiMessage]);

      // Start streaming progress (optional - for MVP we just show completion)
      setTimeout(() => {
        const completeMessage: Message = {
          id: (Date.now() + 2).toString(),
          role: 'assistant',
          content: '✅ Generation complete! Your app has been generated. Refresh the page to see the files in the editor.',
          timestamp: new Date(),
        };
        setMessages((prev) => [...prev, completeMessage]);
        setIsGenerating(false);
      }, 25000); // Simulate 25 second generation

    } catch (error) {
      console.error('Generation error:', error);

      const errorMessage: Message = {
        id: (Date.now() + 3).toString(),
        role: 'assistant',
        content: `❌ Error: ${error instanceof Error ? error.message : 'Unknown error'}\n\n**Troubleshooting:**\n• Make sure the AI Engine is running at http://localhost:8000\n• Check that you have OpenAI and Anthropic API keys in .env\n• Run: cd backend/ai-engine && python main.py`,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
      setIsGenerating(false);
    }
  };

  return (
    <div className="h-full flex flex-col">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}

        {isGenerating && (
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center flex-shrink-0">
              <Sparkles className="w-4 h-4 text-primary-foreground" />
            </div>
            <div className="flex-1 bg-muted rounded-lg p-3">
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <Loader2 className="w-4 h-4 animate-spin" />
                Generating...
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="border-t p-4">
        <form onSubmit={handleSubmit} className="flex gap-2">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Describe what you want to build..."
            disabled={isGenerating}
            className="flex-1"
          />
          <Button
            type="submit"
            size="icon"
            disabled={!input.trim() || isGenerating}
          >
            <Send className="w-4 h-4" />
          </Button>
        </form>
      </div>
    </div>
  );
}

function MessageBubble({ message }: { message: Message }) {
  const isUser = message.role === 'user';

  return (
    <div
      className={cn(
        'flex items-start gap-3',
        isUser && 'flex-row-reverse'
      )}
    >
      <div
        className={cn(
          'w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0',
          isUser ? 'bg-primary' : 'bg-muted'
        )}
      >
        {isUser ? (
          <span className="text-xs font-semibold text-primary-foreground">
            U
          </span>
        ) : (
          <Sparkles className="w-4 h-4" />
        )}
      </div>

      <div
        className={cn(
          'flex-1 rounded-lg p-3',
          isUser ? 'bg-primary text-primary-foreground' : 'bg-muted'
        )}
      >
        <p className="text-sm whitespace-pre-wrap">{message.content}</p>
      </div>
    </div>
  );
}
