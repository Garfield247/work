"""empty message

Revision ID: fc9d5ee17f0b
Revises: 
Create Date: 2020-06-22 10:00:40.255722

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc9d5ee17f0b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dmp_case',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('dmp_case_name', sa.String(length=32), nullable=False, comment='案例名称'),
    sa.Column('description', sa.String(length=128), nullable=True, comment='案例说明'),
    sa.Column('url_name', sa.String(length=32), nullable=True, comment='可视化网站名称'),
    sa.Column('url', sa.String(length=64), nullable=True, comment='网址'),
    sa.Column('created_on', sa.DateTime(), nullable=False, comment='创建时间'),
    sa.Column('changed_on', sa.DateTime(), nullable=True, comment='修改时间'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dmp_group',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='用户组ID'),
    sa.Column('dmp_group_name', sa.String(length=32), nullable=False, comment='用户组名'),
    sa.Column('created_on', sa.DateTime(), nullable=True, comment='创建时间'),
    sa.Column('changed_on', sa.DateTime(), nullable=True, comment='修改时间'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('dmp_group_name')
    )
    op.create_table('dmp_permission',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='权限ID'),
    sa.Column('route', sa.String(length=64), nullable=False, comment='权限路由'),
    sa.Column('dmp_permission_name', sa.String(length=32), nullable=False, comment='路由功能名称'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dmp_group_permission',
    sa.Column('dmp_group_id', sa.Integer(), nullable=True, comment='用户组ID'),
    sa.Column('dmp_permission_id', sa.Integer(), nullable=True, comment='权限ID'),
    sa.ForeignKeyConstraint(['dmp_group_id'], ['dmp_group.id'], ),
    sa.ForeignKeyConstraint(['dmp_permission_id'], ['dmp_permission.id'], )
    )
    op.create_table('dmp_user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='用户ID'),
    sa.Column('dmp_username', sa.String(length=32), nullable=False, comment='用户名'),
    sa.Column('real_name', sa.String(length=32), nullable=False, comment='真实姓名'),
    sa.Column('email', sa.String(length=32), nullable=False, comment='用户邮箱'),
    sa.Column('passwd', sa.String(length=64), nullable=False, comment='用户密码，加密储存'),
    sa.Column('confirmed', sa.Boolean(), nullable=True, comment='用户激活状态'),
    sa.Column('icon', sa.String(length=128), nullable=True, comment='用户头像'),
    sa.Column('dmp_user_info', sa.String(length=256), nullable=True, comment='个人简介'),
    sa.Column('last_login', sa.DateTime(), nullable=True, comment='最后登录时间'),
    sa.Column('created_on', sa.DateTime(), nullable=True, comment='创建时间'),
    sa.Column('changed_on', sa.DateTime(), nullable=True, comment='修改时间'),
    sa.Column('dmp_group_id', sa.Integer(), nullable=False, comment='所属用户组ID，默认学生用户组'),
    sa.Column('leader_dmp_user_id', sa.Integer(), nullable=True, comment='直属管理者，默认是超级管理员用户, 自关联'),
    sa.ForeignKeyConstraint(['dmp_group_id'], ['dmp_group.id'], ),
    sa.ForeignKeyConstraint(['leader_dmp_user_id'], ['dmp_user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('dmp_username'),
    sa.UniqueConstraint('email')
    )
    op.create_table('dmp_database',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('dmp_database_name', sa.String(length=32), nullable=False, comment='数据显示名称'),
    sa.Column('db_type', sa.Integer(), nullable=False, comment='数据库类型,hive:0,mysql:1,mongo:2'),
    sa.Column('db_host', sa.String(length=32), nullable=False, comment='数据库主机地址'),
    sa.Column('db_port', sa.Integer(), nullable=False, comment='数据库端口号'),
    sa.Column('db_name', sa.String(length=32), nullable=True, comment='数据库名称'),
    sa.Column('db_username', sa.String(length=32), nullable=True, comment='数据库用户名'),
    sa.Column('db_passwd', sa.String(length=64), nullable=True, comment='数据库密码'),
    sa.Column('description', sa.String(length=128), nullable=True, comment='数据库说明'),
    sa.Column('created_on', sa.DateTime(), nullable=False, comment='创建时间'),
    sa.Column('changed_on', sa.DateTime(), nullable=True, comment='修改时间'),
    sa.Column('dmp_user_id', sa.Integer(), nullable=False, comment='所属用户ID'),
    sa.ForeignKeyConstraint(['dmp_user_id'], ['dmp_user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('dmp_database_name')
    )
    op.create_table('dmp_data_table',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('dmp_data_table_name', sa.String(length=32), nullable=False, comment='数据名称'),
    sa.Column('db_table_name', sa.String(length=32), nullable=False, comment='数据库内数据表名称'),
    sa.Column('description', sa.String(length=128), nullable=True, comment='数据说明'),
    sa.Column('created_on', sa.DateTime(), nullable=False, comment='创建时间'),
    sa.Column('changed_on', sa.DateTime(), nullable=True, comment='修改时间'),
    sa.Column('dmp_user_id', sa.Integer(), nullable=False, comment='添加人'),
    sa.Column('dmp_database_id', sa.Integer(), nullable=False, comment='数据库ID'),
    sa.Column('dmp_case_id', sa.Integer(), nullable=False, comment='所属案例ID'),
    sa.ForeignKeyConstraint(['dmp_case_id'], ['dmp_case.id'], ),
    sa.ForeignKeyConstraint(['dmp_database_id'], ['dmp_database.id'], ),
    sa.ForeignKeyConstraint(['dmp_user_id'], ['dmp_user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('dmp_data_table_name')
    )
    op.create_table('dmp_from_add_data_table',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('dmp_data_table_name', sa.String(length=64), nullable=True, comment='数据名称'),
    sa.Column('db_table_name', sa.String(length=32), nullable=False, comment='数据库内数据表名称'),
    sa.Column('submit_on', sa.DateTime(), nullable=False, comment='提交时间'),
    sa.Column('description', sa.String(length=128), nullable=True, comment='说明'),
    sa.Column('approve_on', sa.DateTime(), nullable=True, comment='审批时间'),
    sa.Column('approve_result', sa.Integer(), nullable=True, comment='审批结果,默认:0,通过:1,不通过:2'),
    sa.Column('answer', sa.String(length=32), nullable=True, comment='审批答复'),
    sa.Column('created_on', sa.DateTime(), nullable=False, comment='创建时间'),
    sa.Column('changed_on', sa.DateTime(), nullable=True, comment='修改时间'),
    sa.Column('submit_dmp_user_id', sa.Integer(), nullable=False, comment='提交人'),
    sa.Column('dmp_database_id', sa.Integer(), nullable=False, comment='数据库ID'),
    sa.Column('dmp_case_id', sa.Integer(), nullable=False, comment='所属案例ID'),
    sa.Column('approve_dmp_user_id', sa.Integer(), nullable=True, comment='审批人'),
    sa.ForeignKeyConstraint(['approve_dmp_user_id'], ['dmp_user.id'], ),
    sa.ForeignKeyConstraint(['dmp_case_id'], ['dmp_case.id'], ),
    sa.ForeignKeyConstraint(['dmp_database_id'], ['dmp_database.id'], ),
    sa.ForeignKeyConstraint(['submit_dmp_user_id'], ['dmp_user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('dmp_data_table_name')
    )
    op.create_table('dmp_from_upload',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('filetype', sa.Integer(), nullable=False, comment='文件类型'),
    sa.Column('filepath', sa.String(length=128), nullable=False, comment='文件路径'),
    sa.Column('column_line', sa.Integer(), nullable=True, comment='列名行号'),
    sa.Column('column', sa.String(length=32), nullable=True, comment='自定义列名'),
    sa.Column('json_dimension_reduction', sa.Boolean(), nullable=True, comment='json数据是否遍历存储'),
    sa.Column('new_table_name', sa.String(length=32), nullable=False, comment='表名'),
    sa.Column('method', sa.Integer(), nullable=True, comment='新建1、添加2或覆盖3'),
    sa.Column('description', sa.String(length=128), nullable=True, comment='说明'),
    sa.Column('submit_on', sa.DateTime(), nullable=False, comment='提交时间'),
    sa.Column('approve_on', sa.DateTime(), nullable=True, comment='审批时间'),
    sa.Column('approve_result', sa.Integer(), nullable=True, comment='审批结果,默认:0,通过:1,不通过:2'),
    sa.Column('answer', sa.String(length=32), nullable=True, comment='审批答复'),
    sa.Column('upload', sa.Boolean(), nullable=True, comment='是否成功'),
    sa.Column('upload_result', sa.String(length=32), nullable=True, comment='数据上传结果'),
    sa.Column('created_on', sa.DateTime(), nullable=False, comment='创建时间'),
    sa.Column('changed_on', sa.DateTime(), nullable=True, comment='修改时间'),
    sa.Column('submit_dmp_user_id', sa.Integer(), nullable=False, comment='提交人'),
    sa.Column('destination_dmp_database_id', sa.Integer(), nullable=False, comment='目标数据库ID'),
    sa.Column('dmp_case_id', sa.Integer(), nullable=False, comment='所属案例'),
    sa.Column('approve_dmp_user_id', sa.Integer(), nullable=True, comment='审批人'),
    sa.ForeignKeyConstraint(['approve_dmp_user_id'], ['dmp_user.id'], ),
    sa.ForeignKeyConstraint(['destination_dmp_database_id'], ['dmp_database.id'], ),
    sa.ForeignKeyConstraint(['dmp_case_id'], ['dmp_case.id'], ),
    sa.ForeignKeyConstraint(['submit_dmp_user_id'], ['dmp_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dmp_data_table_column',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('dmp_data_table_column_name', sa.String(length=32), nullable=False, comment='列名'),
    sa.Column('groupby', sa.Boolean(), nullable=True, comment='可以进行分组'),
    sa.Column('wherein', sa.Boolean(), nullable=True, comment='可以区间筛选'),
    sa.Column('isdate', sa.Boolean(), nullable=True, comment='是否为时间日期字段'),
    sa.Column('description', sa.String(length=128), nullable=True, comment='字段说明'),
    sa.Column('dmp_data_table_id', sa.Integer(), nullable=False, comment='数据ID'),
    sa.ForeignKeyConstraint(['dmp_data_table_id'], ['dmp_data_table.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dmp_from_download',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('rule', sa.String(length=64), nullable=True, comment='数据库提取规则'),
    sa.Column('description', sa.String(length=128), nullable=True, comment='说明'),
    sa.Column('submit_on', sa.DateTime(), nullable=False, comment='提交时间'),
    sa.Column('approve_on', sa.DateTime(), nullable=True, comment='审批时间'),
    sa.Column('approve_result', sa.Integer(), nullable=True, comment='审批结果,默认:0,通过:1,不通过:2'),
    sa.Column('answer', sa.String(length=32), nullable=True, comment='审批答复'),
    sa.Column('ftp_url', sa.String(length=64), nullable=True, comment='FTP下载链接'),
    sa.Column('ftp_pid', sa.Integer(), nullable=True, comment='FTP进程号'),
    sa.Column('filepath', sa.String(length=128), nullable=True, comment='文件路径'),
    sa.Column('finish', sa.Boolean(), nullable=True, comment='是否完成'),
    sa.Column('created_on', sa.DateTime(), nullable=False, comment='创建时间'),
    sa.Column('changed_on', sa.DateTime(), nullable=True, comment='修改时间'),
    sa.Column('submit_dmp_user_id', sa.Integer(), nullable=False, comment='提交人'),
    sa.Column('dmp_data_table_id', sa.Integer(), nullable=False, comment='源数据表ID'),
    sa.Column('approve_dmp_user_id', sa.Integer(), nullable=True, comment='审批人'),
    sa.ForeignKeyConstraint(['approve_dmp_user_id'], ['dmp_user.id'], ),
    sa.ForeignKeyConstraint(['dmp_data_table_id'], ['dmp_data_table.id'], ),
    sa.ForeignKeyConstraint(['submit_dmp_user_id'], ['dmp_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dmp_from_migrate',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('rule', sa.String(length=64), nullable=True, comment='数据库提取规则'),
    sa.Column('new_table_name', sa.String(length=32), nullable=False, comment='新表名'),
    sa.Column('method', sa.Integer(), nullable=True, comment='新建1、覆盖2或添加3'),
    sa.Column('description', sa.String(length=128), nullable=True, comment='说明'),
    sa.Column('submit_on', sa.DateTime(), nullable=False, comment='提交时间'),
    sa.Column('approve_on', sa.DateTime(), nullable=True, comment='审批时间'),
    sa.Column('approve_result', sa.Integer(), nullable=True, comment='审批结果,默认:0,通过:1,不通过:2'),
    sa.Column('answer', sa.String(length=32), nullable=True, comment='审批答复'),
    sa.Column('migrate', sa.Boolean(), nullable=True, comment='迁移成功'),
    sa.Column('migrate_result', sa.String(length=32), nullable=True, comment='迁移结果'),
    sa.Column('created_on', sa.DateTime(), nullable=False, comment='创建时间'),
    sa.Column('changed_on', sa.DateTime(), nullable=True, comment='修改时间'),
    sa.Column('submit_dmp_user_id', sa.Integer(), nullable=False, comment='提交人'),
    sa.Column('origin_dmp_table_id', sa.Integer(), nullable=False, comment='起点数据表'),
    sa.Column('destination_dmp_database_id', sa.Integer(), nullable=False, comment='目标数据库ID'),
    sa.Column('approve_dmp_user_id', sa.Integer(), nullable=True, comment='审批人'),
    sa.ForeignKeyConstraint(['approve_dmp_user_id'], ['dmp_user.id'], ),
    sa.ForeignKeyConstraint(['destination_dmp_database_id'], ['dmp_database.id'], ),
    sa.ForeignKeyConstraint(['origin_dmp_table_id'], ['dmp_data_table.id'], ),
    sa.ForeignKeyConstraint(['submit_dmp_user_id'], ['dmp_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dmp_data_table_column_range',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('context', sa.String(length=256), nullable=True, comment='内容'),
    sa.Column('dmp_data_table_column_id', sa.Integer(), nullable=False, comment='列ID'),
    sa.ForeignKeyConstraint(['dmp_data_table_column_id'], ['dmp_data_table_column.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dmp_data_table_column_range')
    op.drop_table('dmp_from_migrate')
    op.drop_table('dmp_from_download')
    op.drop_table('dmp_data_table_column')
    op.drop_table('dmp_from_upload')
    op.drop_table('dmp_from_add_data_table')
    op.drop_table('dmp_data_table')
    op.drop_table('dmp_database')
    op.drop_table('dmp_user')
    op.drop_table('dmp_group_permission')
    op.drop_table('dmp_permission')
    op.drop_table('dmp_group')
    op.drop_table('dmp_case')
    # ### end Alembic commands ###
