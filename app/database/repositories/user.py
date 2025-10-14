from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from typing import Optional, List

from app.database import AsyncSessionLocal, User
from app.core import logger


class UserRepository:
    def __init__(self):
        pass
    
    
    async def _get_user_by_id(
        self,
        session,
        user_id: int
    ) -> Optional[User]:
        result = await session.execute(
            select(User).where(User.user_id == user_id)
        )
        
        return result.scalar_one_or_none()
    
    
    async def create_user(
        self,
        session: AsyncSession,
        user_id: int,
        username: str
    ) -> Optional[User]:
        try:
            exists_user = await self._get_user_by_id(session, user_id)
            
            if exists_user:
                logger.info(f"⚠️User {username}({user_id}) already exists")
                return exists_user
                
            new_user = User(
            user_id=user_id,
            username=username,
            interests=None,
            notification_time=None,
            )
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            
            logger.info(f"✅User {username}({user_id}) created successfully")
            return new_user
            
        except SQLAlchemyError as sqlerr:
            logger.error(f"❌ DB error while creating user: {sqlerr}")
            await session.rollback()
            return None
        
        except Exception as e:
            logger.error(f"❌Unexpected error while creating user: {e}")
            await session.rollback()
            return None


    async def save_user_interests(
        self,
        session: AsyncSession,
        user_id: int,
        username: str,
        user_interests: List[str],
    ) -> Optional[User]:
        try:
            result = await session.execute(
                select(User).where(
                    User.user_id == user_id,
                    User.interests.isnot(None)
                )
            )
            existing_user = result.scalar_one_or_none()

            if existing_user:
                logger.info(f"⚠️ User {user_id} already has interests, skipping...")
                return existing_user

            result = await session.execute(
                select(User).where(User.user_id == user_id)
            )
            user = result.scalar_one_or_none()

            if user:
                user.interests = user_interests
                await session.commit()
                await session.refresh(user)
                logger.info(f"✅ Interests updated for user {username}({user_id})")
                return user
            
            await self.create_user(
                session,
                user_id,
                username
            )

        except SQLAlchemyError as sqlerr:
            logger.error(f"❌ DB error while saving interests: {sqlerr}")
            await session.rollback()
            return None
        except Exception as e:
            logger.error(f"❌ Unexpected error while saving interests: {e}")
            await session.rollback()
            return None


user_repo = UserRepository()