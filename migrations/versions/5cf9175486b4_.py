"""empty message

Revision ID: 5cf9175486b4
Revises: 
Create Date: 2021-07-13 15:10:27.838330

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "5cf9175486b4"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "meeting",
        sa.Column("date", sa.DateTime(), nullable=False),
        sa.Column("link", sa.String(length=500), nullable=True),
        sa.PrimaryKeyConstraint("date"),
    )
    op.create_table(
        "label",
        sa.Column(
            "id", sa.Integer().with_variant(sa.Integer(), "sqlite"), nullable=False
        ),
        sa.Column("name", sa.String(length=80), nullable=False),
        sa.Column("meeting_date", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["meeting_date"],
            ["meeting.date"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "participant",
        sa.Column(
            "id", sa.Integer().with_variant(sa.Integer(), "sqlite"), nullable=False
        ),
        sa.Column("name", sa.String(length=80), nullable=False),
        sa.Column("meeting_date", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["meeting_date"],
            ["meeting.date"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("participant")
    op.drop_table("label")
    op.drop_table("meeting")
    # ### end Alembic commands ###
