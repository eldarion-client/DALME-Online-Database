"""
This file houses all of the miscellaneous functions used elsewhere in the project.
"""
import os
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models import Q
from django.db import connections
from dalme_app.menus import menu_constructor
from urllib.parse import urlencode
import re, json, requests, hashlib, os, uuid, calendar, datetime
import pandas as pd
import lxml.etree as etree
from random import randint

from dalme_app import menus
from dalme_app.models import *
from functools import wraps

import logging
logger = logging.getLogger(__name__)

try:
    from dalme_app.scripts.db import wp_db, wiki_db, dam_db
except:
    logger.debug("Can't connect to MySQL instance containing Wiki, DAM, and WP databases.")


#Security and permissions functions
def check_group(request, group_name):
    """
    Checks if the current user is a member of the passed group.
    """
    try:
        if request.user.is_superuser:
        #if request.user.groups.filter(name=group_name).exists() or request.user.is_superuser:
            result = True
        else:
            result = False
    except:
        result = False

    return result

def in_group(group_name):
    """
    Takes a group name and checks whether the current user is in the group.
    Used by adding as decorator before function/class: @functions.in_group('group_name')
    """
    def _in_group(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            #print request.user
            if request.user.is_anonymous:
                return redirect('/admin/')
            if (not (request.user.groups.filter(name=group_name).exists())
                or request.user.is_superuser):
                raise Http404
            return view_func(request, *args, **kwargs)
        return wrapper
    return _in_group

#General functions
def set_menus(request, context, state):
    bc = []
    for i in state['breadcrumb']:
        bc.append(i[0])
    state['breadcrumb'] = bc
    context['dropdowns'] = menu_constructor(request, 'dropdown_item', 'dropdowns_default.json', state)
    context['sidebar'] = menu_constructor(request, 'sidebar_item', 'sidebar_default.json', state)
    return context

def notification(request, **kwargs):
    if 'level' and 'text' in kwargs:
        msg_level = eval('messages.'+kwargs['level'])
        msg_output = kwargs['text']
    elif 'code' in kwargs:
        base_message = Notification.objects.get(code=code)
        msg_text = base_message.text
        msg_level = base_message.level

        if 'para' in kwargs:
            para = kwargs['para']
            msg_output = msg_text.format(**para)
        elif 'data' in kwargs:
            data = kwargs['data']
            msg_output = msg_text + '<p>' + str(data) + '</p>'
        else:
            msg_output = msg_text
    else:
        msg_level = 'DEBUG'
        msg_output = 'There was a problem processing this notification: No notification code was supplied.'

    if 'user' in kwargs:
        user = kwargs['user']
        the_user = User.objects.get(username=user)
        message_user(the_user, msg_output, msg_level)

    else:
        messages.add_message(request, msg_level, msg_output)

def format_date(value, type):
    if type == 'timestamp':
        try:
            date_str = value.strftime('%d-%b-%Y@%H:%M')
        except:
            date_str = str(value)
    elif type == 'attribute':
        if value.value_DATE_d == None or value.value_DATE_m == None or value.value_DATE_y == None:
            date_str = value.value_STR
        else:
            date_str = value.value_DATE.strftime('%A, %d %B, %Y').lstrip("0").replace(" 0", " ")
    else:
        date_str = str(value)

    return date_str

#module-specific functions
def get_editor_folios(source):
    folios = source.pages.all().order_by('order')
    folio_count = len(folios)
    editor_folios = { 'folio_count': folio_count }
    folio_list = []
    if folio_count == 1:
        folio_menu = '<div class="single_folio">Folio {} (1/1)</div>'.format(folios[0].name)
        folio_dict = {
            'name': folios[0].name,
            'id': str(folios[0].id),
            'dam_id': str(folios[0].dam_id),
            'order': str(folios[0].order)
            }
        transcription = Source_pages.objects.get(source_id=source.id, page_id=folios[0].id)
        if transcription.transcription_id:
            folio_dict['tr_id'] = str(transcription.transcription_id)
            transcription_version = transcription.transcription_id.version
            if transcription_version:
                folio_dict['tr_version'] = transcription_version
            else:
                folio_dict['tr_version'] = 0
        else:
            folio_dict['tr_id'] = "None"
            folio_dict['tr_version'] = 0
        folio_list.append(folio_dict)
    else:
        folio_menu = '<div class="disabled-btn-left"><i class="fa fa-caret-left fa-fw"></i></div>'
        count = 1
        for f in folios:
            folio_dict = {
                'name': f.name,
                'id': str(f.id),
                'dam_id': str(f.dam_id),
                'order': str(f.order)
                }
            transcription = Source_pages.objects.get(source_id=source.id, page_id=f.id)
            if transcription.transcription_id:
                folio_dict['tr_id'] = str(transcription.transcription_id)
                transcription_version = transcription.transcription_id.version
                if transcription_version:
                    folio_dict['tr_version'] = transcription_version
                else:
                    folio_dict['tr_version'] = 0
            else:
                folio_dict['tr_id'] = "None"
                folio_dict['tr_version'] = 0
            if count == 1:
                folio_menu += '<button id="folios" type="button" class="editor-btn button-border-left" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Folio {} (1/{})</button><div class="dropdown-menu" aria-labelledby="folios">'.format(f.name,folio_count)
                folio_menu += '<div class="current-folio-menu">Folio {}</div>'.format(f.name)
            elif count == 2:
                next = f.name
                folio_menu += '<a class="dropdown-item" href="#" id="{}" onclick="folioSwitch(this.id)">Folio {}</a>'.format(f.name, f.name)
            else:
                folio_menu += '<a class="dropdown-item" href="#" id="{}" onclick="folioSwitch(this.id)">Folio {}</a>'.format(f.name, f.name)
            count = count + 1
            folio_list.append(folio_dict)

        folio_menu += '</div><button type="button" class="editor-btn button-border-left" id="{}" onclick="folioSwitch(this.id)"><i class="fa fa-caret-right fa-fw"></i></button>'.format(next)

    editor_folios['folio_menu'] = folio_menu
    editor_folios['folio_list'] = folio_list

    return editor_folios

def render_transcription(transcription):
    try:
        dom = etree.fromstring(transcription)
        xslt = etree.parse(os.path.join(settings.BASE_DIR, 'dalme_app/templates/xslt/tei_transcription.xslt'))
        transform = etree.XSLT(xslt)
        newdom = transform(dom)
        render = etree.tostring(newdom)
    except:
        render = '<b>Rendering failed.</b>'
    return render

def get_attribute_value(attribute):
    dt = attribute.attribute_type.data_type
    if dt == 'DATE':
        value = format_date(attribute, 'attribute')
    else:
        value = eval('attribute.value_'+dt)
    return value

def add_filter_options(values, filter, mode='complete'):
    if mode == 'strict':
        op = []
    elif mode == 'check':
        op = [{'label':'None'}]
    else:
        op = [{'label':'Any'}, {'label':'None'}, {'label':'divider'}]

    for d in values:
        v = list(d.values())[0]
        if v != '':
            op.append({'label':v})
    filter['options'] = op
    return filter

def get_dam_user(ref,output):
    user = rs_user.objects.get(ref=ref).username
    try:
        c_user = Profile.objects.get(user__username=str(user))
        if output == 'html':
            ret = '<a href="/user/{}">{}</a>'.format(c_user.user_id, c_user.full_name)
        else:
            ret = str(c_user.username)
    except:
        ret = str(user)

    return ret

def get_page_chain(breadcrumb, current=None):
    i_count = len(breadcrumb)
    title = ''
    if current and current != breadcrumb[i_count-1][0]:
        if len(current) > 55:
            current = current[:55] + ' <i class="fa fa-plus-circle fa-fw" data-toggle="tooltip" data-placement="bottom" title="{}"></i> '.format(current)
        for i in breadcrumb:
            if i[1] != '':
                title += '<a href="{}" class="title_link">{}</a>'.format(i[1],i[0])
            else:
                title += i[0]
            title += ' <i class="fa fa-caret-right fa-fw"></i> '
        title += '<span class="title_current">{}</span>'.format(current)
    else:
        c = 0
        while c <= i_count - 1:
            if c == i_count - 1:
                title += '<span class="title_current">{}</span>'.format(breadcrumb[c][0])
            else:
                title += breadcrumb[c][0] + ' <i class="fa fa-caret-right fa-fw"></i> '
            c = c + 1
    return title

def get_dam_preview(resource):
    """
    Returns the url for an image from the ResourceSpace Digital Asset Management
    system for the given resource.
    """
    endpoint = 'https://dam.dalme.org/api/?'
    user = 'api_bot'
    key = os.environ['DAM_API_KEY']
    queryParams = {
        "function": "search_get_previews",
        "param1": '!list'+str(resource),
        "param2": "",
        "param3": "",
        "param4": "0",
        "param5": "1",
        "param6": "asc",
        "param7": "",
        "param8": "scr",
        "param9": "jpg",
    }
    try:
        response = rs_api_query(endpoint, user, key, **queryParams)
        data = json.loads(response.text)
        preview_url = data[0]['url_scr']
    except:
        preview_url = None

    return preview_url

def get_unique_username(username, app):
    try:
        if app == 'wp':
            exists = wp_users.objects.get(user_login=username)
        if app == 'wiki':
            exists = wiki_user.objects.get(user_name=bytes(username, encoding='ascii'))
        if app == 'dam':
            exists = rs_user.objects.get(username=username)
    except:
        exists = False
    if exists:
        username = username + str(randint(100, 999))
    return username

def get_count(item):
    """
    Gets counts of different types of content based on `item` input string.
    Valid values are: "inventories", "objects", "wiki-articles", "assets", "notarial_sources", "sources", "biblio_sources", "archives".
    All other values for `item` return None
    """
    if item == 'inventories':
        return Source.objects.filter(is_inventory=True).count()

    elif item == 'archives':
        return Source.objects.filter(type=19).count()

    elif item == 'sources':
        return Source.objects.count()

    elif item == 'notarial_sources':
        return Source.objects.filter(Q(type=12) | Q(type=13)).count()

    elif item == 'biblio_sources':
        return Source.objects.filter(type__lte=11).count()

    elif item == 'wiki-articles':
        return wiki_page.objects.filter(page_is_new=1).count()

    elif item == 'assets':
        return rs_resource.objects.count()

    else:
        return None

#Special functions [outdated?]
def inventory_check(_file):
    """
    Takes the data from a DALME Inventory Package and makes sure it's properly formatted
    """

    # TODO: ALSO NEEDS TO CHECK IF INVENTORY ALREADY EXISTS

    metadata_tag = '*METADATA*'
    structure_tag = '*STRUCTURE*'
    transcription_tag = '*TRANSCRIPTION*'

    status = {}

    with _file as f:
        text = f.read()
        text = text.decode("utf-8")

    #check that the metadata section is there
    if metadata_tag in text:
        status['has_metadata'] = 1
    else:
        status['has_metadata'] = 0

    #check if the file has a STRUCTURE section
    if structure_tag in text:
        status['has_structure'] = 1
    else:
        status['has_structure'] = 0

    #check if the file has a TRANSCRIPTION section
    if transcription_tag in text:
        status['has_transcription'] = 1
    else:
        status['has_transcription'] = 0

    #if the STRUCTURE section is missing, just stop and send the report back
    if status['has_structure'] == 0:
        return status

    else:
        #remove blank lines
        empty_pattern = re.compile(r'\n$', re.MULTILINE)
        text = empty_pattern.sub('', text)
        status['text'] = text

        #determine the boundaries of each section
        lines = text.split('\n')
        #get the starting lines for all the sections and the file's last line
        last_line = len(lines)
        for num, line in enumerate(lines, 1):
            if metadata_tag in line:
                status['metadata_start'] = num

            elif structure_tag in line:
                status['structure_start'] = num

            elif transcription_tag in line:
                status['transcription_start'] = num

        #assign the outer boundaries of each section
        #if it has a METADATA section, assign outer boundary and parse it
        if status['has_metadata'] == 1:
            status['metadata_end'] = status['structure_start'] - 1
            meta_lines = lines[status['metadata_start']:status['metadata_end']]
            label_pattern = re.compile(r'^([\w ]+):', re.IGNORECASE)
            line_pattern = re.compile(r'([\w ]+): (.+)', re.IGNORECASE)
            full_pattern = re.compile(r'(.+)', re.IGNORECASE)
            #get metadata
            meta_dict = {}
            for line in meta_lines:
                if label_pattern.match(line) != None:
                    m = line_pattern.match(line)
                    label = m.group(1)
                    content = m.group(2)
                    meta_dict[label] = content.rstrip()

                else:
                    new_content = line.rstrip()
                    old_content = meta_dict[label]
                    meta_dict[label] = old_content + '\n' + new_content

            status['metadata'] = meta_dict

            #see which fields are included and whether all the required ones are present
            required_fields = ['Title', 'Archival source', 'Country', 'Series', 'Shelf', 'Transcriber']
            required = 1
            fields = []
            for i in required_fields:
                if i in meta_dict:
                    present = 1
                else:
                    present = 0
                    required = 0
                fields.append((i,present))

            status['fields'] = fields
            status['required'] = required

        if status['has_transcription'] == 1:
            status['structure_end'] = status['transcription_start'] - 1
            status['transcription_end'] = last_line
        else:
            status['structure_end'] = last_line

    return status


def tokenise(line, t_type):
    """
    Takes a line and returns a list of dictionaries, one for each token, with all the pertinent attributes
    """

    #create the tokens
    tokens = line.split(' ')
    keyword_substract = 0
    type_pattern = re.compile(r'(CONTEXT|INVENTORY):')
    token_type = t_type
    tokens_dict = {}
    tokens_list = []

    for num, token in enumerate(tokens, 1):
        if type_pattern.match(token):
            m = type_pattern.match(token)
            token_type = m.group(1)
            keyword_substract = keyword_substract + 1

        else:
            #deal with flags, situations to consider:
            #[nostri]
            #presen[tibus]
            #lxxxxvii^o^
            #-Ad evit-
            #(word missing) or (word or words missing)
            #?sin[e]berti?
            #^quondam^
            #-dicti-
            #-?Raymunde?-
            #?als arcs?

            #also flags for need punctuation, so it can be used later for defining sentences
            #and tokens should be lower-case, but track uppercase for determining sentences+proper names?

            tags_pattern = re.compile(r'(-|\?|\^|\[|\]|\.)')
            tags_pattern_enc = re.compile(r'^(-|\?|\^|\[|\.)([a-z]+)(-|\?|\^|\]|\.)$', re.IGNORECASE)
            tags_pattern_hyphen = re.compile(r'(_|\[_\])$')
            tags_pattern_period = re.compile(r'\.$')
            tags_pattern_partial = re.compile(r'([a-z]+)(-|\?|\^|\[|\]|\{|\()([a-z]+)(-|\?|\^|\[|\]|\{|\()(-|\?|\^|\[|\]|\{|\(|([a-z]*))', re.IGNORECASE)

            if tags_pattern.search(token):

                #first check for simple cases of flags that enclose words
                if tags_pattern_enc.search(token):
                    m = tags_pattern_enc.search(token)
                    flags = m.group(1)
                    clean_token = m.group(2)
                    norm_token = clean_token.lower()
                    tokens_dict = {}
                    tokens_dict['position'] = num - keyword_substract
                    tokens_dict['raw_token'] = token
                    tokens_dict['clean_token'] = clean_token
                    tokens_dict['norm_token'] = norm_token
                    tokens_dict['token_type'] = token_type
                    tokens_dict['flags'] = flags
                    tokens_dict['span_start'] = None
                    tokens_dict['span_end'] = None

                #then words that break at the end of a line, we'll just flag them here and rejoin them later
                elif tags_pattern_hyphen.search(token):
                    flags = '_'
                    clean_token = tags_pattern_hyphen.sub('', token)
                    norm_token = clean_token.lower()
                    tokens_dict = {}
                    tokens_dict['position'] = num - keyword_substract
                    tokens_dict['raw_token'] = token
                    tokens_dict['clean_token'] = clean_token
                    tokens_dict['norm_token'] = norm_token
                    tokens_dict['token_type'] = token_type
                    tokens_dict['flags'] = flags
                    tokens_dict['span_start'] = None
                    tokens_dict['span_end'] = None

                #then check for full stops, i.e. flag tokens that mark end-of-sentence
                elif tags_pattern_period.search(token):
                    flags = 'eos'
                    clean_token = tags_pattern_period.sub('', token)
                    norm_token = clean_token.lower()
                    tokens_dict = {}
                    tokens_dict['position'] = num - keyword_substract
                    tokens_dict['raw_token'] = token
                    tokens_dict['clean_token'] = clean_token
                    tokens_dict['norm_token'] = norm_token
                    tokens_dict['token_type'] = token_type
                    tokens_dict['flags'] = flags
                    tokens_dict['span_start'] = None
                    tokens_dict['span_end'] = None

                #check for tags enclosing only part of the word
                elif tags_pattern_partial.search(token):
                     m = tags_pattern_partial.search(token)
                     t = tags_pattern.search(token)
                     flags = t.group(1)
                     clean_token = m.group(1) + m.group(3) + m.group(5)
                     norm_token = clean_token.lower()
                     span_start = str(m.start())
                     span_end = str(m.end())
                     tokens_dict = {}
                     tokens_dict['position'] = num - keyword_substract
                     tokens_dict['raw_token'] = token
                     tokens_dict['clean_token'] = clean_token
                     tokens_dict['norm_token'] = norm_token
                     tokens_dict['token_type'] = token_type
                     tokens_dict['flags'] = flags
                     tokens_dict['span_start'] = span_start
                     tokens_dict['span_end'] = span_end

                else:
                    flags = ''
                    clean_token = 'FUCK'
                    norm_token = clean_token.lower()
                    tokens_dict = {}
                    tokens_dict['position'] = num - keyword_substract
                    tokens_dict['raw_token'] = token
                    tokens_dict['clean_token'] = clean_token
                    tokens_dict['norm_token'] = norm_token
                    tokens_dict['token_type'] = token_type
                    tokens_dict['flags'] = flags
                    tokens_dict['span_start'] = None
                    tokens_dict['span_end'] = None
            else:
                flags = ''
                clean_token = token
                norm_token = clean_token.lower()
                tokens_dict = {}
                tokens_dict['position'] = num - keyword_substract
                tokens_dict['raw_token'] = token
                tokens_dict['clean_token'] = clean_token
                tokens_dict['norm_token'] = norm_token
                tokens_dict['token_type'] = token_type
                tokens_dict['flags'] = flags
                tokens_dict['span_start'] = None
                tokens_dict['span_end'] = None

            tokens_list.append(tokens_dict)

    results = [token_type, tokens_list]

    return results

def get_inventory(inv, output_type):
    """
    Returns information associated with an inventory in the specified format
    """

    if output_type == 'full':
        results = []
        folios = inv.par_folio_set.all()
        folios = folios.order_by('folio_no')
        line = 1
        for i in folios:
            folio_no = i.folio_no
            image_url = get_dam_preview(i.dam_id)
            folio_list = [folio_no,image_url]
            tokens = i.par_token_set.all()
            tokens = tokens.order_by('line_no', 'position')
            all_lines = []
            line_list = [line]
            line_tokens = []
            no_tokens = len(tokens)
            for num, token in enumerate(tokens, 1):
                if num == no_tokens:
                    out_token = token.clean_token
                    out_class = get_display_token_class(token.flags)
                    line_tokens.append((out_token, out_class))
                    line_list.append(line_tokens)
                    all_lines.append(line_list)
                    line = line + 1
                    line_list = [line]
                    line_tokens = []

                else:
                    if token.line_no != line:
                        line_list.append(line_tokens)
                        all_lines.append(line_list)
                        line = line + 1
                        line_list = [line]
                        line_tokens = []
                        out_token = token.clean_token
                        out_class = get_display_token_class(token.flags)
                        line_tokens.append((out_token, out_class))

                    else:
                        out_token = token.clean_token
                        out_class = get_display_token_class(token.flags)
                        line_tokens.append((out_token, out_class))

            folio_list.append(all_lines)
            results.append(folio_list)

    return results

def get_display_token_class(flag):
    if flag == '-':
        token_class = 'token_strikeout'

    elif flag == '^':
        token_class = 'token_superscript'

    elif flag == '?':
        token_class = 'token_uncertain'

    elif flag == '[':
        token_class = 'token_supplied'

    elif flag == '{':
        token_class = 'token_imputed'

    elif flag == '':
        token_class = 'token_clean'

    elif flag == '.':
        token_class = 'token_periods'

    elif flag == 'eos':
        token_class = 'token_eos'

    else:
        token_class = 'token_flag_error'

    return token_class

def bar_chart():
    results = []
    materials = par_object.objects.order_by().values_list('material', flat=True).distinct()

    for i in materials:
        count = par_object.objects.filter(material=i).count()
        entry = (i, count)
        results.append(entry)

    return results

def get_task_icon(list_id):
    if list_id == 1:
        icon = 'fa-gears'
    return icon

def get_date_from_elements(day, month, year):
    #do some stuff
    if year:
        if month:
            month_name = calendar.month_name[abs(int(month))]
            if day:
                output = str(abs(int(day))) + ' ' + month_name + ', ' + str(abs(int(year)))

            else:
                output = month_name + ' ' + str(abs(int(year)))
        else:
            output = str(abs(int(year)))
    else:
        output = ''

    return output

def create_user(request, data):

    # process the data in form.cleaned_data as required
    username = data.cleaned_data['username']
    first_name = data.cleaned_data['first_name']
    last_name = data.cleaned_data['last_name']
    email = data.cleaned_data['email']
    is_staff = data.cleaned_data['is_staff']
    is_superuser = data.cleaned_data['is_superuser']
    dam_usergroup = data.cleaned_data['dam_usergroup']
    wiki_groups_list = data.cleaned_data['wiki_groups']
    if wiki_groups_list:
        if len(wiki_groups_list) > 1:
            wiki_groups = '|'.join(wiki_groups_list)
        else:
            wiki_groups = wiki_groups_list[0]
    else:
        wiki_groups = 'users'
    wp_role = data.cleaned_data['wp_role']
    #generate extra fields:
    full_name = first_name + ' ' + last_name
    wiki_username = username.title()
    wiki_realname = username
    password = str(uuid.uuid4().hex)
    wp_user_registered = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    #create a new user object and add the fields
    the_user = User()
    the_user.username = username
    the_user.first_name = first_name
    the_user.last_name = last_name
    the_user.email = email
    the_user.is_staff = is_staff
    the_user.is_superuser = is_superuser
    the_user.save()
    the_user.profile.dam_usergroup = dam_usergroup
    the_user.profile.wp_role = wp_role
    the_user.profile.full_name = full_name
    the_user.profile.wiki_username = wiki_username
    the_user.profile.wiki_groups = wiki_groups
    the_user.save()

    #create record in WP
    wp_db.ping(True)
    cursor = wp_db.cursor()
    cursor.execute("INSERT INTO wp_users (user_login, user_pass, user_nicename, user_email, user_registered, user_status, display_name) VALUES(%s, %s, %s, %s, %s, %s, %s)", (username, password, username, email, wp_user_registered, '0', full_name))

    #get wp user id and add it to User object
    cursor.execute("SELECT ID FROM wp_users WHERE user_login = %s",[username])
    wp_userid = cursor.fetchone()[0]
    the_user.profile.wp_userid = wp_userid
    the_user.save()

    #add user metadata
    cursor.execute("INSERT INTO wp_usermeta (user_id, meta_key, meta_value) VALUES(%s, %s, %s)", (wp_userid, 'first_name', first_name))
    cursor.execute("INSERT INTO wp_usermeta (user_id, meta_key, meta_value) VALUES(%s, %s, %s)", (wp_userid, 'last_name', last_name))
    cursor.execute("INSERT INTO wp_usermeta (user_id, meta_key, meta_value) VALUES(%s, %s, %s)", (wp_userid, 'wp_capabilities', wp_role))

    #create record in wiki
    wiki_db.ping(True)
    cursor = wiki_db.cursor()
    cursor.execute("INSERT INTO user (user_name, user_real_name, user_password, user_newpassword, user_email) VALUES(%s, %s, %s, %s, %s)", (wiki_username, wiki_realname, password, password, email))

    #get wiki user id and add it to User object
    cursor.execute("SELECT user_id FROM user WHERE user_name = %s",[wiki_username])
    wiki_userid = cursor.fetchone()[0]
    the_user.profile.wiki_userid = wiki_userid
    the_user.save()

    #add user to groups if necessary
    if wiki_groups != 'user':
        for i in wiki_groups_list:
            if i == 'administrator':
                ug_group = 'sysop'
            elif i == 'bureaucrat':
                ug_group = 'bureaucrat'

            cursor.execute("INSERT INTO user_groups (ug_user, ug_group) VALUES(%s, %s)", (wiki_userid, ug_group))


    #create record in dam
    dam_db.ping(True)
    cursor = dam_db.cursor()
    cursor.execute("INSERT INTO user (username, password, fullname, email, usergroup, approved) VALUES(%s, %s, %s, %s, %s, %s)",(username, password, full_name, email,dam_usergroup,1))

    #get dam user id and add it to User object
    cursor.execute("SELECT ref FROM user WHERE username = %s",[username])
    dam_userid = cursor.fetchone()[0]
    the_user.profile.dam_userid = dam_userid
    the_user.save()
