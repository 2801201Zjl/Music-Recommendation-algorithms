import os
import django
import torch
from datetime import datetime
import logging
import time

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_recommendation.settings')
django.setup()

# 导入必要的模块
from music.models import Song, UserPreference
from music.utils.llm_processor import LLMProcessor
from music.utils.audio_processor import extract_features
from music.utils.recommendation import get_recommendations
from django.contrib.auth.models import User

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('music_recommendation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MusicRecommendationSystem:
    def __init__(self):
        self.llm_processor = LLMProcessor()
        self.logger = logging.getLogger(__name__)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.logger.info(f"Using device: {self.device}")

    def initialize_system(self):
        """初始化系统"""
        try:
            self.logger.info("Initializing music recommendation system...")
            # 检查数据库连接
            self._check_database()
            # 检查模型和必要组件
            self._check_components()
            self.logger.info("System initialized successfully")
            return True
        except Exception as e:
            self.logger.error(f"Initialization failed: {str(e)}")
            return False

    def _check_database(self):
        """检查数据库连接和必要的表"""
        try:
            # 检查是否有用户
            user_count = User.objects.count()
            self.logger.info(f"Found {user_count} users in database")
            # 检查是否有歌曲
            song_count = Song.objects.count()
            self.logger.info(f"Found {song_count} songs in database")
        except Exception as e:
            self.logger.error(f"Database check failed: {str(e)}")
            raise

    def _check_components(self):
        """检查系统组件"""
        try:
            self.llm_processor.model.to(self.device)
            self.logger.info("LLM model loaded successfully")
        except Exception as e:
            self.logger.error(f"Failed to load LLM model: {str(e)}")
            raise

    def process_user_preferences(self, user_id):
        """处理用户偏好"""
        try:
            preferences = UserPreference.objects.filter(user_id=user_id)
            if not preferences.exists():
                self.logger.info(f"No preferences found for user {user_id}")
                return None

            comments = [pref.comment for pref in preferences if pref.comment]
            if comments:
                self.logger.info(f"Processing {len(comments)} comments for user {user_id}")
                text_features = self.llm_processor.process_text(comments)
            else:
                text_features = None

            songs = [pref.song for pref in preferences]
            if songs:
                audio_features = extract_features(songs)
            else:
                audio_features = None

            return text_features, audio_features

        except Exception as e:
            self.logger.error(f"Error processing user preferences: {str(e)}")
            return None

    def generate_recommendations(self, user_id):
        """生成推荐"""
        try:
            features = self.process_user_preferences(user_id)
            if not features:
                self.logger.info(f"No features available for user {user_id}")
                return []

            text_features, audio_features = features
            recommendations = get_recommendations(
                user_id,
                text_features,
                audio_features
            )

            self.logger.info(f"Generated {len(recommendations)} recommendations for user {user_id}")
            return recommendations

        except Exception as e:
            self.logger.error(f"Error generating recommendations: {str(e)}")
            return []

    def update_recommendations(self):
        """更新所有用户的推荐"""
        try:
            users = User.objects.filter(is_active=True)
            if not users.exists():
                self.logger.warning("No active users found in database")
                return

            for user in users:
                self.logger.info(f"Updating recommendations for user {user.id}")
                recommendations = self.generate_recommendations(user.id)
                if recommendations:
                    # 这里可以添加推荐结果的存储逻辑
                    self.logger.info(f"Successfully updated recommendations for user {user.id}")

            self.logger.info("Recommendations update completed")

        except Exception as e:
            self.logger.error(f"Error updating recommendations: {str(e)}")

    def run_continuously(self, interval=3600):
        """持续运行推荐系统"""
        self.logger.info(f"Starting continuous recommendation updates every {interval} seconds")
        while True:
            try:
                self.update_recommendations()
                self.logger.info(f"Waiting {interval} seconds until next update...")
                time.sleep(interval)
            except KeyboardInterrupt:
                self.logger.info("Shutting down recommendation system...")
                break
            except Exception as e:
                self.logger.error(f"Error in continuous run: {str(e)}")
                time.sleep(60)  # 出错后等待1分钟再重试

def main():
    """主函数"""
    try:
        system = MusicRecommendationSystem()
        
        if not system.initialize_system():
            logger.error("System initialization failed")
            return

        system.run_continuously(interval=3600)  # 每小时更新一次
        
    except Exception as e:
        logger.error(f"Main process failed: {str(e)}")
    finally:
        logger.info("Main process completed")

if __name__ == "__main__":
    main() 