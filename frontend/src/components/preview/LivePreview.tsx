'use client';

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { RefreshCw, ExternalLink, Loader2 } from 'lucide-react';

interface LivePreviewProps {
  projectId: string;
}

export function LivePreview({ projectId }: LivePreviewProps) {
  const [isLoading, setIsLoading] = useState(true);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  useEffect(() => {
    // TODO: Start sandbox and get preview URL
    // Simulate loading
    setTimeout(() => {
      setPreviewUrl(`http://localhost:4000/${projectId}`);
      setIsLoading(false);
    }, 2000);
  }, [projectId]);

  const handleRefresh = () => {
    setIsLoading(true);
    // Reload the iframe
    setTimeout(() => {
      setIsLoading(false);
    }, 500);
  };

  const handleOpenInNewTab = () => {
    if (previewUrl) {
      window.open(previewUrl, '_blank');
    }
  };

  return (
    <div className="h-full flex flex-col">
      {/* Preview Controls */}
      <div className="h-12 border-b flex items-center justify-between px-4 bg-muted/20">
        <div className="text-sm text-muted-foreground">
          {isLoading ? 'Starting preview...' : 'Preview'}
        </div>
        <div className="flex items-center gap-2">
          <Button
            variant="ghost"
            size="sm"
            onClick={handleRefresh}
            disabled={isLoading}
          >
            <RefreshCw className="w-4 h-4" />
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={handleOpenInNewTab}
            disabled={!previewUrl}
          >
            <ExternalLink className="w-4 h-4" />
          </Button>
        </div>
      </div>

      {/* Preview Frame */}
      <div className="flex-1 relative bg-white">
        {isLoading ? (
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="text-center space-y-4">
              <Loader2 className="w-8 h-8 animate-spin text-muted-foreground mx-auto" />
              <p className="text-sm text-muted-foreground">
                Starting development server...
              </p>
            </div>
          </div>
        ) : previewUrl ? (
          <iframe
            src={previewUrl}
            className="w-full h-full border-0"
            title="Preview"
            sandbox="allow-scripts allow-same-origin allow-forms"
          />
        ) : (
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="text-center space-y-2">
              <p className="text-sm text-muted-foreground">
                No preview available
              </p>
              <Button variant="outline" size="sm">
                Start Preview
              </Button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
