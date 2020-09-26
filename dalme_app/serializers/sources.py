from django.contrib.auth.models import User
from dalme_app.models import Agent, Attribute_type, Content_attributes, Set, Set_x_content, Source, Source_credit
from dalme_app.models._templates import get_current_user
from rest_framework import serializers
from ._common import DynamicSerializer, translate_workflow_status
import dalme_app.serializers.users as _users
import dalme_app.serializers.attributes as _attributes
import dalme_app.serializers.others as _others
import dalme_app.serializers.workflow as _workflow
import dalme_app.serializers.sets as _sets


class SourceSetSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='set_id.id', required=True)
    name = serializers.ReadOnlyField(source='set_id.name', required=False)
    detail_string = serializers.ReadOnlyField(source='set_id.detail_string', required=False)

    class Meta:
        model = Set_x_content
        fields = ('id', 'name', 'detail_string')


class SourceCreditSerializer(DynamicSerializer):
    agent = serializers.ReadOnlyField(source='agent.standard_name', required=False)
    agent_id = serializers.ReadOnlyField(source='agent.id', required=False)
    notes = serializers.ReadOnlyField(source='agent.notes', required=False)

    class Meta:
        model = Source_credit
        fields = ('id', 'type', 'agent', 'agent_id', 'notes')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['type'] = {
            'id': instance.type,
            'name': instance.get_type_display()
        }
        ret['agent'] = {
            'id': ret.pop('agent_id'),
            'standard_name': ret['agent']
        }
        return ret


