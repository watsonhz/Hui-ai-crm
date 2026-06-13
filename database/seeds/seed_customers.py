"""Insert seed customer data for development / testing.

Usage:
    python database/seeds/seed_customers.py
"""

import os
import sys
from datetime import date, datetime, timedelta
from random import choice, randint

# Add project root so we can import app modules if needed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "backend"))

from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://crm_user:crm_pass@localhost:3306/ai_crm",
)

engine = create_engine(DATABASE_URL)

CUSTOMERS = [
    {"name": "张伟", "company": "华为技术有限公司", "industry": "信息技术", "phone": "13800138001", "email": "zhangwei@huawei.com", "source": "展会", "level": "A", "status": "谈判"},
    {"name": "李娜", "company": "阿里巴巴集团", "industry": "电子商务", "phone": "13800138002", "email": "lina@alibaba.com", "source": "官网", "level": "A", "status": "意向"},
    {"name": "王强", "company": "比亚迪股份有限公司", "industry": "新能源", "phone": "13800138003", "email": "wangqiang@byd.com", "source": "推荐", "level": "B", "status": "潜在"},
    {"name": "赵敏", "company": "中国平安保险", "industry": "金融保险", "phone": "13800138004", "email": "zhaomin@pingan.com", "source": "电话", "level": "B", "status": "成交"},
    {"name": "刘洋", "company": "京东集团", "industry": "电子商务", "phone": "13800138005", "email": "liuyang@jd.com", "source": "展会", "level": "C", "status": "谈判"},
    {"name": "陈静", "company": "美的集团", "industry": "家电制造", "phone": "13800138006", "email": "chenjing@midea.com", "source": "官网", "level": "A", "status": "意向"},
    {"name": "孙磊", "company": "中兴通讯", "industry": "通信设备", "phone": "13800138007", "email": "sunlei@zte.com", "source": "推荐", "level": "B", "status": "潜在"},
    {"name": "周婷", "company": "格力电器", "industry": "家电制造", "phone": "13800138008", "email": "zhouting@gree.com", "source": "电话", "level": "C", "status": "流失"},
    {"name": "吴刚", "company": "小米科技", "industry": "消费电子", "phone": "13800138009", "email": "wugang@xiaomi.com", "source": "展会", "level": "A", "status": "谈判"},
    {"name": "郑丽", "company": "招商银行", "industry": "金融银行", "phone": "13800138010", "email": "zhengli@cmbchina.com", "source": "官网", "level": "B", "status": "意向"},
    {"name": "冯涛", "company": "腾讯科技", "industry": "互联网", "phone": "13800138011", "email": "fengtao@tencent.com", "source": "推荐", "level": "A", "status": "成交"},
    {"name": "蒋欢", "company": "网易集团", "industry": "互联网", "phone": "13800138012", "email": "jianghuan@netease.com", "source": "电话", "level": "C", "status": "潜在"},
    {"name": "韩雪", "company": "联想集团", "industry": "信息技术", "phone": "13800138013", "email": "hanxue@lenovo.com", "source": "展会", "level": "B", "status": "谈判"},
    {"name": "沈飞", "company": "海康威视", "industry": "安防监控", "phone": "13800138014", "email": "shenfei@hikvision.com", "source": "官网", "level": "A", "status": "意向"},
    {"name": "杨光", "company": "宁德时代", "industry": "新能源", "phone": "13800138015", "email": "yangguang@catl.com", "source": "推荐", "level": "B", "status": "潜在"},
    {"name": "朱慧", "company": "万科地产", "industry": "房地产", "phone": "13800138016", "email": "zhuhui@vanke.com", "source": "电话", "level": "D", "status": "流失"},
    {"name": "秦鹏", "company": "顺丰速运", "industry": "物流快递", "phone": "13800138017", "email": "qinpeng@sf-express.com", "source": "展会", "level": "C", "status": "谈判"},
    {"name": "许梅", "company": "药明康德", "industry": "医药研发", "phone": "13800138018", "email": "xumei@wuxiapptec.com", "source": "官网", "level": "B", "status": "意向"},
    {"name": "何斌", "company": "大疆创新", "industry": "无人机", "phone": "13800138019", "email": "hebin@dji.com", "source": "推荐", "level": "A", "status": "成交"},
    {"name": "吕芳", "company": "字节跳动", "industry": "互联网", "phone": "13800138020", "email": "lvfang@bytedance.com", "source": "展会", "level": "B", "status": "潜在"},
]

CONTACTS = [
    {"name": "刘助理", "title": "总经理助理", "phone": "13900139001", "email": "liuzl@example.com", "is_primary": True},
    {"name": "陈经理", "title": "采购经理", "phone": "13900139002", "email": "chenjl@example.com", "is_primary": False},
    {"name": "王主管", "title": "技术主管", "phone": "13900139003", "email": "wangzg@example.com", "is_primary": False},
]


def seed():
    with engine.connect() as conn:
        # Clear existing seed data
        conn.execute(text("DELETE FROM contacts"))
        conn.execute(text("DELETE FROM sales_funnel"))
        conn.execute(text("DELETE FROM customers"))
        conn.commit()

        for i, c in enumerate(CUSTOMERS):
            result = conn.execute(
                text(
                    "INSERT INTO customers (name, company, industry, phone, email, source, level, status, created_at, updated_at) "
                    "VALUES (:name, :company, :industry, :phone, :email, :source, :level, :status, :created_at, :updated_at)"
                ),
                {
                    **c,
                    "created_at": datetime.utcnow() - timedelta(days=randint(1, 90)),
                    "updated_at": datetime.utcnow() - timedelta(hours=randint(1, 48)),
                },
            )
            customer_id = result.lastrowid

            # Add 1-3 contacts per customer
            for contact in CONTACTS[: randint(1, 3)]:
                conn.execute(
                    text(
                        "INSERT INTO contacts (customer_id, name, title, phone, email, is_primary) "
                        "VALUES (:customer_id, :name, :title, :phone, :email, :is_primary)"
                    ),
                    {"customer_id": customer_id, **contact},
                )

            # Add funnel entry if status indicates pipeline activity
            if c["status"] in ("潜在", "意向", "谈判"):
                stages = {"潜在": "线索", "意向": "需求", "谈判": "报价", "成交": "成交"}
                stage = stages.get(c["status"], "线索")
                conn.execute(
                    text(
                        "INSERT INTO sales_funnel (customer_id, stage, amount, probability, expected_close) "
                        "VALUES (:customer_id, :stage, :amount, :probability, :expected_close)"
                    ),
                    {
                        "customer_id": customer_id,
                        "stage": stage,
                        "amount": round(randint(5, 200) * 10000 + choice([0, 5000, 8000]), 2),
                        "probability": {"线索": 10, "初访": 25, "需求": 50, "报价": 75, "谈判": 90, "成交": 100}.get(stage, 20),
                        "expected_close": date.today() + timedelta(days=randint(7, 90)),
                    },
                )

            conn.commit()

    print(f"✅ Seeded {len(CUSTOMERS)} customers with contacts and funnel data.")


if __name__ == "__main__":
    seed()
