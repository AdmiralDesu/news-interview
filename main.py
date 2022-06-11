from flask import Flask
from flask_restful import Resource, Api
from apispec import APISpec
from marshmallow import Schema, fields
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs


app = Flask(__name__)
api = Api(app)
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='news-interview',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI для доступа к swagger JSON
    'APISPEC_SWAGGER_UI_URL': '/docs/'  # URI для доступа к swagger GUI
})
docs = FlaskApiSpec(app)


class NewsResponseSchema(Schema):
    name = fields.Str()
    message = fields.Str(dump_default='Success')


class NewsRequestSchema(Schema):
    api_type = fields.String(
        name='',
        required=True,
        description="API type new-interview schama"
    )


class NewsAPI(MethodResource, Resource):
    @doc(
        description='GET method',
        tags=['News']
    )
    @marshal_with(NewsResponseSchema)  # marshalling
    def get(self, name):
        '''
        Get method represents a GET API method
        '''
        return {'message': f'{name}'}

    @doc(description='POST method', tags=['1st'])
    @use_kwargs(NewsRequestSchema, location='json')
    @marshal_with(NewsResponseSchema)  # marshalling
    def post(self):
        """
        Get method represents a GET API method
        """
        return {
            'message': 'PUT endpoint'
        }


api.add_resource(NewsAPI, '/test/<string:name>')
docs.register(NewsAPI)

if __name__ == '__main__':
    app.run(debug=True)
