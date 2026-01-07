import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { ArrowRight, Code, Sparkles, Zap } from 'lucide-react';

export default function HomePage() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-blue-50 to-white dark:from-gray-900 dark:to-gray-800">
      {/* Hero Section */}
      <div className="container mx-auto px-4 py-20">
        <div className="flex flex-col items-center text-center space-y-8">
          <div className="inline-flex items-center px-4 py-2 bg-blue-100 dark:bg-blue-900 rounded-full text-sm font-medium text-blue-800 dark:text-blue-200">
            <Sparkles className="w-4 h-4 mr-2" />
            AI-Powered Development
          </div>

          <h1 className="text-5xl md:text-7xl font-bold tracking-tight max-w-4xl">
            Build Full-Stack Apps
            <span className="text-blue-600 dark:text-blue-400"> with AI</span>
          </h1>

          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl">
            Describe your app in plain English and watch AI generate
            production-ready code with Next.js, TypeScript, and best practices.
          </p>

          <div className="flex gap-4">
            <Link href="/projects">
              <Button size="lg" className="gap-2">
                Start Building <ArrowRight className="w-4 h-4" />
              </Button>
            </Link>
            <Link href="/examples">
              <Button size="lg" variant="outline">
                View Examples
              </Button>
            </Link>
          </div>
        </div>

        {/* Features Grid */}
        <div className="mt-32 grid md:grid-cols-3 gap-8">
          <FeatureCard
            icon={<Code className="w-6 h-6" />}
            title="Production-Ready Code"
            description="Generate clean, type-safe TypeScript code with proper error handling and best practices."
          />
          <FeatureCard
            icon={<Zap className="w-6 h-6" />}
            title="Instant Preview"
            description="See your app come to life in real-time with our live preview sandbox."
          />
          <FeatureCard
            icon={<Sparkles className="w-6 h-6" />}
            title="AI-Powered Iterations"
            description="Refine your app through conversation. Just describe what you want to change."
          />
        </div>

        {/* Example Prompts */}
        <div className="mt-32">
          <h2 className="text-3xl font-bold text-center mb-12">
            Try These Prompts
          </h2>
          <div className="grid md:grid-cols-2 gap-4 max-w-4xl mx-auto">
            <PromptCard prompt="Build a SaaS landing page with pricing and authentication" />
            <PromptCard prompt="Create a task management app with drag-and-drop" />
            <PromptCard prompt="Generate a blog with MDX support and search" />
            <PromptCard prompt="Build an e-commerce store with Stripe checkout" />
          </div>
        </div>
      </div>
    </main>
  );
}

function FeatureCard({
  icon,
  title,
  description,
}: {
  icon: React.ReactNode;
  title: string;
  description: string;
}) {
  return (
    <div className="p-6 bg-white dark:bg-gray-800 rounded-lg border shadow-sm">
      <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900 rounded-lg flex items-center justify-center text-blue-600 dark:text-blue-400 mb-4">
        {icon}
      </div>
      <h3 className="text-xl font-semibold mb-2">{title}</h3>
      <p className="text-gray-600 dark:text-gray-300">{description}</p>
    </div>
  );
}

function PromptCard({ prompt }: { prompt: string }) {
  return (
    <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg border hover:border-blue-500 transition-colors cursor-pointer">
      <p className="text-gray-700 dark:text-gray-300">&ldquo;{prompt}&rdquo;</p>
    </div>
  );
}
