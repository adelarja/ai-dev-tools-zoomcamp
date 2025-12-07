import asyncio
from app.database import AsyncSessionLocal, engine
from app.models import InterviewSession
from sqlalchemy import select

async def seed_data():
    async with AsyncSessionLocal() as session:
        # Check if data exists
        result = await session.execute(select(InterviewSession))
        if result.scalars().first():
            print("Database already contains data. Skipping seed.")
            return

        print("Seeding database...")
        
        sessions = [
            InterviewSession(
                language="python",
                code_content="# Python Interview\ndef solve():\n    pass"
            ),
            InterviewSession(
                language="javascript",
                code_content="// JavaScript Interview\nfunction solve() {\n}"
            ),
            InterviewSession(
                language="java",
                code_content="// Java Interview\npublic class Main {\n    public static void main(String[] args) {\n    }\n}"
            )
        ]
        
        session.add_all(sessions)
        await session.commit()
        print(f"Added {len(sessions)} sessions.")

async def main():
    # Ensure tables exist (though alembic should handle this)
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    
    await seed_data()
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(main())
