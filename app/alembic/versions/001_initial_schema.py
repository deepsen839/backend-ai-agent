from alembic import op
import sqlalchemy as sa


revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        "sessions",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True
        ),

        sa.Column(
            "session_id",
            sa.String()
        ),

        sa.Column(
            "user_id",
            sa.String()
        ),

        sa.Column(
            "created_at",
            sa.DateTime()
        )
    )

    op.create_table(
        "conversations",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True
        ),

        sa.Column(
            "session_id",
            sa.String()
        ),

        sa.Column(
            "user_id",
            sa.String()
        ),

        sa.Column(
            "role",
            sa.String()
        ),

        sa.Column(
            "content",
            sa.Text()
        ),

        sa.Column(
            "created_at",
            sa.DateTime()
        )
    )

    op.create_table(
        "memory_facts",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True
        ),

        sa.Column(
            "user_id",
            sa.String()
        ),

        sa.Column(
            "fact",
            sa.Text()
        ),

        sa.Column(
            "created_at",
            sa.DateTime()
        )
    )

    op.create_table(
        "eval_logs",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True
        ),

        sa.Column(
            "user_id",
            sa.String()
        ),

        sa.Column(
            "session_id",
            sa.String()
        ),

        sa.Column(
            "groundedness",
            sa.Float()
        ),

        sa.Column(
            "relevance",
            sa.Float()
        ),

        sa.Column(
            "confidence",
            sa.Float()
        ),

        sa.Column(
            "flagged",
            sa.Boolean()
        ),

        sa.Column(
            "reasoning",
            sa.Text()
        ),

        sa.Column(
            "created_at",
            sa.DateTime()
        )
    )

    op.create_table(
        "escalations",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True
        ),

        sa.Column(
            "user_id",
            sa.String()
        ),

        sa.Column(
            "reason",
            sa.Text()
        ),

        sa.Column(
            "created_at",
            sa.DateTime()
        )
    )


def downgrade():

    op.drop_table(
        "escalations"
    )

    op.drop_table(
        "eval_logs"
    )

    op.drop_table(
        "memory_facts"
    )

    op.drop_table(
        "conversations"
    )

    op.drop_table(
        "sessions"
    )