import csv
import os
import json
from datetime import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.content.models import FAQ


class Command(BaseCommand):
    help = 'Seed FAQ data from CSV file with Chinese translations'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing FAQ data before seeding',
        )

    def handle(self, *args, **options):
        # Define hardcoded translations since they are not in the CSV
        # Map faq_id (e.g. "faq_id_1") or question text to Chinese Q&A
        translations = {
            "faq_id_1": {
                "question_zh_tw": "如何申請志工專案？",
                "answer_zh_tw": "若要申請志工專案，請瀏覽我們的專案頁面，選擇您感興趣的專案，然後點擊「申請」按鈕。您需要登入帳戶才能提交申請。"
            },
            "faq_id_2": {
                "question_zh_tw": "成為志工有什麼要求？",
                "answer_zh_tw": "要求因專案而異，但通常您需要年滿 18 歲（或 16 歲並獲得父母同意），熱衷於社區服務，並能承諾專案期間。特定專案可能有額外要求。"
            },
            "faq_id_3": {
                "question_zh_tw": "志工活動有費用嗎？",
                "answer_zh_tw": "我們的大多數志工專案都是免費參加的。然而，志工通常需要自行負擔交通、住宿和個人費用。有些專案可能會收取少量的行政費用。"
            },
            "faq_id_4": {
                "question_zh_tw": "我可以參加國際志工嗎？",
                "answer_zh_tw": "是的！我們提供台灣和國際的志工機會。請查看我們專案頁面上的國家篩選器，找到您感興趣的機會。"
            },
            "faq_id_5": {
                "question_zh_tw": "志工專案通常持續多久？",
                "answer_zh_tw": "專案持續時間從幾天到幾週或幾個月不等。每個專案列表都會顯示預計的時間投入和持續時間。您可以在我們的搜尋頁面上按持續時間篩選專案。"
            },
            "faq_id_6": {
                "question_zh_tw": "完成專案後我會收到證書嗎？",
                "answer_zh_tw": "是的！順利完成志工專案後，您將收到一份記錄您的志工時數和貢獻的證書。這對學校要求或求職申請很有用。"
            },
            "faq_id_7": {
                "question_zh_tw": "如果我需要取消申請怎麼辦？",
                "answer_zh_tw": "如果您需要取消申請，請盡快透過聯絡表單或電子郵件與我們聯繫。我們了解情況可能會發生變化，我們將與您一起尋找解決方案。"
            },
            "faq_id_8": {
                "question_zh_tw": "志工需要特殊技能嗎？",
                "answer_zh_tw": "不一定！我們的許多專案都歡迎沒有特殊技能的志工——只需要熱情和樂於助人的心。然而，有些專業專案可能需要特定的技能或資格，這將在專案描述中清楚說明。"
            }
        }

        data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
        csv_path = os.path.join(data_dir, '4_FAQ.csv')

        if options['clear']:
            self.stdout.write('Clearing existing FAQ data...')
            FAQ.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing FAQ data cleared.'))

        self.stdout.write('Starting FAQ data seeding...')

        if not os.path.exists(csv_path):
            self.stdout.write(self.style.WARNING(f'CSV file not found: {csv_path}'))
            return

        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Parse dates
                created_at = self.parse_datetime(row.get('created_at'))
                updated_at = self.parse_datetime(row.get('updated_at'))

                # Parse boolean field
                is_schema_ready = row.get('is_schema_ready', '').lower() == 'true'

                # Parse integers
                order = int(row.get('order', 0)) if row.get('order') else 0
                thumbs_up = int(row.get('thumbs_up', 0)) if row.get('thumbs_up') else 0
                thumbs_down = int(row.get('thumbs_down', 0)) if row.get('thumbs_down') else 0

                faq_id = row.get('faq_id')
                question_en = row.get('question', '')
                answer_en = row.get('answer', '')
                
                # Check for translations in CSV first, then fallback to hardcoded map
                question_zh = row.get('question_zh_tw') or translations.get(faq_id, {}).get('question_zh_tw', '')
                answer_zh = row.get('answer_zh_tw') or translations.get(faq_id, {}).get('answer_zh_tw', '')

                # If still empty, maybe use English as fallback? 
                # Better to leave it empty if we really don't have it, but for this task we want Chinese.
                if not question_zh:
                    question_zh = question_en
                if not answer_zh:
                    answer_zh = answer_en

                defaults = {
                    'question': question_en,       # Default language (usually en)
                    'answer': answer_en,           # Default language (usually en)
                    'question_en': question_en,
                    'answer_en': answer_en,
                    'question_zh_tw': question_zh,
                    'answer_zh_tw': answer_zh,
                    'order': order,
                    'is_schema_ready': is_schema_ready,
                    'thumbs_up': thumbs_up,
                    'thumbs_down': thumbs_down,
                    'created_at': created_at or timezone.now(),
                    'updated_at': updated_at or timezone.now(),
                }

                faq, created = FAQ.objects.update_or_create(
                    faq_id=faq_id,
                    defaults=defaults
                )

                if created:
                    self.stdout.write(f'Created FAQ: {faq.question}')
                else:
                    self.stdout.write(f'Updated FAQ: {faq.question}')

        self.stdout.write(self.style.SUCCESS('FAQ seeding completed successfully!'))

    def parse_datetime(self, date_str):
        """Parse datetime string to datetime object"""
        if not date_str or date_str.lower() == 'null':
            return None
        try:
            # Handle ISO format with Z
            if date_str.endswith('Z'):
                date_str = date_str[:-1] + '+00:00'
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            # Make timezone-naive since USE_TZ=False or handled elsewhere
            if dt.tzinfo is not None:
                dt = dt.replace(tzinfo=None)
            return dt
        except ValueError:
            self.stdout.write(self.style.WARNING(f'Invalid datetime format: {date_str}'))
            return None
