'use client';

import { useState } from 'react';
import { FileTree } from '@/components/project/FileTree';
import { CodeEditor } from '@/components/editor/CodeEditor';
import { ChatInterface } from '@/components/chat/ChatInterface';
import { LivePreview } from '@/components/preview/LivePreview';
import { Button } from '@/components/ui/button';
import {
  PanelLeftClose,
  PanelLeftOpen,
  Play,
  Download,
  Settings
} from 'lucide-react';

export default function ProjectPage({ params }: { params: { id: string } }) {
  const [showSidebar, setShowSidebar] = useState(true);
  const [showChat, setShowChat] = useState(true);
  const [activeFile, setActiveFile] = useState<string | null>('src/app/page.tsx');

  return (
    <div className="h-screen flex flex-col bg-background">
      {/* Header */}
      <header className="h-14 border-b flex items-center justify-between px-4">
        <div className="flex items-center gap-4">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setShowSidebar(!showSidebar)}
          >
            {showSidebar ? (
              <PanelLeftClose className="w-4 h-4" />
            ) : (
              <PanelLeftOpen className="w-4 h-4" />
            )}
          </Button>
          <div>
            <h1 className="text-lg font-semibold">My SaaS App</h1>
            <p className="text-xs text-muted-foreground">Next.js • TypeScript • Tailwind</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" className="gap-2">
            <Download className="w-4 h-4" />
            Export
          </Button>
          <Button size="sm" className="gap-2">
            <Play className="w-4 h-4" />
            Deploy
          </Button>
          <Button variant="ghost" size="icon">
            <Settings className="w-4 h-4" />
          </Button>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden">
        {/* File Tree Sidebar */}
        {showSidebar && (
          <div className="w-64 border-r flex flex-col">
            <div className="p-4 border-b">
              <h2 className="text-sm font-semibold">Files</h2>
            </div>
            <div className="flex-1 overflow-auto">
              <FileTree
                files={mockFileTree}
                activeFile={activeFile}
                onFileSelect={setActiveFile}
              />
            </div>
          </div>
        )}

        {/* Code Editor */}
        <div className="flex-1 flex flex-col">
          <CodeEditor
            file={activeFile}
            projectId={params.id}
          />
        </div>

        {/* Right Panel - Chat or Preview */}
        <div className="w-96 border-l flex flex-col">
          <div className="border-b">
            <div className="flex">
              <button
                className={`flex-1 px-4 py-2 text-sm font-medium ${
                  showChat ? 'border-b-2 border-primary' : 'text-muted-foreground'
                }`}
                onClick={() => setShowChat(true)}
              >
                AI Assistant
              </button>
              <button
                className={`flex-1 px-4 py-2 text-sm font-medium ${
                  !showChat ? 'border-b-2 border-primary' : 'text-muted-foreground'
                }`}
                onClick={() => setShowChat(false)}
              >
                Preview
              </button>
            </div>
          </div>

          <div className="flex-1 overflow-hidden">
            {showChat ? (
              <ChatInterface projectId={params.id} />
            ) : (
              <LivePreview projectId={params.id} />
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

// Mock file tree data
const mockFileTree = {
  name: 'root',
  type: 'directory' as const,
  children: [
    {
      name: 'src',
      type: 'directory' as const,
      children: [
        {
          name: 'app',
          type: 'directory' as const,
          children: [
            { name: 'page.tsx', type: 'file' as const },
            { name: 'layout.tsx', type: 'file' as const },
            { name: 'globals.css', type: 'file' as const },
          ],
        },
        {
          name: 'components',
          type: 'directory' as const,
          children: [
            {
              name: 'ui',
              type: 'directory' as const,
              children: [
                { name: 'button.tsx', type: 'file' as const },
                { name: 'card.tsx', type: 'file' as const },
              ],
            },
          ],
        },
      ],
    },
    { name: 'package.json', type: 'file' as const },
    { name: 'tsconfig.json', type: 'file' as const },
    { name: 'tailwind.config.ts', type: 'file' as const },
  ],
};
