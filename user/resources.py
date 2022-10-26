from import_export import resources
from blog.models import *

class ProgrammeResources(resources.ModelResource):
    class meta:
        model = Programme