class SourceSerializer(DynamicSerializer):
    attributes = _attributes.AttributeSerializer(many=True, required=False)
    inherited = _attributes.AttributeSerializer(many=True, required=False)
    tags = _others.TagSerializer(many=True, required=False)
    workflow = _workflow.WorkflowSerializer(required=False)
    sets = SourceSetSerializer(many=True, required=False)
    pages = _others.PageSerializer(many=True, required=False)
    owner = _users.UserSerializer(fields=['full_name', 'username', 'id'])
    credits = SourceCreditSerializer(many=True, required=False)
    primary_dataset = _sets.SetSerializer(fields=['id', 'name', 'detail_string'], required=False)

    class Meta:
        model = Source
        fields = ('id', 'type', 'name', 'short_name', 'parent', 'has_inventory', 'primary_dataset', 'attributes', 'inherited', 'credits',
                  'no_folios', 'no_images', 'tags', 'workflow', 'owner', 'sets', 'pages', 'no_records', 'is_private')
        extra_kwargs = {
                        'parent': {'required': False},
                        'no_folios': {'required': False},
                        'no_images': {'required': False},
                        'primary_dataset': {'required': False}
                        }

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if ret.get('attributes') is not None:
            ret['attributes'] = self.process_attributes(ret.pop('attributes'), instance)
        if ret.get('inherited') is not None:
            if ret['inherited'] is not None:
                ret['inherited'] = self.process_attributes(ret.pop('inherited'))
        if ret.get('parent') is not None:
            if ret['parent']:
                ret['parent'] = {'id': ret['parent'], 'name': instance.parent.name}
        if ret.get('type') is not None:
            ret['type'] = {
                'name': instance.type.name,
                'id': ret['type']
            }
        for k, v in dict(ret).items():
            if v is None:
                ret.pop(k)
        return ret

    def to_internal_value(self, data):
        try:
            ct = self.instance.type
        except AttributeError:
            ct = data['type']
        multi_attributes = [i.attribute_type.short_name for i in Content_attributes.objects.filter(content_type=ct) if not i.unique]
        deserialised = []
        for key, value in data['attributes'].items():
            att_type = Attribute_type.objects.get(short_name=key)
            if key in multi_attributes and value == 0:
                continue
            value_list = value if key in multi_attributes else [value]
            for v in value_list:
                if v is not None:
                    att = {'attribute_type': att_type.id}
                    add_att = True
                    if att_type.data_type == 'INT':
                        att['value_INT'] = int(v)
                    elif att_type.data_type == 'TXT':
                        att['value_TXT'] = v
                    elif att_type.data_type == 'DATE':
                        if v['d'] is None and v['m'] is None and v['y'] is None:
                            add_att = False
                        else:
                            att['value_DATE_d'] = v['d']
                            att['value_DATE_m'] = v['m']
                            att['value_DATE_y'] = v['y']
                    elif att_type.data_type == 'FK-INT' or att_type.data_type == 'FK-UUID':
                        if type(v) is dict and v.get('id') is not None:
                            att['value_JSON'] = json.loads(v['id'])
                        elif type(v) is str and v != '':
                            att['value_JSON'] = json.loads(v)
                        else:
                            add_att = False
                    else:
                        att['value_STR'] = v
                    if add_att:
                        deserialised.append(att)
        data['attributes'] = deserialised

        if data.get('workflow') is not None and data['workflow'].get('status') is not None:
            if data['workflow']['status']['text'] is not None:
                values = translate_workflow_status(data['workflow']['status']['text'])
                data['workflow']['wf_status'] = values['wf_status']
                data['workflow']['stage'] = values['stage']
            else:
                data['workflow'].pop('status')

        credits = data.pop('credits')
        if credits != 0:
            self.context['credits'] = credits

        if data.get('sets') is not None and data.get('sets') == 0:
            data.pop('sets')

        if data.get('pages') is not None and data.get('pages') == 0:
            data.pop('pages')

        if data.get('owner') is None:
            data['owner'] = get_current_user().id

        return super().to_internal_value(data)

    def create(self, validated_data):
        attributes_data = validated_data.pop('attributes') if validated_data.get('attributes') is not None else False
        workflow_data = validated_data.pop('workflow') if validated_data.get('workflow') is not None else False
        pages_data = validated_data.pop('pages') if validated_data.get('pages') is not None else False
        sets_list = [i['set_id'] for i in validated_data.pop('sets')] if validated_data.get('sets') is not None else False
        credits_data = self.context['credits'] if self.context.get('credits') is not None else False

        if validated_data.get('owner') is not None:
            validated_data['owner'] = User.objects.get(username=validated_data['owner']['username'])
        # else:
        #     validated_data['owner'] = get_current_user()

        source = Source.objects.create(**validated_data)

        if attributes_data:
            for attribute in attributes_data:
                source.attributes.create(**attribute)

        if workflow_data:
            workflow = source.workflow
            if workflow_data.get('status') is not None:
                status_data = translate_workflow_status(workflow_data['status'])
                workflow.wf_status = status_data.get('wf_status', workflow.wf_status)
                workflow.stage = status_data.get('stage', workflow.stage)
            workflow.help_flag = workflow_data.get('help_flag', workflow.help_flag)
            workflow.is_public = workflow_data.get('is_public', workflow.is_public)
            workflow.save()

        if pages_data:
            for page in pages_data:
                source.pages.create(**page)

        if sets_list:
            for _set in sets_list:
                Set_x_content.objects.create(set_id=_set, content_object=source)

        if credits_data:
            for credit in credits_data:
                credit.pop('id')
                agent = Agent.objects.get(pk=credit.pop('standard_name'))
                Source_credit.objects.create(source=source, agent=agent, **credit)

        return source

    def update(self, instance, validated_data):
        if validated_data.get('attributes') is not None:
            attributes_data = validated_data.pop('attributes')
            multi_attributes = [i.attribute_type for i in Content_attributes.objects.filter(content_type=instance.type) if not i.unique]
            attributes = {}
            for attribute in attributes_data:
                if attribute['attribute_type'] in multi_attributes:
                    if attributes.get(attribute['attribute_type']) is not None:
                        attributes[attribute['attribute_type']].append(attribute)
                    else:
                        attributes[attribute['attribute_type']] = [attribute]
                else:
                    attributes[attribute['attribute_type']] = attribute

            current_attributes = instance.attributes.all()
            control = []

            for att_type, attribute_dict in attributes.items():
                if type(attribute_dict) is list:
                    current_attributes.filter(attribute_type=att_type).delete()
                    for att in attribute_dict:
                        na = instance.attributes.create(**att)
                        control.append(na.id)
                else:
                    if current_attributes.filter(**attribute_dict).exists():
                        control.append(current_attributes.get(**attribute_dict).id)
                    elif current_attributes.filter(attribute_type=att_type).count() > 0:
                        attribute = current_attributes.get(attribute_type=att_type)
                        attribute_dict.pop('attribute_type')
                        for attr, value in attribute_dict.items():
                            setattr(attribute, attr, value)
                        attribute.save()
                        control.append(attribute.id)
                    else:
                        na = instance.attributes.create(**attribute_dict)
                        control.append(na.id)

            for attribute in current_attributes:
                if attribute.id not in control:
                    attribute.delete()

        if validated_data.get('workflow') is not None:
            workflow_data = validated_data.pop('workflow')
            workflow = instance.workflow
            if workflow_data.get('status') is not None:
                status_data = translate_workflow_status(workflow_data['status'])
                workflow.wf_status = status_data.get('wf_status', workflow.wf_status)
                workflow.stage = status_data.get('stage', workflow.stage)
            workflow.help_flag = workflow_data.get('help_flag', workflow.help_flag)
            workflow.is_public = workflow_data.get('is_public', workflow.is_public)
            workflow.save()

        if validated_data.get('pages') is not None:
            pages_data = validated_data.pop('pages')
            current_pages = instance.pages.all()
            control = []
            for page_dict in pages_data:
                if current_pages.filter(**page_dict).exists():
                    control.append(current_pages.get(**page_dict).id)
                else:
                    if page_dict.get('id') is not None:
                        page = current_pages.get(pk=page_dict['id'])
                        for attr, value in page_dict.items():
                            setattr(page, attr, value)
                        page.save()
                        control.append(page.id)
                    else:
                        np = instance.pages.create(**page_dict)
                        control.append(np.id)
            for page in current_pages:
                if page.id not in control:
                    page.delete()

        if validated_data.get('sets') is not None:
            sets = validated_data.pop('sets')
            sets_list = [i['set_id']['id'] for i in sets]
            current_sets_list = [i.set_id.id for i in instance.sets.all()]
            for _set in sets_list:
                if _set not in current_sets_list:
                    set_object = Set.objects.get(pk=_set)
                    Set_x_content.objects.create(set_id=set_object, content_object=instance)
            for _set in current_sets_list:
                if _set not in sets_list:
                    instance.sets.get(set_id=_set.id).delete()

        if self.context.get('credits') is not None:
            credits = self.context['credits']
            current_credits = [i.id for i in instance.credits.all()]
            for credit in credits:
                if credit.get('id') is not None:
                    obj = Source_credit.objects.get(pk=credit.pop('id'))
                    agent = Agent.objects.get(pk=credit.pop('standard_name'))
                    obj.agent = agent
                    obj.note = credit['note']
                    obj.type = credit['type']
                    obj.save()
                    current_credits.remove(obj.id)
                else:
                    credit.pop('id')
                    agent = Agent.objects.get(pk=credit.pop('standard_name'))
                    Source_credit.objects.create(source=instance, agent=agent, **credit)
            if current_credits:
                for c in current_credits:
                    Source_credit.objects.get(pk=c).delete()

        if validated_data.get('owner') is not None:
            validated_data['owner'] = User.objects.get(username=validated_data['owner']['username'])

        return super().update(instance, validated_data)

    def deserialise_numbered_dict(self, data):
        deserialised = []
        for key, value in data.items():
            deserialised.append(value)
        return deserialised

    def process_attributes(self, qset, instance):
        result = {}
        multi_attributes = [i.attribute_type.short_name for i in Content_attributes.objects.filter(content_type=instance.type) if not i.unique]
        for i in qset:
            (k, v), = i.items()
            if k in multi_attributes:
                if result.get(k) is not None:
                    result[k].append(v)
                else:
                    result[k] = [v]
            else:
                result[k] = v
        return result
