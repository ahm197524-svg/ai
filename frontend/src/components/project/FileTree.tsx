'use client';

import { useState } from 'react';
import { ChevronRight, ChevronDown, File, Folder, FolderOpen } from 'lucide-react';
import { cn } from '@/lib/utils';

export type FileNode = {
  name: string;
  type: 'file' | 'directory';
  children?: FileNode[];
  path?: string;
};

interface FileTreeProps {
  files: FileNode;
  activeFile: string | null;
  onFileSelect: (path: string) => void;
}

export function FileTree({ files, activeFile, onFileSelect }: FileTreeProps) {
  return (
    <div className="py-2">
      <TreeNode
        node={files}
        path=""
        activeFile={activeFile}
        onFileSelect={onFileSelect}
        level={0}
      />
    </div>
  );
}

function TreeNode({
  node,
  path,
  activeFile,
  onFileSelect,
  level,
}: {
  node: FileNode;
  path: string;
  activeFile: string | null;
  onFileSelect: (path: string) => void;
  level: number;
}) {
  const [isExpanded, setIsExpanded] = useState(level < 2);
  const fullPath = path ? `${path}/${node.name}` : node.name;
  const isActive = activeFile === fullPath;

  if (node.type === 'file') {
    return (
      <button
        onClick={() => onFileSelect(fullPath)}
        className={cn(
          'w-full flex items-center gap-2 px-2 py-1 text-sm hover:bg-accent rounded-sm transition-colors',
          isActive && 'bg-accent text-accent-foreground font-medium'
        )}
        style={{ paddingLeft: `${level * 12 + 8}px` }}
      >
        <File className="w-4 h-4 text-muted-foreground flex-shrink-0" />
        <span className="truncate">{node.name}</span>
      </button>
    );
  }

  return (
    <div>
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full flex items-center gap-2 px-2 py-1 text-sm hover:bg-accent rounded-sm transition-colors"
        style={{ paddingLeft: `${level * 12 + 8}px` }}
      >
        {isExpanded ? (
          <ChevronDown className="w-4 h-4 flex-shrink-0" />
        ) : (
          <ChevronRight className="w-4 h-4 flex-shrink-0" />
        )}
        {isExpanded ? (
          <FolderOpen className="w-4 h-4 text-muted-foreground flex-shrink-0" />
        ) : (
          <Folder className="w-4 h-4 text-muted-foreground flex-shrink-0" />
        )}
        <span className="truncate font-medium">{node.name}</span>
      </button>

      {isExpanded && node.children && (
        <div>
          {node.children.map((child, index) => (
            <TreeNode
              key={`${child.name}-${index}`}
              node={child}
              path={fullPath}
              activeFile={activeFile}
              onFileSelect={onFileSelect}
              level={level + 1}
            />
          ))}
        </div>
      )}
    </div>
  );
}
