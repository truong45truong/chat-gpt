from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from gpt_base.documents.models import Templates,WorkBooks , Documents
from gpt_base.members.models.members import Members

from gpt_base.common.constants.db_fields import DBTemplatesFields,DBWorkBooksFields , DBDocumentsFields


class TemplateDetailListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Templates
        fields = (
            DBTemplatesFields.ID.value,
            DBTemplatesFields.ICON.value,
            DBTemplatesFields.CONTENT.value,
            DBTemplatesFields.TEXTFEATUREBUTTON.value
        )

        
class TemplateDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Templates
        fields = (
            DBTemplatesFields.ID.value,
            DBTemplatesFields.NAME.value,
            DBTemplatesFields.PARAMS.value,
            DBTemplatesFields.HTML.value,
            DBTemplatesFields.ICON.value,
            DBTemplatesFields.CONTENT.value,
            DBTemplatesFields.TEXTFEATUREBUTTON.value,
            DBTemplatesFields.QUESTION_ASKED.value
        )

class WorkBooksCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkBooks
        fields = (
            DBWorkBooksFields.NAME.value,
        )

    def create(self, validated_data, user):
        member = Members.objects.get(user=user)
        workbook = WorkBooks.objects.create(
            **validated_data, member=member
        )
        data = {
            "data": {
                "id": workbook.pk, 
                "name": workbook.name,
                "quantity_document" : 0
            }
        }
        return data

class WorkBookDetailListSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkBooks
        fields = (
            DBWorkBooksFields.ID.value,
            DBWorkBooksFields.NAME.value,
            DBWorkBooksFields.QUANTITY.value,
        )
class WorkBooksUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkBooks
        fields = (
            DBWorkBooksFields.NAME.value,
        )
# ---------------------------------------------------------------------------- #
#                             DOCUMENTS SERIALIZERS                            #
# ---------------------------------------------------------------------------- #
class DocumentsCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Documents
        fields = (
            DBDocumentsFields.CONTENT.value,
            DBDocumentsFields.NAME.value,
            DBDocumentsFields.PARAMS_VALUE.value,
            DBDocumentsFields.WORKBOOK.value,
            DBDocumentsFields.TEMPLATE.value,
        )

    def create(self, validated_data, user,workbook_id, template_id):
        member = Members.objects.get(user=user)
        workbook = WorkBooks.objects.get(id = workbook_id)
        template = Templates.objects.get(id = template_id)
        document = Documents.objects.create(
            **validated_data, member=member,
            workbook = workbook , template = template
        )
        data = {
            "data": {
                "id": document.pk, 
                "name": document.name
            }
        }
        return data

class DocumentsDetailListSerializer(serializers.ModelSerializer):
    template_name = serializers.SerializerMethodField()
    def get_template_name(self, obj):
        return Templates.objects.get(id = obj.template_id).name
    class Meta:
        model = Documents
        fields = (
            DBDocumentsFields.ID.value,
            DBDocumentsFields.NAME.value,
            DBDocumentsFields.WORKBOOK.value,
            DBDocumentsFields.TEMPLATE.value,
            'template_name',
            DBDocumentsFields.CREATED_AT.value,
            DBDocumentsFields.LANGUAGE.value,
        )
class DocumentsDetailSerializer(serializers.ModelSerializer):
    template_name = serializers.SerializerMethodField()
    def get_template_name(self, obj):
        return Templates.objects.get(id = obj.template_id).name
    class Meta:
        model = Documents
        fields = (
            DBDocumentsFields.ID.value,
            DBDocumentsFields.NAME.value,
            DBDocumentsFields.WORKBOOK.value,
            DBDocumentsFields.TEMPLATE.value,
            'template_name',
            DBDocumentsFields.CREATED_AT.value,
            DBDocumentsFields.LANGUAGE.value,
            DBDocumentsFields.CONTENT.value,
        )
class DocumentsUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Documents
        fields = (
            DBDocumentsFields.ID.value,
            DBDocumentsFields.CONTENT.value,
        )