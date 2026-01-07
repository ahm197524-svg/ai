"""
Code Generation Agent - Generates actual code files.

This agent:
1. Takes plan + architecture
2. Generates production-ready code for each file
3. Ensures consistency across files
4. Includes proper error handling, types, and best practices
"""

from typing import Dict, Any, List
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
from config import settings
import asyncio


class CodeGenAgent:
    def __init__(self):
        self.openai = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.anthropic = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

    async def generate_files(
        self,
        plan: Dict[str, Any],
        architecture: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """
        Generate all code files based on plan and architecture.

        Args:
            plan: Application plan
            architecture: System architecture

        Returns:
            List of {path, content} dictionaries
        """
        file_structure = architecture.get("fileStructure", {})
        file_list = self._flatten_structure(file_structure)

        # Generate files in parallel (batches of 5)
        batch_size = 5
        all_files = []

        for i in range(0, len(file_list), batch_size):
            batch = file_list[i:i + batch_size]
            tasks = [
                self.generate_file(path, plan, architecture)
                for path in batch
            ]
            batch_results = await asyncio.gather(*tasks)
            all_files.extend(batch_results)

        return all_files

    async def generate_file(
        self,
        file_path: str,
        plan: Dict[str, Any],
        architecture: Dict[str, Any]
    ) -> Dict[str, str]:
        """
        Generate a single file.

        Args:
            file_path: Path to the file
            plan: Application plan
            architecture: System architecture

        Returns:
            {path, content} dictionary
        """
        # Determine file type and select appropriate generator
        ext = file_path.split('.')[-1]

        if ext in ['tsx', 'ts', 'jsx', 'js']:
            content = await self._generate_typescript_file(file_path, plan, architecture)
        elif ext == 'prisma':
            content = await self._generate_prisma_schema(architecture)
        elif ext == 'json':
            content = await self._generate_json_file(file_path, architecture)
        elif ext in ['css', 'scss']:
            content = await self._generate_css_file(file_path, architecture)
        else:
            content = f"// {file_path}\n// Generated file\n"

        return {
            "path": file_path,
            "content": content
        }

    async def _generate_typescript_file(
        self,
        file_path: str,
        plan: Dict[str, Any],
        architecture: Dict[str, Any]
    ) -> str:
        """Generate TypeScript/React file."""

        # Build context-specific prompt
        context = self._build_file_context(file_path, plan, architecture)

        system_prompt = """You are an expert React/Next.js developer.
Generate clean, production-ready code following these rules:

1. Use TypeScript with proper types
2. Include error handling and loading states
3. Follow Next.js 14 App Router conventions
4. Use Tailwind CSS for styling
5. Add proper accessibility attributes
6. Include JSDoc comments for exported functions
7. Use async/await for API calls
8. Implement proper form validation with Zod
9. Use 'use client' directive when needed

Return ONLY the code, no explanations."""

        user_prompt = f"""Generate the file: {file_path}

CONTEXT:
{context}

ARCHITECTURE:
{self._format_architecture_context(architecture)}

Generate complete, production-ready code for this file."""

        response = await self.openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2
        )

        code = response.choices[0].message.content

        # Clean up code blocks if present
        if "```" in code:
            code = code.split("```")[1]
            if code.startswith("typescript") or code.startswith("tsx"):
                code = "\n".join(code.split("\n")[1:])

        return code.strip()

    async def _generate_prisma_schema(self, architecture: Dict[str, Any]) -> str:
        """Generate Prisma schema file."""

        db_schema = architecture.get("databaseSchema", {})

        schema = """generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

"""

        for model_name, fields in db_schema.items():
            schema += f"model {model_name} {{\n"
            for field_name, field_type in fields.items():
                schema += f"  {field_name}  {field_type}\n"
            schema += "}\n\n"

        return schema

    async def _generate_json_file(
        self,
        file_path: str,
        architecture: Dict[str, Any]
    ) -> str:
        """Generate JSON configuration files."""

        if 'package.json' in file_path:
            return self._generate_package_json(architecture)
        elif 'tsconfig.json' in file_path:
            return self._generate_tsconfig()
        else:
            return "{}\n"

    async def _generate_css_file(
        self,
        file_path: str,
        architecture: Dict[str, Any]
    ) -> str:
        """Generate CSS files."""

        if 'globals.css' in file_path or 'global' in file_path:
            return """@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
  }
}
"""
        return ""

    def _generate_package_json(self, architecture: Dict[str, Any]) -> str:
        """Generate package.json."""
        import json

        deps = architecture.get("dependencies", {})

        package = {
            "name": "generated-app",
            "version": "0.1.0",
            "private": True,
            "scripts": {
                "dev": "next dev",
                "build": "next build",
                "start": "next start",
                "lint": "next lint"
            },
            "dependencies": deps,
            "devDependencies": {
                "@types/node": "^20",
                "@types/react": "^18",
                "typescript": "^5",
                "autoprefixer": "^10",
                "postcss": "^8",
                "tailwindcss": "^3"
            }
        }

        return json.dumps(package, indent=2) + "\n"

    def _generate_tsconfig(self) -> str:
        """Generate tsconfig.json."""
        import json

        config = {
            "compilerOptions": {
                "target": "ES2017",
                "lib": ["dom", "dom.iterable", "esnext"],
                "allowJs": True,
                "skipLibCheck": True,
                "strict": True,
                "noEmit": True,
                "esModuleInterop": True,
                "module": "esnext",
                "moduleResolution": "bundler",
                "resolveJsonModule": True,
                "isolatedModules": True,
                "jsx": "preserve",
                "incremental": True,
                "plugins": [{"name": "next"}],
                "paths": {
                    "@/*": ["./src/*"]
                }
            },
            "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
            "exclude": ["node_modules"]
        }

        return json.dumps(config, indent=2) + "\n"

    def _flatten_structure(
        self,
        structure: Dict[str, Any],
        prefix: str = ""
    ) -> List[str]:
        """Flatten nested file structure into list of paths."""

        files = []

        for name, value in structure.items():
            path = f"{prefix}/{name}" if prefix else name

            if isinstance(value, dict):
                # Directory
                files.extend(self._flatten_structure(value, path))
            else:
                # File
                files.append(path)

        return files

    def _build_file_context(
        self,
        file_path: str,
        plan: Dict[str, Any],
        architecture: Dict[str, Any]
    ) -> str:
        """Build context string for file generation."""

        context = f"File: {file_path}\n\n"

        # Add relevant plan info
        if 'requirements' in plan:
            context += "Requirements:\n"
            for req in plan['requirements'][:5]:  # Top 5
                context += f"- {req}\n"
            context += "\n"

        # Add page info if it's a page
        if 'page.tsx' in file_path and 'pages' in plan:
            for page in plan['pages']:
                if page.get('path', '').replace('/', '') in file_path:
                    context += f"Page: {page.get('name')}\n"
                    context += f"Description: {page.get('description')}\n\n"

        return context

    def _format_architecture_context(self, architecture: Dict[str, Any]) -> str:
        """Format architecture for context."""
        import json

        # Only include relevant parts to save tokens
        relevant = {
            "apiRoutes": architecture.get("apiRoutes", [])[:3],
            "databaseSchema": architecture.get("databaseSchema", {}),
        }

        return json.dumps(relevant, indent=2)
