from alembic import op
import sqlalchemy as sa

revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("uid", sa.String, unique=True),
        sa.Column("nombre", sa.String),
        sa.Column("email", sa.String, unique=True),
        sa.Column("role", sa.String),
        sa.Column("created_at", sa.DateTime),
    )
    op.create_table(
        "contacts",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("nombre", sa.String, index=True),
        sa.Column("telefono", sa.String, index=True),
        sa.Column("circuito", sa.String, index=True),
        sa.Column("congregacion", sa.String, index=True),
        sa.Column("territorio", sa.String, index=True),
        sa.Column("privilegios", sa.String),
        sa.Column("metadata", sa.JSON),
    )
    op.create_table(
        "channels",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("type", sa.String, nullable=False),
        sa.Column("group_id", sa.Integer),
        sa.Column("created_at", sa.DateTime),
    )
    op.create_table(
        "messages",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("channel_id", sa.Integer, sa.ForeignKey("channels.id")),
        sa.Column("sender_contact_id", sa.Integer, nullable=True),
        sa.Column("body", sa.Text),
        sa.Column("kind", sa.String),
        sa.Column("metadata", sa.JSON),
        sa.Column("created_at", sa.DateTime),
    )
    op.create_table(
        "receipts",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("message_id", sa.Integer, sa.ForeignKey("messages.id")),
        sa.Column("contact_id", sa.Integer, sa.ForeignKey("contacts.id")),
        sa.Column("status", sa.String),
        sa.Column("ts", sa.DateTime),
    )
    op.create_table(
        "reactions",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("message_id", sa.Integer, sa.ForeignKey("messages.id")),
        sa.Column("contact_id", sa.Integer, sa.ForeignKey("contacts.id")),
        sa.Column("tipo", sa.String),
        sa.Column("ts", sa.DateTime),
    )
    op.create_table(
        "search_feedback",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("query", sa.String),
        sa.Column("chosen_contact_id", sa.Integer, sa.ForeignKey("contacts.id")),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("ok", sa.Boolean),
        sa.Column("created_at", sa.DateTime),
    )

def downgrade():
    for t in ["search_feedback","reactions","receipts","messages","channels","contacts","users"]:
        op.drop_table(t)
