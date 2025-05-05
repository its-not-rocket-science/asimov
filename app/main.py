"""
Main Entrypoint
---------------
Launches the FastAPI application and optionally runs a simulated agent test 
suite if executed as a script.
"""
from fastapi import FastAPI
from app.api.routes import moderate_route
from app.agent import SimulatedAIAgent
from app.core.system import AbstractAISystem
from app.core.reflector import EthicalReflector

app = FastAPI()
app.state.ai = AbstractAISystem()
"""
FastAPI application instance that exposes moderation routes.
"""
app.include_router(moderate_route)

if __name__ == "__main__":  # pragma: no cover
    ai = AbstractAISystem(reflector=EthicalReflector())

    print("Running Simulated Tests...")
    sim = SimulatedAIAgent(ai)
    for result in sim.run_simulation():
        print(result)
