import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.database import Base, SessionModel, MessageModel
from app.services.database_service import DatabaseService
import uuid

class TestDatabaseService(unittest.TestCase):
    def setUp(self):
        # 创建内存数据库用于测试
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)
        self.db = self.SessionLocal()
        self.database_service = DatabaseService()

    def tearDown(self):
        self.db.close()

    def test_create_session(self):
        # 测试创建会话
        session = self.database_service.create_session(self.db, "测试会话")
        self.assertIsNotNone(session.id)
        self.assertEqual(session.title, "测试会话")
        self.assertTrue(session.is_active)

    def test_get_session(self):
        # 测试获取会话
        created_session = self.database_service.create_session(self.db, "测试会话")
        retrieved_session = self.database_service.get_session(self.db, created_session.id)
        self.assertEqual(created_session.id, retrieved_session.id)
        self.assertEqual(created_session.title, retrieved_session.title)

    def test_update_session(self):
        # 测试更新会话
        session = self.database_service.create_session(self.db, "原始标题")
        updated_session = self.database_service.update_session(self.db, session.id, "更新后的标题")
        self.assertEqual(updated_session.title, "更新后的标题")

    def test_delete_session(self):
        # 测试删除会话
        session = self.database_service.create_session(self.db, "待删除会话")
        result = self.database_service.delete_session(self.db, session.id)
        self.assertTrue(result)
        deleted_session = self.database_service.get_session(self.db, session.id)
        self.assertIsNone(deleted_session)

    def test_add_message(self):
        # 测试添加消息
        session = self.database_service.create_session(self.db, "测试会话")
        message = self.database_service.add_message(
            self.db, 
            session.id, 
            "user", 
            "你好，这是一个测试消息", 
            10
        )
        self.assertIsNotNone(message.id)
        self.assertEqual(message.session_id, session.id)
        self.assertEqual(message.role, "user")
        self.assertEqual(message.content, "你好，这是一个测试消息")
        self.assertEqual(message.tokens, 10)

    def test_get_messages(self):
        # 测试获取消息
        session = self.database_service.create_session(self.db, "测试会话")
        self.database_service.add_message(self.db, session.id, "user", "用户消息", 5)
        self.database_service.add_message(self.db, session.id, "assistant", "AI回复", 3)
        
        messages = self.database_service.get_messages(self.db, session.id)
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0].role, "user")
        self.assertEqual(messages[1].role, "assistant")

if __name__ == '__main__':
    unittest.main()