#!/usr/bin/env python3
"""AWS Lambda handler for SignalWire agent.

Lab 2.11 Deliverable: Demonstrates serverless deployment patterns
for AWS Lambda with proper initialization and warm start handling.
"""

import os
from signalwire_agents import AgentBase, SwaigFunctionResult


class LambdaAgent(AgentBase):
    """Agent optimized for serverless deployment."""

    def __init__(self):
        super().__init__(name="lambda-agent")

        self.prompt_add_section(
            "Role",
            "You are a serverless assistant running on AWS Lambda."
        )

        self.prompt_add_section(
            "Capabilities",
            bullets=[
                "Answer questions about the service",
                "Provide status information",
                "Help with basic inquiries"
            ]
        )

        self.add_language("English", "en-US", "rime.spore")
        self._setup_functions()

    def _setup_functions(self):
        @self.tool(description="Get service status")
        def get_status() -> SwaigFunctionResult:
            return SwaigFunctionResult(
                "The service is running on AWS Lambda. All systems operational."
            )

        @self.tool(description="Get deployment info")
        def get_deployment_info() -> SwaigFunctionResult:
            region = os.getenv("AWS_REGION", "unknown")
            function = os.getenv("AWS_LAMBDA_FUNCTION_NAME", "unknown")
            memory = os.getenv("AWS_LAMBDA_FUNCTION_MEMORY_SIZE", "unknown")
            return SwaigFunctionResult(
                f"Running in {region} as {function} with {memory}MB memory."
            )

        @self.tool(
            description="Echo a message back",
            parameters={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Message to echo"
                    }
                },
                "required": ["message"]
            }
        )
        def echo(message: str) -> SwaigFunctionResult:
            return SwaigFunctionResult(f"You said: {message}")

        @self.tool(description="Get help information")
        def get_help() -> SwaigFunctionResult:
            return SwaigFunctionResult(
                "I can provide status info, deployment details, or echo messages. "
                "How can I help you today?"
            )


# Create agent instance outside handler for warm starts
# This allows the agent to be reused across invocations
agent = LambdaAgent()


def lambda_handler(event, context):
    """AWS Lambda entry point.

    Args:
        event: Lambda event (API Gateway request)
        context: Lambda context with runtime info

    Returns:
        API Gateway response dict
    """
    return agent.handle_lambda(event, context)
