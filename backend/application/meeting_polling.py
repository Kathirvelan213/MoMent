import asyncio
from application.moments_orchestrator import MomentsOrchestrator
from shared_state import meeting_states

async def poll_meetings(orchestrator: MomentsOrchestrator, interval: float = 5.0) -> None:
    while True:
        for meeting_id in list(meeting_states.keys()):
            orchestrator.process_meeting_workflow(meeting_id)
        await asyncio.sleep(interval)
