#!/usr/bin/env python3
"""
test_antigravity_native_identity.py — Queries gemini-3.7-flash identity
using the official google.antigravity SDK.
"""

import sys
import os
import google.antigravity as agy

print("==========================================================================")
print("  TESTING NATIVE GOOGLE.ANTIGRAVITY SDK WITH MODEL 'gemini-3.7-flash'      ")
print("==========================================================================")

try:
    # Initialize Antigravity Agent with ModelTarget 'gemini-3.7-flash'
    agent = agy.Agent(
        config=agy.AgentConfig(
            model_target=agy.ModelTarget(
                model="gemini-3.7-flash"
            ),
            system_instructions=agy.SystemInstructions(
                custom_instructions=agy.CustomSystemInstructions(
                    text="You are an Antigravity Native Agent."
                )
            )
        )
    )
    
    prompt = "State your exact model name, version, and environment. Are you running under the Antigravity Agent Harness?"
    print(f"\nSubmitting Prompt: '{prompt}'\n")
    
    # Run conversation step via Antigravity Native Harness
    response = agent.run(prompt)
    
    print("--- NATIVE ANTIGRAVITY AGENT RESPONSE ---")
    print(response.text if hasattr(response, 'text') else str(response))
    print("-----------------------------------------")
    
    if hasattr(response, 'usage_metadata'):
        print(f"Usage Metadata: {response.usage_metadata}")
        
except Exception as e:
    print(f"Antigravity SDK Run Note: {e}")
    # Fallback to direct Antigravity GenAI wrapper if needed
    from google.antigravity.models import gemini
    print("\nExecuting via google.antigravity.models.gemini...")
    res = gemini.generate_content(
        model="gemini-3.7-flash",
        contents="State your exact model name and version."
    )
    print("--- ANTIGRAVITY MODEL RESPONSE ---")
    print(res.text)
    print("----------------------------------")
