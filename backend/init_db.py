"""Initialize database — create all tables and seed sample data."""
from app.db.session import engine, Base, SessionLocal
from app.models.customer import Customer
from app.models.bidding import Bidding
from app.models.project import Project
from app.models.organization import Organization
from datetime import date

def init():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created.")

    db = SessionLocal()
    try:
        # Seed: Organizations
        if db.query(Organization).count() == 0:
            db.add_all([
                Organization(id=1, name='华东区', parent_id=None, level=1, sort_order=1),
                Organization(id=2, name='上海', parent_id=1, level=2, sort_order=1),
                Organization(id=3, name='杭州', parent_id=1, level=2, sort_order=2),
                Organization(id=4, name='华南区', parent_id=None, level=1, sort_order=2),
                Organization(id=5, name='深圳', parent_id=4, level=2, sort_order=1),
                Organization(id=6, name='广州', parent_id=4, level=2, sort_order=2),
            ])

        # Seed: Customers
        if db.query(Customer).count() == 0:
            db.add_all([
                Customer(name='中科曙光', company='中科曙光信息产业股份有限公司', phone='13800001111', email='contact@sugon.com', industry='IT/互联网', level='A'),
                Customer(name='上海张江集团', company='上海张江高科技园区开发股份有限公司', phone='13800002222', email='contact@zhangjiang.com', industry='政府/国企', level='B'),
                Customer(name='浙江大数据局', company='浙江省大数据发展管理局', phone='13800003333', industry='政府/国企', level='A'),
                Customer(name='深圳华为', company='华为技术有限公司', phone='13800004444', industry='IT/互联网', level='B'),
            ])

        # Seed: Bidding
        if db.query(Bidding).count() == 0:
            db.add_all([
                Bidding(project_name='智慧园区管理平台', customer_name='上海张江集团', amount=12600000, bid_deadline=date(2026,7,15), status='方案设计', probability=60),
                Bidding(project_name='大数据分析平台二期', customer_name='浙江大数据局', amount=8600000, bid_deadline=date(2026,8,1), status='商务谈判', probability=80),
                Bidding(project_name='云计算基础设施扩容', customer_name='深圳华为', amount=3200000, bid_deadline=date(2026,6,30), status='投标中', probability=50),
            ])

        # Seed: Projects
        if db.query(Project).count() == 0:
            db.add_all([
                Project(project_name='中科曙光IT运维平台', customer_name='中科曙光', pm_name='王工', stage='商务谈判', progress=65, start_date=date(2025,11,1), expected_end_date=date(2026,9,30), amount=5800000),
                Project(project_name='张江智慧园区一期', customer_name='上海张江集团', pm_name='李经理', stage='方案演示', progress=30, start_date=date(2026,3,1), expected_end_date=date(2027,3,1), amount=12600000),
            ])

        db.commit()
        print("Seed data inserted.")
    finally:
        db.close()

if __name__ == '__main__':
    init()
