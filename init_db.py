from pathlib import Path
import sqlite3

# هذا يحدد مجلد الملف الحالي (مجلد المشروع)
base_dir = Path(__file__).parent
# هذا ينشئ مسار مجلد فرعي باسم "database" لتخزين قاعدة البيانات
db_dir = base_dir / "database"
# هذا المسار الكامل لملف قاعدة البيانات نفسه
db_path = db_dir / "opinion_ai.db"
# هذا المسار لملف SQL الذي يحتوي على كل أوامر إنشاء الجداول
schema_path = base_dir / "schema.sql"

# ينشئ مجلد "database" إذا لم يكن موجود، وإلا يتجاهل الخطأ
db_dir.mkdir(exist_ok=True)

# يفتح قاعدة البيانات، إذا لم تكن موجودة ينشئها تلقائيًا
conn = sqlite3.connect(db_path)

# يفتح ملف schema.sql للقراءة ويخزن كل محتواه في متغير schema_sql
with open(schema_path, "r", encoding="utf-8") as f:
    schema_sql = f.read()

# ينفذ كل أوامر SQL الموجودة في الملف دفعة واحدة (إنشاء الجداول)
conn.executescript(schema_sql)

# يغلق الاتصال بقاعدة البيانات بعد الانتهاء
conn.close()

# يطبع رسالة نجاح مع مكان ملف قاعدة البيانات
print(f"Database created successfully at: {db_path}")