from marshmallow import Schema, fields


class NewsResponseSchema(Schema):
    message = fields.String(
        dump_default='Yes',
        required=True,
        description='just kal'
    )
    date_to = fields.String(
        required=True,
        description='Дата до'
    )
    date_from = fields.String(
        required=True,
        description='Дата от'
    )


class NewsRequestSchema(Schema):
    api_type = fields.String(
        name='',
        required=True,
        description="API type new-interview schema"
    )
    date_to = fields.String(
        required=True,
        description='Дата до'
    )
    date_from = fields.String(
        required=True,
        description='Дата от'
    )


class News(Schema):
    news_id = fields.Integer(
        name='news_id',
        required=True
    )
    title = fields.String(
        name='title',
        required=True
    )
    news_image = fields.String(
        name='news_image',
        required=True
    )
    news_date = fields.String(
        name='news_date',
        required=True
    )

