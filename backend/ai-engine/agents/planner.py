"""
Planner Agent - Decomposes user prompts into structured requirements.

This agent:
1. Analyzes the user's natural language prompt
2. Extracts key requirements (pages, features, integrations)
3. Determines complexity and scope
4. Creates a structured plan for the Architect agent
"""

from typing import Dict, Any, List
from openai import AsyncOpenAI
from config import settings
import json


class PlannerAgent:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.PLANNER_MODEL

    async def create_plan(self, prompt: str) -> Dict[str, Any]:
        """
        Analyze user prompt and create structured plan.

        Args:
            prompt: User's natural language description

        Returns:
            Structured plan with requirements, features, pages, etc.
        """
        system_prompt = """You are an expert software architect and product manager.
Your job is to analyze user requests for web applications and break them down into
structured, actionable plans.

Given a user prompt, extract:
1. **requirements**: List of specific features/capabilities needed
2. **pages**: List of pages/routes required with descriptions
3. **features**: High-level feature categories (auth, payments, etc.)
4. **integrations**: Third-party services needed (Stripe, Auth0, etc.)
5. **database_entities**: Main data models/entities
6. **complexity**: 'simple', 'medium', or 'complex'
7. **estimated_files**: Approximate number of files needed

Return ONLY valid JSON. Be specific and thorough."""

        user_message = f"""Analyze this application request and create a detailed plan:

"{prompt}"

Return a JSON object with the structure described in the system prompt."""

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            response_format={"type": "json_object"},
            temperature=0.3
        )

        plan_json = response.choices[0].message.content
        plan = json.loads(plan_json)

        return plan


    async def refine_plan(self, plan: Dict[str, Any], feedback: str) -> Dict[str, Any]:
        """
        Refine an existing plan based on user feedback.

        Args:
            plan: Current plan
            feedback: User feedback/modifications

        Returns:
            Updated plan
        """
        system_prompt = """You are refining an application plan based on user feedback.
Update the plan while maintaining the same JSON structure."""

        user_message = f"""Current plan:
{json.dumps(plan, indent=2)}

User feedback:
"{feedback}"

Update the plan based on the feedback. Return the complete updated plan as JSON."""

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            response_format={"type": "json_object"},
            temperature=0.3
        )

        updated_plan = json.loads(response.choices[0].message.content)
        return updated_plan


# Example plan output:
"""
{
  "requirements": [
    "Landing page with hero section, features, and pricing",
    "Email/password authentication system",
    "User dashboard showing subscription status",
    "Stripe payment integration for Pro plan ($29/month)",
    "Account settings page"
  ],
  "pages": [
    {
      "path": "/",
      "name": "Landing Page",
      "description": "Marketing page with hero, features, pricing sections"
    },
    {
      "path": "/login",
      "name": "Login",
      "description": "User login with email/password"
    },
    {
      "path": "/signup",
      "name": "Signup",
      "description": "User registration"
    },
    {
      "path": "/app",
      "name": "Dashboard",
      "protected": true,
      "description": "User dashboard showing subscription info"
    },
    {
      "path": "/app/settings",
      "name": "Settings",
      "protected": true,
      "description": "Account settings and billing portal"
    }
  ],
  "features": [
    "authentication",
    "payments",
    "user-dashboard"
  ],
  "integrations": [
    {
      "service": "stripe",
      "purpose": "Payment processing and subscriptions"
    },
    {
      "service": "next-auth",
      "purpose": "Authentication"
    }
  ],
  "database_entities": [
    {
      "name": "User",
      "fields": ["id", "email", "password", "name", "createdAt"]
    },
    {
      "name": "Subscription",
      "fields": ["id", "userId", "stripeCustomerId", "status", "currentPeriodEnd"]
    }
  ],
  "complexity": "medium",
  "estimated_files": 38
}
"""
