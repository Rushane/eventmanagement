"""empty message

Revision ID: f71ca84bb887
Revises: 52b571990ac1
Create Date: 2019-06-26 18:56:35.999591

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f71ca84bb887'
down_revision = '52b571990ac1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('username', table_name='event_manager')
    op.drop_table('event_manager')
    op.drop_table('comment')
    op.drop_table('rating')
    op.drop_table('guest')
    op.drop_table('event')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('event',
    sa.Column('eventid', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('title', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('category', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('start_date', mysql.DATETIME(), nullable=False),
    sa.Column('end_date', mysql.DATETIME(), nullable=False),
    sa.Column('description', mysql.VARCHAR(length=1000), nullable=False),
    sa.Column('cost', mysql.FLOAT(), nullable=True),
    sa.Column('venue', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('flyer', mysql.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('eventid'),
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    op.create_table('guest',
    sa.Column('guestid', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('displayname', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('email', mysql.VARCHAR(length=180), nullable=True),
    sa.PrimaryKeyConstraint('guestid'),
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    op.create_table('rating',
    sa.Column('rateid', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('rate_value', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('eventid', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['eventid'], ['event.eventid'], name='rating_ibfk_1'),
    sa.PrimaryKeyConstraint('rateid'),
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    op.create_table('comment',
    sa.Column('commentid', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('title', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('comment', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('eventid', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['eventid'], ['event.eventid'], name='comment_ibfk_1'),
    sa.PrimaryKeyConstraint('commentid'),
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    op.create_table('event_manager',
    sa.Column('userid', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('first_name', mysql.VARCHAR(length=80), nullable=True),
    sa.Column('last_name', mysql.VARCHAR(length=80), nullable=True),
    sa.Column('email', mysql.VARCHAR(length=180), nullable=True),
    sa.Column('telnum', mysql.VARCHAR(length=180), nullable=True),
    sa.Column('username', mysql.VARCHAR(length=80), nullable=True),
    sa.Column('password', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('admin', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('userid'),
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    op.create_index('username', 'event_manager', ['username'], unique=True)
    # ### end Alembic commands ###
