from django_elasticsearch_dsl import DocType, Index
from mattersmithapp.models import *

user = Index('user')

@user.doc_type
class userTrack(DocType):
    class Meta:
        model = User

        fields = [
            'first_name',
            'last_name',
            'username',
            
        ]