"""Create the campus support-ticket table."""
from alembic import op
import sqlalchemy as sa
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table("tickets", sa.Column("id",sa.Integer,primary_key=True),
        sa.Column("title",sa.String(200),nullable=False), sa.Column("description",sa.Text,nullable=False),
        sa.Column("category",sa.String(30),nullable=False), sa.Column("requester",sa.String(120),nullable=False),
        sa.Column("owner",sa.String(120),nullable=False), sa.Column("status",sa.String(30),nullable=False),
        sa.Column("priority",sa.String(20),nullable=False), sa.Column("created_at",sa.DateTime(timezone=True),nullable=False),
        sa.Column("updated_at",sa.DateTime(timezone=True),nullable=False))

def downgrade():
    op.drop_table("tickets")
