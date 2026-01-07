"""
Architect Agent - Designs the system architecture.

This agent:
1. Takes the plan from the Planner agent
2. Designs file/folder structure
3. Creates database schema
4. Defines API routes
5. Selects appropriate dependencies
"""

from typing import Dict, Any, List
from anthropic import AsyncAnthropic
from config import settings
import json


class ArchitectAgent:
    def __init__(self):
        self.client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = "claude-sonnet-3-5-20241022"

    async def design_architecture(
        self,
        plan: Dict[str, Any],
        framework: str = "nextjs",
        language: str = "typescript",
        styling: str = "tailwind"
    ) -> Dict[str, Any]:
        """
        Design system architecture based on plan.

        Args:
            plan: Plan from PlannerAgent
            framework: Frontend framework
            language: Programming language
            styling: CSS framework

        Returns:
            Complete architecture specification
        """
        system_prompt = """You are an expert software architect specializing in modern web applications.

Your job is to design a complete system architecture including:
1. File structure (directories and files)
2. Database schema (with proper relationships)
3. API routes (endpoints needed)
4. Dependencies (npm packages with versions)
5. Environment variables needed
6. Configuration files

Design production-ready, scalable architectures following best practices.
Return ONLY valid JSON."""

        user_message = f"""Design a complete architecture for this application:

PLAN:
{json.dumps(plan, indent=2)}

TECH STACK:
- Framework: {framework}
- Language: {language}
- Styling: {styling}
- ORM: Prisma
- Auth: NextAuth.js

Return a JSON object with:
- fileStructure: Complete directory tree with files
- databaseSchema: Prisma schema models
- apiRoutes: List of API endpoints with methods
- dependencies: npm packages with versions
- envVars: Required environment variables
- scripts: npm scripts for package.json"""

        response = await self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_message}
            ],
            temperature=0.2
        )

        architecture_json = response.content[0].text

        # Extract JSON from markdown code blocks if present
        if "```json" in architecture_json:
            architecture_json = architecture_json.split("```json")[1].split("```")[0].strip()
        elif "```" in architecture_json:
            architecture_json = architecture_json.split("```")[1].split("```")[0].strip()

        architecture = json.loads(architecture_json)

        return architecture


    def generate_file_list(self, file_structure: Dict[str, Any]) -> List[str]:
        """
        Flatten file structure into a list of file paths.

        Args:
            file_structure: Nested file structure

        Returns:
            List of file paths
        """
        files = []

        def traverse(node: Dict[str, Any], path: str = ""):
            for name, value in node.items():
                current_path = f"{path}/{name}" if path else name

                if isinstance(value, dict):
                    # Directory
                    traverse(value, current_path)
                else:
                    # File
                    files.append(current_path)

        traverse(file_structure)
        return files


# Example architecture output:
"""
{
  "fileStructure": {
    "src": {
      "app": {
        "page.tsx": "Landing page",
        "layout.tsx": "Root layout",
        "globals.css": "Global styles",
        "login": {
          "page.tsx": "Login page"
        },
        "signup": {
          "page.tsx": "Signup page"
        },
        "app": {
          "layout.tsx": "Protected layout",
          "page.tsx": "Dashboard",
          "settings": {
            "page.tsx": "Settings page"
          }
        },
        "api": {
          "auth": {
            "[...nextauth]": {
              "route.ts": "NextAuth handler"
            }
          },
          "stripe": {
            "checkout": {
              "route.ts": "Create checkout session"
            },
            "webhook": {
              "route.ts": "Stripe webhook"
            }
          }
        }
      },
      "components": {
        "landing": {
          "Hero.tsx": "Hero section",
          "Features.tsx": "Features",
          "Pricing.tsx": "Pricing"
        },
        "ui": {
          "button.tsx": "Button component",
          "card.tsx": "Card component"
        }
      },
      "lib": {
        "auth.ts": "Auth config",
        "db.ts": "Prisma client",
        "stripe.ts": "Stripe client"
      }
    },
    "prisma": {
      "schema.prisma": "Database schema"
    },
    "package.json": "Package manifest",
    "tsconfig.json": "TypeScript config",
    "tailwind.config.ts": "Tailwind config"
  },
  "databaseSchema": {
    "User": {
      "id": "String @id @default(cuid())",
      "email": "String @unique",
      "password": "String",
      "name": "String?",
      "createdAt": "DateTime @default(now())"
    },
    "Subscription": {
      "id": "String @id @default(cuid())",
      "userId": "String @unique",
      "stripeCustomerId": "String @unique",
      "status": "String",
      "currentPeriodEnd": "DateTime?"
    }
  },
  "apiRoutes": [
    {
      "method": "POST",
      "path": "/api/auth/[...nextauth]",
      "description": "NextAuth authentication"
    },
    {
      "method": "POST",
      "path": "/api/stripe/checkout",
      "description": "Create Stripe checkout session"
    },
    {
      "method": "POST",
      "path": "/api/stripe/webhook",
      "description": "Handle Stripe webhooks"
    }
  ],
  "dependencies": {
    "next": "14.0.4",
    "react": "^18.2.0",
    "next-auth": "^4.24.5",
    "stripe": "^14.10.0",
    "@prisma/client": "^5.7.1",
    "tailwindcss": "^3.4.0"
  },
  "envVars": [
    "DATABASE_URL",
    "NEXTAUTH_SECRET",
    "NEXTAUTH_URL",
    "STRIPE_SECRET_KEY",
    "NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY"
  ]
}
"""
