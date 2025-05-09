from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    google,
    cartesia,
    deepgram,
    noise_cancellation,
    silero,
)
from livekit.plugins.turn_detector.multilingual import MultilingualModel
from livekit.agents.llm import function_tool
from enum import Enum
import logging
logger = logging.getLogger("annotated-tool-args")
logger.setLevel(logging.INFO)
from typing import Annotated, Literal
load_dotenv()
import aiohttp

class Agent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=("You are a helpful voice AI assistant."),
        )

    @function_tool
    async def get_weather(self, location: str) -> str:
        """
        Called when the user asks about the weather.

        Args:
            location: The location to get the weather for
        """
        logger.info(f"Getting weather for {location}")
        return f"The weather in {location} is sunny today."

    @function_tool
    async def toggle_light(self, switch_to: Literal["on", "off"]) -> str:
        """
        Called when the user asks to turn on or off the light.
        Makes direct API call to ESP32 web server and remembers the state.
        
        Args:
            switch_to: The state to turn the light to ("on" or "off")
            
        Returns:
            str: Confirmation message of the action taken
        """
        esp32_ip = "192.168.0.101" 
        url = f"http://{esp32_ip}/led"
        headers = {"Content-Type": "application/json"}
        payload = {"status": switch_to}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, headers=headers) as response:
                    if response.status == 200:
                        self.light_status = switch_to
                        response_data = await response.json()
                        return f"Light turned {switch_to}. {response_data.get('message', '')}"
                    else:
                        error_text = await response.text()
                        return f"Failed to toggle light. Error: {error_text}"
        
        except Exception as e:
            logger.error(f"Error toggling light: {str(e)}")
            return "Sorry, I couldn't control the light. Please try again later."

async def entrypoint(ctx: agents.JobContext):
    await ctx.connect()

    session = AgentSession(
        stt=deepgram.STT(model="nova-3", language="multi"),
        llm=google.LLM(model="gemini-2.0-flash-001"),
        tts=cartesia.TTS(),
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    await session.start(
        room=ctx.room,
        agent=Agent(),
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(), 
        ),
    )

    await session.generate_reply(
        instructions="Greet the user and offer your assistance."
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))